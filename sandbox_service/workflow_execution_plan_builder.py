import json
from pathlib import Path

OUT = Path("sandbox_service/workflow_execution_plan_builder.json")

def main():
    plan = json.loads(Path("sandbox_service/workflow_execution_plan.json").read_text(encoding="utf-8"))
    payload = {"stage_count": len(plan["stages"]), "stages": plan["stages"]}
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
