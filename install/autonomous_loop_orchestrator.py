import os
import json
import subprocess
import time

TEST_OUTPUT = "test_output.txt"
RESULT_PATH = "payload/runtime/autonomous_loop_report.json"


def run_tests():
    proc = subprocess.run(
        "python -m pytest -q",
        shell=True,
        capture_output=True,
        text=True
    )
    return proc.returncode, proc.stdout + proc.stderr


def run_self_improve():
    proc = subprocess.run(
        f"python engine/self_improve_runner.py {TEST_OUTPUT}",
        shell=True,
        capture_output=True,
        text=True
    )
    return proc.returncode, proc.stdout + proc.stderr


def main():

    os.makedirs("payload/runtime", exist_ok=True)

    # 1. RUN TESTS (this is the missing piece)
    rc, out = run_tests()

    with open(TEST_OUTPUT, "w") as f:
        f.write(out)

    # 2. IF FAILURE → TRIGGER REPAIR LOOP
    repair_triggered = False
    repair_output = ""

    if rc != 0:
        repair_triggered = True
        _, repair_output = run_self_improve()

    # 3. STILL PRODUCE RECEIPTS (your existing behavior)
    report = {
        "status": "ok",
        "tests_passed": rc == 0,
        "repair_triggered": repair_triggered,
        "timestamp": time.time(),
        "report": RESULT_PATH
    }

    with open(RESULT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
