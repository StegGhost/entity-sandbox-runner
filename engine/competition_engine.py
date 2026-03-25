
def rank_agents(agent_stats):
    return sorted(agent_stats, key=lambda x: x['roi'], reverse=True)
