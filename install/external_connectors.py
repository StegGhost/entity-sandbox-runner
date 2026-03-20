def execute_external(proposal: dict):
    name = proposal.get("name")

    if name == "file_write":
        with open("output.txt", "w") as f:
            f.write(str(proposal.get("payload")))
        return {"status": "file_written"}

    if name == "api_call":
        return {"status": "api_called"}

    return {"status": "noop"}
