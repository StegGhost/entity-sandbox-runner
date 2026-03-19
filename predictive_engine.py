from u_signal_monitor import compute_u

def simulate_future_u(proposal, steps=3):
    u_values = []

    simulated = proposal.copy()

    for _ in range(steps):
        u = compute_u(simulated)
        u_values.append(u)

        # naive forward drift
        simulated["drift"] = simulated.get("drift", 0) + 0.05

    return u_values

def is_future_stable(u_values, threshold=0.5):
    return all(u > threshold for u in u_values)
