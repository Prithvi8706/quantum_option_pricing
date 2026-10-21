"""Bounded, paid reversible DAG pebbling with atomic producer lifetimes.

This module plans native leaf invocations, never arithmetic approximations.  An
erase has the same predecessor requirements as a compute.  Rebuilding a missing
predecessor appends actual paid invocations.  Failed speculative planning paths
are rolled back before emission, while their search budget remains charged.
"""

from copy import deepcopy
from fractions import Fraction
from math import isqrt
from time import process_time


ALGORITHM = "paid-atomic-dag-checkpointing-v1"
HEURISTICS = ("block", "cost-aware")
LIMITS = dict(max_events=100_000, max_moves=20_000, max_cpu_seconds=900)


class PlanningError(Exception):
    """A bounded planner cannot finish this proposed schedule."""


def _normalise(plan):
    floor = int(plan["floor"])
    groups = {int(group["id"]): deepcopy(group) for group in plan["groups"]}
    if floor < 0 or len(groups) != len(plan["groups"]):
        raise ValueError("invalid floor or duplicate atomic group")
    order = list(groups)
    rank = {group: index for index, group in enumerate(order)}
    owners = {}
    for group in groups.values():
        gid = int(group["id"])
        group["preds"] = tuple(dict.fromkeys(int(p) for p in group["preds"]))
        for field in ("width", "private", "cost"):
            group[field] = int(group[field])
            if group[field] < 0:
                raise ValueError(f"negative {field}")
        for pred in group["preds"]:
            if pred not in groups or rank[pred] >= rank[gid]:
                raise ValueError("missing, self, or forward predecessor")
        for value in group["outputs"]:
            if value in owners:
                raise ValueError("value has multiple atomic producers")
            owners[value] = gid
    outputs = deepcopy(plan["outputs"])
    names = set()
    for binding in outputs:
        name, value = binding["outputname"], binding["value"]
        if name in names or value not in owners:
            raise ValueError("duplicate output name or nonproduced output")
        names.add(name)
        if int(binding.get("group", owners[value])) != owners[value]:
            raise ValueError("output binding disagrees with atomic owner")
        binding["group"] = owners[value]
    return floor, groups, order, rank, outputs


def minimum_required(plan):
    """An independent local lower bound: floor + one leaf + all its inputs."""
    floor, groups, order, _, _ = _normalise(plan)
    rows = [
        dict(
            group=gid,
            total=floor
            + groups[gid]["width"]
            + groups[gid]["private"]
            + sum(groups[p]["width"] for p in groups[gid]["preds"]),
        )
        for gid in order
    ]
    return max(rows, key=lambda row: row["total"], default=dict(group=None, total=floor))


