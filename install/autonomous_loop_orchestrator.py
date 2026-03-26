import subprocess
import json
import time
import os


REPORT_PATH = "payload/runtime/autonomous_loop_report.json"


def run_tests():
    try:
        result = subprocess.run(
            ["pytest", "-q"],
            capture_output=True,
            text=True
        )

        output = result.stdout + "\n" + result.stderr

        print("===== PYTEST OUTPUT BEGIN =====")
        print(output)
        print("===== PYTEST OUTPUT END =====")

        return result.returncode == 0, output

    except Exception as e:
        return False, str(e)


def main():
    os.makedirs("payload/runtime", exist_ok=True)

    tests_passed, test_output = run_tests()

    report = {
        "status": "ok",
        "tests_passed": tests_passed,
        "repair_triggered": not tests_passed,
        "timestamp": time.time(),
        "report": REPORT_PATH,
        "test_output_snippet": test_output[-1000:]  # last 1000 chars
    }

    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
