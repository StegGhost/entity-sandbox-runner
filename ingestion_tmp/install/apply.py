import os, shutil

def apply_bundle():
    base = os.getcwd()
    for folder in ["engine","tests"]:
        os.makedirs(os.path.join(base, folder), exist_ok=True)

    for f in os.listdir("install/engine"):
        shutil.copy(os.path.join("install/engine", f), os.path.join(base, "engine", f))

    for f in os.listdir("install/tests"):
        shutil.copy(os.path.join("install/tests", f), os.path.join(base, "tests", f))

if __name__ == "__main__":
    apply_bundle()
