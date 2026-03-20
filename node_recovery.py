import shutil


def recover_node(source_node: str, target_node: str):
    shutil.rmtree(target_node, ignore_errors=True)
    shutil.copytree(source_node, target_node)

    return {
        "status": "recovered",
        "source": source_node,
        "target": target_node,
    }