class _Planner:
    def __init__(self, plan, cap, heuristic):
        self.floor, self.groups, self.order, self.rank, self.outputs = _normalise(plan)
        self.cap, self.heuristic = int(cap), heuristic
        self.moves, self.live = [], {}
        self.free = [(self.floor, self.cap - self.floor)]
        self.events, self.peak_live, self.highwater = 0, self.floor, self.floor
        self.paid_moves = 0
        self.started = process_time()
        self.stack = set()
        self.block_size = max(1, isqrt(len(self.order)))
        if self.block_size * self.block_size < len(self.order):
            self.block_size += 1
        self.block = {gid: self.rank[gid] // self.block_size for gid in self.order}
        consumers = {gid: [] for gid in self.order}
        for gid, group in self.groups.items():
            for pred in group["preds"]:
                consumers[pred].append(gid)
        self.last_block = {
            gid: max([self.block[gid], *(self.block[c] for c in consumers[gid])])
            for gid in self.order
        }
        self.checkpoints = {gid for gid in self.order if self.last_block[gid] > self.block[gid]}
        self.rebuild_cost = {}
        for gid in self.order:
            ancestors, todo = set(), [gid]
            while todo:
                item = todo.pop()
                if item not in ancestors:
                    ancestors.add(item)
                    todo.extend(self.groups[item]["preds"])
            self.rebuild_cost[gid] = sum(self.groups[a]["cost"] for a in ancestors)

    def tick(self):
        self.events += 1
        if self.events > LIMITS["max_events"]:
            raise PlanningError("recursive event limit")
        if process_time() - self.started > LIMITS["max_cpu_seconds"]:
            raise PlanningError("process CPU limit")

    def record(self, move):
        if move["kind"] != "copy_output":
            if self.paid_moves >= LIMITS["max_moves"]:
                raise PlanningError("paid invocation limit")
            self.paid_moves += 1
        self.moves.append(move)

    def snapshot(self):
        return (
            len(self.moves),
            deepcopy(self.live),
            list(self.free),
            self.peak_live,
            self.highwater,
            self.paid_moves,
        )

    def restore(self, snapshot):
        length, self.live, self.free, self.peak_live, self.highwater, self.paid_moves = snapshot
        del self.moves[length:]

    def available(self):
        return sum(width for _, width in self.free)

    def allocate(self, width):
        if width > self.available():
            raise PlanningError("allocation exceeds cap")
        spans, remaining = [], width
        while remaining:
            offset, count = self.free.pop(0)
            take = min(count, remaining)
            spans.append(dict(offset=offset, width=take))
            if count > take:
                self.free.insert(0, (offset + take, count - take))
            remaining -= take
            self.highwater = max(self.highwater, offset + take)
        self.peak_live = max(self.peak_live, self.cap - self.available())
        return spans

    def release(self, spans):
        self.free.extend((span["offset"], span["width"]) for span in spans)
        merged = []
        for offset, width in sorted(self.free):
            if merged and merged[-1][0] + merged[-1][1] == offset:
                merged[-1] = (merged[-1][0], merged[-1][1] + width)
            else:
                merged.append((offset, width))
        self.free = merged

    def priority(self, gid):
        if self.heuristic == "block":
            return (gid in self.checkpoints, -self.rank[gid])
        return (
            Fraction(self.rebuild_cost[gid], max(1, self.groups[gid]["width"])),
            -self.rank[gid],
        )

    def make_room(self, width, protected):
        while self.available() < width:
            self.tick()
            candidates = [
                gid
                for gid in self.live
                if gid not in protected
                and self.groups[gid]["width"]
                and ("erase", gid) not in self.stack
            ]
            # An erase requiring no reconstruction gets the first attempt.
            candidates.sort(
                key=lambda gid: (
                    not (
                        all(p in self.live for p in self.groups[gid]["preds"])
                        and self.available() >= self.groups[gid]["private"]
                    ),
                    self.priority(gid),
                )
            )
            progress = False
            for victim in candidates:
                saved, before = self.snapshot(), self.available()
                try:
                    self.erase(victim, protected)
                    if self.available() <= before:
                        raise PlanningError("eviction made no net room")
                    progress = True
                    break
                except PlanningError:
                    self.restore(saved)
                    self.tick()  # Failed branches consume the fixed search budget.
            if not progress:
                raise PlanningError("no legal paid eviction fits this cap")

    def ensure(self, gid, protected):
        self.tick()
        if gid in self.live:
            return
        operation = ("compute", gid)
        if operation in self.stack:
            raise PlanningError("recursive compute cycle")
        self.stack.add(operation)
        try:
            group = self.groups[gid]
            held = set(protected)
            for pred in group["preds"]:
                self.ensure(pred, held)
                held.add(pred)
            self.make_room(group["width"] + group["private"], held)
            storage = self.allocate(group["width"])
            private = self.allocate(group["private"])
            self.record(
                dict(
                    kind="compute",
                    group=gid,
                    storage=deepcopy(storage),
                    private_storage=deepcopy(private),
                )
            )
            self.live[gid] = storage
            self.release(private)
        finally:
            self.stack.remove(operation)

    def erase(self, gid, protected):
        self.tick()
        if gid not in self.live:
            return
        if gid in protected:
            raise PlanningError("attempted protected checkpoint erase")
        operation = ("erase", gid)
        if operation in self.stack:
            raise PlanningError("recursive erase cycle")
        self.stack.add(operation)
        try:
            group = self.groups[gid]
            held = set(protected) | {gid}
            for pred in group["preds"]:
                self.ensure(pred, held)
                held.add(pred)
            self.make_room(group["private"], held)
            private = self.allocate(group["private"])
            self.record(
                dict(
                    kind="erase",
                    group=gid,
                    storage=deepcopy(self.live[gid]),
                    private_storage=deepcopy(private),
                )
            )
            self.release(private)
            self.release(self.live.pop(gid))
        finally:
            self.stack.remove(operation)

    def copy(self, binding):
        self.ensure(binding["group"], set())
        self.record(
            dict(
                kind="copy_output",
                group=binding["group"],
                value=binding["value"],
                outputname=binding["outputname"],
            )
        )

    def clean_except(self, protected):
        while set(self.live) - protected:
            self.tick()
            victim = max(set(self.live) - protected, key=self.rank.__getitem__)
            self.erase(victim, protected)

    def run(self):
        if self.heuristic == "block":
            bindings = {}
            for binding in self.outputs:
                bindings.setdefault(binding["group"], []).append(binding)
            for start in range(0, len(self.order), self.block_size):
                block = self.order[start : start + self.block_size]
                for gid in block:
                    self.ensure(gid, set())
                    for binding in bindings.get(gid, []):
                        self.copy(binding)
                index = self.block[block[-1]]
                protected = {gid for gid in self.live if self.last_block[gid] > index}
                self.clean_except(protected)
        else:
            for binding in self.outputs:
                self.copy(binding)
        self.clean_except(set())
        return dict(
            passed=True,
            algorithm=ALGORITHM,
            heuristic=self.heuristic,
            cap=self.cap,
            floor=self.floor,
            moves=self.moves,
            observed_peak_live=self.peak_live,
            logical_qubits=self.highwater,
            events=self.events,
            process_cpu_seconds=process_time() - self.started,
            block_size=self.block_size if self.heuristic == "block" else None,
            leaf_invocations=sum(move["kind"] != "copy_output" for move in self.moves),
            limits=deepcopy(LIMITS),
        )


def schedule(plan, cap, heuristic):
    """Return one legal bounded proposal, or an explicit non-executable failure."""
    if heuristic not in HEURISTICS:
        raise ValueError("undeclared checkpointing heuristic")
    minimum = minimum_required(plan)
    if int(cap) < minimum["total"]:
        return dict(
            passed=False,
            algorithm=ALGORITHM,
            heuristic=heuristic,
            cap=int(cap),
            reason="mandatory leaf and live predecessor lower bound exceeds cap",
            infeasible_proved=True,
            minimum_required=minimum,
            moves=[],
            limits=deepcopy(LIMITS),
        )
    planner = _Planner(plan, cap, heuristic)
    try:
        result = planner.run()
        result["minimum_required"] = minimum
        result["legality"] = validate_schedule(plan, result)
        return result
    except PlanningError as exc:
        return dict(
            passed=False,
            algorithm=ALGORITHM,
            heuristic=heuristic,
            cap=int(cap),
            reason=str(exc),
            infeasible_proved=False,
            minimum_required=minimum,
            moves=[],
            discarded_partial_moves=len(planner.moves),
            events=planner.events,
            process_cpu_seconds=process_time() - planner.started,
            limits=deepcopy(LIMITS),
        )


def retain_all(plan):
    """Emit the matched retain-all control with a fixed private scratch bank."""
    floor, groups, order, _, bindings = _normalise(plan)
    total_width = sum(group["width"] for group in groups.values())
    maximum_private = max((group["private"] for group in groups.values()), default=0)
    cap, cursor = floor + total_width + maximum_private, floor
    storage = {}
    for gid in order:
        width = groups[gid]["width"]
        storage[gid] = [dict(offset=cursor, width=width)] if width else []
        cursor += width
    moves = []
    for kind, sequence in (("compute", order), ("erase", list(reversed(order)))):
        if kind == "erase":
            moves.extend(
                dict(
                    kind="copy_output",
                    group=binding["group"],
                    value=binding["value"],
                    outputname=binding["outputname"],
                )
                for binding in bindings
            )
        for gid in sequence:
            count = groups[gid]["private"]
            moves.append(
                dict(
                    kind=kind,
                    group=gid,
                    storage=deepcopy(storage[gid]),
                    private_storage=[dict(offset=cursor, width=count)] if count else [],
                )
            )
    result = dict(
        passed=True,
        algorithm=ALGORITHM,
        heuristic="retain-all",
        cap=cap,
        floor=floor,
        moves=moves,
        leaf_invocations=2 * len(groups),
        transient_workspace=total_width + maximum_private,
    )
    result["legality"] = validate_schedule(plan, result)
    result.update(
        observed_peak_live=result["legality"]["observed_peak_live"],
        logical_qubits=result["legality"]["logical_qubits"],
    )
    return result


def _scope_plan(scope):
    """Adapt the fingerprinted financial extraction without changing its IDs."""
    return dict(
        floor=scope["fixed_floor"],
        groups=[
            dict(
                id=group["id"],
                preds=group["preds"],
                width=group["width"],
                private=group["private"],
                cost=group["cost"],
                outputs=group.get("outputs", group.get("out")),
            )
            for group in scope["groups"]
        ],
        outputs=[
            dict(
                outputname=binding.get("outputname", binding.get("name")),
                value=binding["value"],
                group=binding["group"],
            )
            for binding in scope["outputs"]
        ],
    )


def plan_checkpoint(scope, cap, heuristic):
    """Financial producer entry point using the prospectively named families."""
    names = {"block-checkpointing": "block", "cost-aware": "cost-aware"}
    if heuristic not in names:
        raise ValueError("undeclared financial checkpointing heuristic")
    result = schedule(_scope_plan(scope), cap, names[heuristic])
    result["heuristic"] = heuristic
    result["feasible"] = result["passed"]
    return result


def retain_all_plan(scope):
    result = retain_all(_scope_plan(scope))
    result["feasible"] = result["passed"]
    return result


def validate_schedule(plan, result):
    """Scan lifetime legality and physical intervals without using planner state."""
    floor, groups, _, _, bindings = _normalise(plan)
    cap = int(result["cap"])
    live, copied, intervals = {}, set(), {}
    output_by_name = {binding["outputname"]: binding for binding in bindings}
    peak, highwater = floor, floor

    def check_spans(spans, expected, existing):
        if sum(int(span["width"]) for span in spans) != expected:
            raise ValueError("incorrect register width")
        local = []
        for span in spans:
            low, size = int(span["offset"]), int(span["width"])
            high = low + size
            if size <= 0 or low < floor or high > cap:
                raise ValueError("allocation outside declared workspace cap")
            for left, right in [*existing, *local]:
                if low < right and left < high:
                    raise ValueError("dirty overwrite or aliased live register")
            local.append((low, high))
        return local

    for move in result["moves"]:
        kind = move["kind"]
        gid = int(move["group"])
        if gid not in groups:
            raise ValueError("unknown atomic producer")
        group = groups[gid]
        occupied = [interval for spans in intervals.values() for interval in spans]
        if kind == "copy_output":
            name = move["outputname"]
            if name not in output_by_name or name in copied:
                raise ValueError("missing or repeated output binding")
            binding = output_by_name[name]
            if gid not in live or gid != binding["group"] or move["value"] != binding["value"]:
                raise ValueError("output alias does not have its atomic producer live")
            copied.add(name)
            continue
        if kind not in ("compute", "erase"):
            raise ValueError("unknown lifetime move")
        if any(pred not in live for pred in group["preds"]):
            raise ValueError("missing predecessor for compute or checked erase")
        if kind == "compute":
            if gid in live:
                raise ValueError("compute into dirty atomic producer")
            allocated = check_spans(move["storage"], group["width"], occupied)
            occupied.extend(allocated)
            intervals[gid], live[gid] = allocated, deepcopy(move["storage"])
        elif gid not in live or move["storage"] != live[gid]:
            raise ValueError("erase does not bind the live atomic producer register")
        private = check_spans(move["private_storage"], group["private"], occupied)
        all_intervals = [*occupied, *private]
        peak = max(peak, floor + sum(right - left for left, right in all_intervals))
        highwater = (
            max(highwater, *(right for _, right in all_intervals)) if all_intervals else highwater
        )
        if kind == "erase":
            del intervals[gid], live[gid]
    if live:
        raise ValueError("checkpoint cleanup incomplete")
    if copied != set(output_by_name):
        raise ValueError("protected output copy missing")
    if peak > cap or highwater > cap:
        raise ValueError("observed allocation exceeds cap")
    return dict(
        passed=True,
        observed_peak_live=peak,
        logical_qubits=highwater,
        copied_outputs=len(copied),
        all_intermediates_erased=True,
    )
