def propagate_trust(network):

    for entity in network:

        for neighbor in entity.neighbors:

            if entity.trust < 0.5:
                neighbor.trust *= 0.98
