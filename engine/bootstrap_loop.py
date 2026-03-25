import os, time, subprocess

def run(cmd):
    try:
        subprocess.run(cmd, check=False)
    except Exception:
        pass

def main():
    while True:
        # drive existing system instead of replacing it
        run(["python", "install/engine/next_action_engine.py"])
        run(["python", "install/engine/execute_next_action.py"])
        run(["python", "install/ingestion_v2.py"])
        time.sleep(5)

if __name__ == "__main__":
    main()
