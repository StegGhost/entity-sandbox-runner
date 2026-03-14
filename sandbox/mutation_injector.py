import random


def inject_mutation(state):

    if random.random() < 0.2:

        state["a"] += random.uniform(0.5, 1.5)

    return state
