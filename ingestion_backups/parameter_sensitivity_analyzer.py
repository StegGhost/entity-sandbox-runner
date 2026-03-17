
from observatory.contract import pipeline_contract

@pipeline_contract(
    name="parameter_sensitivity_analyzer",
    tier=3
)
def main():
    print("Running parameter_sensitivity_analyzer")
    return {"status": "ok"}

if __name__ == "__main__":
    main()
