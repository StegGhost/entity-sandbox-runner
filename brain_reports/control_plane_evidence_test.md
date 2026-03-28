# Control Plane Evidence Test Report

**Timestamp:** 2026-03-28T04:47:17
**Status:** partial
**Reason:** some_checks_failed:tvc_check_signed_quorum,tvc_check_distributed_quorum

## file inventory
```json
{
  "control_plane_tvc_files": [
    "control_plane/tvc/README.md",
    "control_plane/tvc/bind_receipt.py",
    "control_plane/tvc/check_distributed_quorum.py",
    "control_plane/tvc/check_quorum.py",
    "control_plane/tvc/check_signed_quorum.py",
    "control_plane/tvc/crypto_utils.py",
    "control_plane/tvc/distributed_quorum.json",
    "control_plane/tvc/issue_token.py",
    "control_plane/tvc/keys/guardian_a.sk",
    "control_plane/tvc/policy.json",
    "control_plane/tvc/quorum_signals.json",
    "control_plane/tvc/signed_quorum.json",
    "control_plane/tvc/verify_bundle_install.py",
    "control_plane/tvc/verify_token.py"
  ],
  "control_plane_tc_files": [
    "control_plane/tc/README.md",
    "control_plane/tc/bundle_install.tc.json",
    "control_plane/tc/public_keys.json",
    "control_plane/tc/verify_receipt.py"
  ],
  "promote_to_main": {
    "path": "/home/runner/work/entity-sandbox-runner/entity-sandbox-runner/install/engine/promote_to_main.py",
    "exists": true,
    "size": 1978,
    "mtime": 1774673231.2510746
  }
}
```

## required artifacts
```json
{
  "json_report": "/home/runner/work/entity-sandbox-runner/entity-sandbox-runner/brain_reports/control_plane_evidence_test.json",
  "md_report": "/home/runner/work/entity-sandbox-runner/entity-sandbox-runner/brain_reports/control_plane_evidence_test.md",
  "headless_cmd_test_json": "/home/runner/work/entity-sandbox-runner/entity-sandbox-runner/brain_reports/headless_cmd_test.json",
  "tvc_token_json": "/home/runner/work/entity-sandbox-runner/entity-sandbox-runner/brain_reports/tvc_token.json",
  "tvc_receipt_binding_json": "/home/runner/work/entity-sandbox-runner/entity-sandbox-runner/brain_reports/tvc_receipt_binding.json"
}
```

## python_dependency_pynacl

- ok: `True`
- returncode: `0`
- duration: `0.011`

### command
```bash
python -c import nacl; print('PYNACL_OK')
```

### stdout
```
PYNACL_OK
```

### stderr
```

```

## tvc_issue_token

- ok: `True`
- returncode: `0`
- duration: `0.027`

### command
```bash
python control_plane/tvc/issue_token.py
```

### stdout
```
{
  "status": "ok",
  "output": "/home/runner/work/entity-sandbox-runner/entity-sandbox-runner/brain_reports/tvc_token.json"
}
```

### stderr
```

```

## tvc_verify_token

- ok: `True`
- returncode: `0`
- duration: `0.024`

### command
```bash
python control_plane/tvc/verify_token.py
```

### stdout
```
{
  "status": "valid",
  "scope": "promotion_to_main"
}
```

### stderr
```

```

## tvc_check_signed_quorum

- ok: `False`
- returncode: `1`
- duration: `0.08`

### command
```bash
python control_plane/tvc/check_signed_quorum.py
```

### stdout
```

```

### stderr
```
Traceback (most recent call last):
  File "/home/runner/work/entity-sandbox-runner/entity-sandbox-runner/control_plane/tvc/check_signed_quorum.py", line 36, in <module>
    main()
  File "/home/runner/work/entity-sandbox-runner/entity-sandbox-runner/control_plane/tvc/check_signed_quorum.py", line 23, in main
    if verify_signature(s["signer"], payload, s["signature"]):
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/entity-sandbox-runner/entity-sandbox-runner/control_plane/tvc/crypto_utils.py", line 32, in verify_signature
    vk = load_public(name)
         ^^^^^^^^^^^^^^^^^
  File "/home/runner/work/entity-sandbox-runner/entity-sandbox-runner/control_plane/tvc/crypto_utils.py", line 17, in load_public
    return VerifyKey(path.read_text().strip(), encoder=HexEncoder)
                     ^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/pathlib.py", line 1058, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors) as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/pathlib.py", line 1044, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/home/runner/work/entity-sandbox-runner/entity-sandbox-runner/control_plane/tvc/keys/guardian_a.pk'
```

