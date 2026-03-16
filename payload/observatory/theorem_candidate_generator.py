
from observatory.contract import pipeline_contract

@pipeline_contract(
    name="theorem_candidate_generator",
    tier=3
)
def main():
    print("Running theorem_candidate_generator")
    return {"status": "ok"}

if __name__ == "__main__":
    main()
