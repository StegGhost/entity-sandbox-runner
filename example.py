
from stability_governor import StabilityGovernor

gov = StabilityGovernor()

receipt = gov.evaluate_and_commit(
    delta={"action":"test"},
    state={"balance":100},
    authority={"user":"rigel"},
    policy={"rule":"allow"}
)

print(receipt)