## tvc_check_distributed_quorum

- ok: `False`
- returncode: `1`
- duration: `0.072`

### command
```bash
python control_plane/tvc/check_distributed_quorum.py
```

### stdout
```
{
  "status": "invalid",
  "reason": "distributed_quorum_not_met"
}
```

### stderr
```

```

## headless_cmd_test

- ok: `True`
- returncode: `0`
- duration: `0.959`

### command
```bash
python install/engine/headless_cmd_tester.py --mode steggate_live_test
```

### stdout
```
{
  "mode": "steggate_live_test",
  "ts": "2026-03-28T04:47:18.178423",
  "status": "ok",
  "steps": {
    "health": {
      "ok": true,
      "status_code": 200,
      "data": {
        "status": "ok",
        "service": "steggate-api",
        "ts": 1774673238
      }
    },
    "token": {
      "ok": true,
      "status_code": 200,
      "data": {
        "status": "ok",
        "token": "ec2e8e291ba77a6170aa4389234bea7fb450b50fdb95f4f326d61839a85c6cc9",
        "expires_in": 120
      }
    },
    "execute": {
      "ok": true,
      "status_code": 200,
      "data": {
        "status": "executed",
        "result": {
          "status_code": 200,
          "body": "{\n  \"args\": {}, \n  \"data\": \"{\\\"t\\\": 1}\", \n  \"files\": {}, \n  \"form\": {}, \n  \"headers\": {\n    \"Accept-Encoding\": \"identity\", \n    \"Content-Length\": \"8\", \n    \"Content-Type\": \"application/json\", \n    \"Host\": \"httpbin.org\", \n    \"User-Agent\": \"Python-urllib/3.11\", \n    \"X-Amzn-Trace-Id\": \"Root=1-69c75d56-5107355847f8f97d0bcf03c8\"\n  }, \n  \"json\": {\n    \"t\": 1\n  }, \n  \"origin\": \"74.220.48.248\", \n  \"url\": \"https://httpbin.org/post\"\n}\n"
        },
        "receipt": {
          "receipt_id": "ce2f7516649ff33db023a548e74bc85d5c853afac65105e90834d74733c2e2c7",
          "timestamp": 1774673238,
          "target": "https://httpbin.org/post",
          "action_hash": "4834945f7bf91f82efc5cf881d902ec1cfa58f1be01cb35fe602b8ad4620c552",
          "result_hash": "bef23da184e375024cf1112622d34a094b513514df2d15765f4ef395d01bc861",
          "policy_passed": true
        }
      }
    },
    "verify": {
      "ok": true,
      "status_code": 200,
      "data": {
        "valid": true,
        "reason": "ok",
        "receipt_id": "ce2f7516649ff33db023a548e74bc85d5c853afac65105e90834d74733c2e2c7"
      }
    }
  },
  "artifacts": {
    "json_report": "/home/runner/work/entity-sandbox-runner/entity-sandbox-runner/brain_reports/headless_cmd_test.json",
    "md_report": "/home/runner/work/entity-sandbox-runner/entity-sandbox-runner/brain_reports/headless_cmd_test.md"
  }
}
```

### stderr
```

```

## tc_verify_receipt

- ok: `True`
- returncode: `0`
- duration: `0.027`

### command
```bash
python control_plane/tc/verify_receipt.py
```

### stdout
```
{
  "status": "ok",
  "receipt_id": "ce2f7516649ff33db023a548e74bc85d5c853afac65105e90834d74733c2e2c7"
}
```

### stderr
```

```

## tvc_bind_receipt

- ok: `True`
- returncode: `0`
- duration: `0.027`

### command
```bash
python control_plane/tvc/bind_receipt.py
```

### stdout
```
{
  "status": "ok",
  "output": "/home/runner/work/entity-sandbox-runner/entity-sandbox-runner/brain_reports/tvc_receipt_binding.json"
}
```

### stderr
```

```

## promote_to_main

- ok: `True`
- returncode: `0`
- duration: `0.121`

### command
```bash
python install/engine/promote_to_main.py
```

### stdout
```
{
  "status": "rejected",
  "reason": "signed_quorum_failed"
}
```

### stderr
```

```
