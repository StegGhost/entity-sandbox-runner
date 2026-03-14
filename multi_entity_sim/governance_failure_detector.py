def detect_failure(entities):

    failures = []

    for e in entities:

        if e.artifact_pressure > e.governance_capacity:
            failures.append(e)

    return failures
