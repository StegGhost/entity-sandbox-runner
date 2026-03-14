from pathlib import Path
import yaml

def load_scenario(exp_path: Path) -> dict:
    config_file = exp_path / "config.yaml"
    if not config_file.exists():
        raise FileNotFoundError(config_file)
    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    def transition(state: dict) -> dict:
        a_next = state["a"] + config["delta_a"]
        g_next = max(0.0, state["g"] - config["g_decay"])
        c_next = state["c"]
        t_next = max(0.0, state["t"] - config["t_decay"])
        bound = (
            config["K"]
            * (g_next ** config["alpha"])
            * (c_next ** config["beta"])
            * (t_next ** config["gamma"])
        )
        return {
            "a_next": a_next,
            "g_next": g_next,
            "c_next": c_next,
            "t_next": t_next,
            "bound": bound,
            "K": config["K"],
            "alpha": config["alpha"],
            "beta": config["beta"],
            "gamma": config["gamma"],
        }

    return {
        "experiment_id": config.get("experiment_id", exp_path.name),
        "initial_state": config["initial_state"],
        "steps": config["steps"],
        "transition": transition,
    }
