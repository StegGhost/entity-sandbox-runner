
def drift(u_history):
    if len(u_history)<5: return 0
    return u_history[-1]-u_history[0]
