from pathlib import Path
import shutil


def actuate(closure_output, state):
    results = []
    root = Path(state["root"])

    for action in closure_output.get("actions", []):
        name = action.get("action")
        targets = action.get("targets", [])

        if name == "inspect_failed_bundles":
            processed = []

            for rel_path in targets:
                src = root / rel_path

                if not src.exists():
                    continue

                # Move failed bundle → incoming for retry
                dest = root / "incoming_bundles" / src.name
                dest.parent.mkdir(parents=True, exist_ok=True)

                shutil.copy2(src, dest)

                processed.append(str(dest.relative_to(root)))

            results.append({
                "action": name,
                "status": "executed",
                "moved_to_incoming": processed,
                "count": len(processed)
            })

        else:
            results.append({
                "action": name,
                "status": "unknown_action",
                "targets": targets
            })

    return {
        "mode": "active",
        "summary": "Actuator executed actions",
        "results": results
    }
