def evaluate_spec(spec: dict):
    failures = []

    for section in ["Inputs", "Outputs", "Constraints", "Interfaces"]:
        value = spec.get(section, "")

        if not value or not value.strip():
            failures.append(section)

    return failures
