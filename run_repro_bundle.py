import argparse
from reproducibility.bundle_builder import build_bundle

parser = argparse.ArgumentParser()
parser.add_argument("--results", required=True)
args = parser.parse_args()

bundle = build_bundle(args.results)
print("Bundle created:", bundle)
