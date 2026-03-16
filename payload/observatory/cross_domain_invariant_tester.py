
from observatory.contract import pipeline_contract

@pipeline_contract(
    name="cross_domain_invariant_tester",
    tier=3
)
def main():
    print("Running cross_domain_invariant_tester")
    return {"status": "ok"}

if __name__ == "__main__":
    main()
