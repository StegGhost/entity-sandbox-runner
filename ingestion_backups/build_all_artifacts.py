import argparse
import json
from pathlib import Path
from runner.report_writer import write_summary_report
from runner.data_collector import append_admissibility_observations
from runner.aggregate_builder import rebuild_admissibility_stats
from runner.report_index import build_indexes
from runner.handoff import build_handoff_manifest

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", required=True)
    args = parser.parse_args()

    result_path = Path("results") / f"{args.experiment}_results.json"
    if not result_path.exists():
        raise FileNotFoundError(result_path)

    result = json.loads(result_path.read_text(encoding="utf-8"))
    report_path = write_summary_report(args.experiment, result)
    append_admissibility_observations(args.experiment, result)
    stats = rebuild_admissibility_stats()

    validation = Path("reports/validation")
    validation.mkdir(parents=True, exist_ok=True)
    (validation / "admissibility_validation_summary.json").write_text(
        json.dumps(stats, indent=2), encoding="utf-8"
    )

    build_indexes()
    build_handoff_manifest(args.experiment, str(result_path), [report_path])
    print(f"Artifacts built for {args.experiment}")

if __name__ == "__main__":
    main()
