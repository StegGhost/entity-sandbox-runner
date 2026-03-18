
def detect_anomaly(history):
    if len(history)<5: return False
    avg=sum(history)/len(history)
    return abs(history[-1]-avg) > 0.25
