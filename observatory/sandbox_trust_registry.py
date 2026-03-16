
from observatory.contract import pipeline_contract

@pipeline_contract(
    name="sandbox_trust_registry",
    tier=3
)
def main():
    print("Running sandbox_trust_registry")
    return {"status": "ok"}

if __name__ == "__main__":
    main()
