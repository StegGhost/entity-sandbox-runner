from install.engine.receipt_chain import append_receipt
from install.engine.admission_engine_v4 import admit_action
from install.engine.governed_passport import hash_passport

def execute_with_governance(passport, action, system_state, executor_fn):
    passport_hash = hash_passport(passport)

    admission = admit_action(passport, action, system_state)

    if not admission["allowed"]:
        return {
            "status": "rejected",
            "admission": admission
        }

    result = executor_fn(action)

    receipt = append_receipt(
        passport_hash=passport_hash,
        action=action,
        result={
            "result": result,
            "admission": admission
        }
    )

    return {
        "status": "executed",
        "result": result,
        "receipt": receipt
    }
