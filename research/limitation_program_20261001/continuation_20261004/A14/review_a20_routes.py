"""Literal-path audit across A20 author versions; no scientific imports."""

import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
RESEARCH=ROOT/"research/limitation_program_20261001"
HERE=Path(__file__).resolve().parent


def literals(text):
    return Counter(node.value for node in ast.walk(ast.parse(text))
                   if isinstance(node,ast.Constant) and isinstance(node.value,str)
                   and (node.value.startswith(("research.","research/","results/",".context/","A20_continuation_"))
                        or node.value.endswith((".py",".json",".md"))
                        or node.value.startswith("A20-comparator-phase-static-READY-")))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--version",choices=("v5","v6"),required=True)
    args=parser.parse_args()
    version=args.version
    run="003" if version=="v5" else "004"
    files={"arithmetic_free_basket_signal_v2.py":"arithmetic_free_basket_signal_continuation_"+version+".py"}
    for stem in ("a20_signal_receipt_continuation_","experiment_arithmetic_free_basket_signal_continuation_","audit_arithmetic_free_basket_signal_continuation_"):
        files[stem+"v4.py"]=stem+version+".py"
    replacements={**files,
        "A20_COMPARATOR_PHASE_CONTINUATION_PREFLIGHT_V4.md":"A20_COMPARATOR_PHASE_CONTINUATION_PREFLIGHT_"+version.upper()+".md",
        "a20_comparator_phase_continuation_preflight_v4.json":"a20_comparator_phase_continuation_preflight_"+version+".json",
        "A20-comparator-phase-static-READY-v4":"A20-comparator-phase-static-READY-"+version,
        "A20_continuation_20261004_producer_run002":"A20_continuation_20261004_producer_run"+run,
        "A20_continuation_20261004_audit_run002":"A20_continuation_20261004_audit_run"+run}
    replacements.update({key[:-3]:value[:-3] for key,value in files.items()})
    record={"schema":"a20-independent-static-literal-route-review-v1","version":version,
            "scientific_execution":False,"path_diff":{},"passed":True}
    for old,new in files.items():
        old_text=(RESEARCH/old).read_text(encoding="utf-8")
        new_data=(RESEARCH/new).read_bytes()
        new_text=new_data.decode("utf-8")
        ast.parse(new_text)
        compile(new_text,new,"exec")
        old_literals=literals(old_text)
        expected=Counter()
        for text,count in old_literals.items():
            altered=text
            for before,after in replacements.items():
                altered=altered.replace(before,after)
            expected[altered]+=count
        current=literals(new_text)
        missing=expected-current
        unexpected=current-expected
        record["path_diff"][new]={"SHA256":hashlib.sha256(new_data).hexdigest(),
                                "missing_expected_literal_counts":dict(missing),
                                "unexpected_literal_counts":dict(unexpected)}
        record["passed"] &= not missing and not unexpected
    with (HERE/("A20_"+version.upper()+"_ROUTE_STATIC_REVIEW_run001.json")).open("x",encoding="utf-8") as stream:
        stream.write(json.dumps(record,sort_keys=True,indent=2)+"\n")
    print(json.dumps(record,sort_keys=True))


if __name__=="__main__":
    main()
