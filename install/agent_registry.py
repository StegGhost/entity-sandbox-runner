AGENTS = {}

def register_agent(agent_id, role="default"):
    AGENTS[agent_id] = {"role": role}

def get_agent(agent_id):
    return AGENTS.get(agent_id)
