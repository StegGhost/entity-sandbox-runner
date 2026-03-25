
GLOBAL_STATE = {}

def register(node_id, state):
    GLOBAL_STATE[node_id] = state

def get_state(node_id):
    return GLOBAL_STATE.get(node_id)

def all_states():
    return GLOBAL_STATE
