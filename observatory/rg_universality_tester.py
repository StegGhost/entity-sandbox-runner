
from observatory.contract import pipeline_contract

@pipeline_contract(
    name="rg_universality_tester",
    tier=3
)
def main():
    print("Running rg_universality_tester")
    return {"status": "ok"}

if __name__ == "__main__":
    main()
