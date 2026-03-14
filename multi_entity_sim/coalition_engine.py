def form_coalitions(entities):

    coalitions = []

    for e in entities:
        if e.trust > 0.7:
            coalitions.append([e])

    return coalitions
