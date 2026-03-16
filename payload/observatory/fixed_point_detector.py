
from observatory.contract import pipeline_contract

@pipeline_contract(
    name="fixed_point_detector",
    tier=3
)
def main():
    print("Running fixed_point_detector")
    return {"status": "ok"}

if __name__ == "__main__":
    main()
