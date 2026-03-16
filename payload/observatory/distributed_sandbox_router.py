
from observatory.contract import pipeline_contract

@pipeline_contract(
    name="distributed_sandbox_router",
    tier=3
)
def main():
    print("Running distributed_sandbox_router")
    return {"status": "ok"}

if __name__ == "__main__":
    main()
