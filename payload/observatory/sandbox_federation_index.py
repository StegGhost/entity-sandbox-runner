
from observatory.contract import pipeline_contract

@pipeline_contract(
    name="sandbox_federation_index",
    tier=3
)
def main():
    print("Running sandbox_federation_index")
    return {"status": "ok"}

if __name__ == "__main__":
    main()
