"""Independent metadata-only reconstruction; no scalar/gate/candidate evaluation."""

import hashlib
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
START = time.monotonic()
BASE = ROOT / "results/limitation_program_20261001"


def require(condition, message):
    if not condition:
        raise ValueError(message)
    if time.process_time() >= 30 or time.monotonic()-START >= 90:
        raise ValueError("Fixed30CPU90wall review cap")


def digest(path):
    data = path.read_bytes()
    require(len(data) <= 64*1024**2, "Bounded selected metadata file")
    return hashlib.sha256(data).hexdigest()


def read(path, expected):
    require(digest(path)==expected, "Exact fixed metadata pin: "+str(path))
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    policy = json.loads((HERE/"A20_STATIC_REVIEW_PREFLIGHT_v5.json").read_text())
    target = read(BASE/"A10_coefficient_run001/B4x12/min-depth/target.json",policy["fixed_target_expected_SHA256"])
    source = read(BASE/"A10_coefficient_run001/B4x12/min-depth/source.json",policy["fixed_source_expected_SHA256"])
    census = read(BASE/"E22_census_run002/B4x12_predicate_census.json",policy["fixed_census_expected_SHA256"])
    owner = read(BASE/"A10_coefficient_run001/manifest.json",policy["original_owner_manifest_expected_SHA256"])
    diagnostic = read(BASE/"A20_continuation_20261004_template_diagnostic_run001/summary.json",policy["diagnostic_summary_expected_SHA256"])
    require((target["width"],target["fraction_bits"])==(72,40),"Same-word native source")
    producers = {value: node for node in target["nodes"] for value in node["out"]}
    closures = []
    for asset in (0,1):
        sites = [row for row in census["builder_label_proof"]["exponentials"] if row["asset"]==asset and row["date"]==0]
        require(len(sites)==1,"Exact date0 occurrence")
        site = sites[0]
        boundary=site["clipped_log"]
        seen,order=set(),[]
        def visit(value):
            if value==boundary or value in seen:
                return
            node=producers[value]
            require(node["op"] in {"const","add","sub","mul","cmul","bits","shift"} and node["out"]==[value],"Closed scalar metadata")
            for dependency in node["args"]:
                visit(dependency)
            seen.add(value)
            order.append(node)
            require(len(order)<=45,"Fixed45closure cap")
        visit(site["stock"])
        require(len(order)==45,"Complete fixed45node closure")
        numbers={boundary:0}
        normalized=[]
        correspondence=[]
        for node in order:
            value=node["out"][0]
            numbers[value]=len(numbers)
            normalized.append(dict(op=node["op"],args=[numbers[v] for v in node["args"]],params=node["params"],out=numbers[value]))
            correspondence.append(dict(normalized_output=numbers[value],original_output_SSA=value))
        saved=diagnostic["closures"][asset]
        require(saved["normalized_nodes"]==normalized and saved["SSA_correspondence"]==correspondence,"Independent reconstruction matches exact diagnostic bytes")
        require(saved["normalized_output"]==45,"Complete output binding")
        clamps=[]
        clip=[row for row in census["builder_label_proof"]["clips"] if row["out"]==boundary]
        require(len(clip)==1,"Bound original clamp")
        for key in ("low","high"):
            literal=producers[clip[0][key]]
            require(literal["op"]=="const","Unchanged literal clamp")
            raw=literal["params"]["value"]
            clamps.append(raw-(1<<72) if raw&(1<<71) else raw)
        require(clamps==policy["clamps_must_equal"],"Exact same clamp domain")
        closures.append(dict(asset=asset,normalized_nodes=normalized,SSA_correspondence=correspondence,clamps=clamps))
    differences=[]
    for a,b in zip(closures[0]["normalized_nodes"],closures[1]["normalized_nodes"],strict=True):
        if a!=b:
            require(a["op"]==b["op"]=="mul" and a["params"]==b["params"]=={} and a["out"]==b["out"] and a["args"]==b["args"][::-1],"Only exact multiplication argument reversal")
            differences.append(a["out"])
    require(differences==policy["difference_normalized_outputs"],"Exactly the five fixed swaps")
    canonical=[]
    for closure in closures:
        canonical.append([{**node,"args":sorted(node["args"]) if node["op"]=="mul" else node["args"]} for node in closure["normalized_nodes"]])
    require(canonical[0]==canonical[1],"Only mul canonicalization gives exact normalized equality")
    metadata=[]
    for closure in closures:
        correspondence={row["normalized_output"]:row["original_output_SSA"] for row in closure["SSA_correspondence"]}
        for out in differences:
            original=correspondence[out]
            calls=[call for call in source["forward_calls"] if call["out"]==[original]]
            require(len(calls)==1,"Exact accepted source call at selected SSA")
            call=calls[0]
            require(call["args"]==producers[original]["args"],"Actual backend argument order stays unchanged")
            path=BASE/"A10_coefficient_run001/B4x12/min-depth/leaves"/(call["leaf"]+".json")
            keys=[key for key in owner["files"] if key.replace("\\","/").endswith("B4x12/min-depth/leaves/"+path.name)]
            require(len(keys)==1,"Unique original owner metadata hash")
            leaf=read(path,owner["files"][keys[0]])
            metadata.append(dict(asset=closure["asset"],normalized_output=out,original_SSA=original,
                                 call=call,leaf_key=call["leaf"],leaf_metadata_expected_SHA256=owner["files"][keys[0]],
                                 leaf_op=leaf.get("op"),leaf_params=leaf.get("params"),leaf_spec=leaf.get("spec"),
                                 input_contract=leaf.get("input_contract"),ports=leaf.get("args"),resources=leaf.get("resources")))
    require(len(metadata)==10,"All ten fixed selected backend metadata rows")
    record=dict(schema="a20-mul-commutativity-metadata-review-v5",passed=True,scientific_execution=False,
                closures=closures,difference_outputs=differences,mul_only_canonicalized_metadata_equal=True,
                selected_backend_metadata=metadata,whole_source_cost_equivalence=False,new_fixture_credit=0,
                budget=dict(CPU=time.process_time(),wall=time.monotonic()-START))
    with (HERE/"A20_MUL_METADATA_REVIEW_v5.json").open("x",encoding="utf-8") as stream:
        stream.write(json.dumps(record,sort_keys=True,indent=2)+"\n")
    print(json.dumps({"passed":True,"closure_nodes":[45,45],"five_outputs":differences,"backend_rows":metadata},sort_keys=True))


if __name__=="__main__":
    main()
