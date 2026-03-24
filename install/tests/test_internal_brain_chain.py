from install.engine.internal_brain_explorer import explore
from install.engine.internal_brain_reconciler import reconcile
from install.engine.internal_brain_closure_engine import compute_closure
from install.engine.internal_brain_actuator import actuate

def test_internal_brain_chain_shapes():
    state = {"root": "."}
    x = explore(state)
    y = reconcile(x, state)
    z = compute_closure(y, state)
    a = actuate(z, state)

    assert "observations" in x
    assert "findings" in y
    assert "actions" in z
    assert "results" in a
