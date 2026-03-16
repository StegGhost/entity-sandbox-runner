import subprocess, sys

def main():
    subprocess.run([sys.executable, "result_delivery/build_raw_data_bundle.py"], check=True)

if __name__ == "__main__":
    main()
