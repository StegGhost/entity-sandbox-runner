
from observatory.contract import pipeline_contract

@pipeline_contract(
    name="experiment_scheduler_cluster",
    tier=3
)
def main():
    print("Running experiment_scheduler_cluster")
    return {"status": "ok"}

if __name__ == "__main__":
    main()
