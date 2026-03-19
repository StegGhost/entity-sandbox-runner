def compute_u(proposal):
    """
    Basic U-signal calculation

    U = (C * A * I) / (D + R + E)
    """

    C = float(proposal.get("coherence", 1.0))
    A = float(proposal.get("authority_validity", 1.0))
    I = float(proposal.get("integrity", 1.0))

    D = float(proposal.get("drift", 0.1))
    R = float(proposal.get("resource_strain", 0.1))
    E = float(proposal.get("entropy", 0.1))

    denominator = D + R + E

    if denominator == 0:
        return 1.0

    return (C * A * I) / denominator
