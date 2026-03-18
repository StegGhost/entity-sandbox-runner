
def arbitrate(local, consensus, anomaly):
    if anomaly:
        return "restrict","anomaly_override"
    if consensus!=local:
        return consensus,"consensus_override"
    return local,"local"
