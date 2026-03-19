from governed_executor import execute_proposal, resolver


def demo_execute():
    return {
        "message": "hello from governed execution",
        "ok": True
    }


def main():
    # Register a valid authority for the test
    resolver.register_authority(
        authority_id="local_admin",
        role="admin",
        trust_score=1.0
    )

    proposal = {
        "name": "demo_proposal",
        "authority_id": "local_admin",
        "execute": demo_execute,

        # Inputs for predictive_engine / u_signal_monitor
        "coherence": 1.0,
        "authority_validity": 1.0,
        "integrity": 1.0,
        "drift": 0.10,
        "resource_strain": 0.10,
        "entropy": 0.10
    }

    result = execute_proposal(proposal)
    print(result)


if __name__ == "__main__":
    main()
