
import json
def load_policy():
    return json.load(open("config/policy.json"))

def enforce_policy(policy,state,u):
    if u < policy["hard_min_u"]:
        return "restrict","hard"
    return "allow","ok"
