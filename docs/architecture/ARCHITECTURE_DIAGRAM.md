# Architecture Diagram

```text
                StegVerse-SDK
                      │
                      ▼
                trust-kernel
                      │
           ┌──────────┼──────────┐
           ▼          ▼          ▼
     control_plane security_plane policy_engine
           │
           ▼
     execution_plane
           │
           ▼
      evidence_plane
           │
           ▼
    observation_plane

 optional extension planes:
 simulation_plane
 cluster_plane
 federation_plane
 service_plane
```

## Repository relationship

```text
StegVerse-org/
├── StegVerse-SDK
├── trust-kernel
├── demo_ingest_engine
├── demo_suite_runner
└── StegVerse-demo-suite

StegGhost/
├── entity-sandbox-runner
├── stegverse_sandbox
└── ghost-pat-lab
```
