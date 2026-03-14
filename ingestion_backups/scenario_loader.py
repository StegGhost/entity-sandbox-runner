import yaml

def load_scenario(exp_path):

    config_file = exp_path / "config.yaml"

    with open(config_file) as f:
        config = yaml.safe_load(f)

    def transition(state):

        return {
            "a_next": state["a"] + config["delta_a"],
            "g_next": state["g"] - config["g_decay"],
            "c_next": state["c"],
            "t_next": state["t"] - config["t_decay"],
        }

    return {
        "initial_state": config["initial_state"],
        "steps": config["steps"],
        "delta_a": config["delta_a"],
        "K": config["K"],
        "alpha": config["alpha"],
        "beta": config["beta"],
        "gamma": config["gamma"],
        "transition": transition,
    }