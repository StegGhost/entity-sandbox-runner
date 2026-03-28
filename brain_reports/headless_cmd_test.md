# Headless Command Test Report

**Mode:** steggate_live_test
**Status:** ok
**Timestamp:** 2026-03-28T02:15:00.394122

## health
```json
{
  "ok": true,
  "status_code": 200,
  "data": {
    "status": "ok",
    "service": "steggate-api",
    "ts": 1774664124
  }
}
```

## token
```json
{
  "ok": true,
  "status_code": 200,
  "data": {
    "status": "ok",
    "token": "424796263e1e130c5ea3580b8784ed6dea0906fc473ed0fa0687fb198cb34c62",
    "expires_in": 120
  }
}
```

## execute
```json
{
  "ok": true,
  "status_code": 200,
  "data": {
    "status": "executed",
    "result": {
      "status_code": 200,
      "body": "{\n  \"args\": {}, \n  \"data\": \"{\\\"t\\\": 1}\", \n  \"files\": {}, \n  \"form\": {}, \n  \"headers\": {\n    \"Accept-Encoding\": \"identity\", \n    \"Content-Length\": \"8\", \n    \"Content-Type\": \"application/json\", \n    \"Host\": \"httpbin.org\", \n    \"User-Agent\": \"Python-urllib/3.11\", \n    \"X-Amzn-Trace-Id\": \"Root=1-69c739bd-19644d86530a7d8e40f3f92a\"\n  }, \n  \"json\": {\n    \"t\": 1\n  }, \n  \"origin\": \"74.220.48.248\", \n  \"url\": \"https://httpbin.org/post\"\n}\n"
    },
    "receipt": {
      "receipt_id": "07a420a8bc16ac62590a1dbc12631bab706d9f0ef34f14cb087fde57f90b821c",
      "timestamp": 1774664125,
      "target": "https://httpbin.org/post",
      "action_hash": "4834945f7bf91f82efc5cf881d902ec1cfa58f1be01cb35fe602b8ad4620c552",
      "result_hash": "08f0bed969413b7b455c0f80f0087104186e3a2a02bd1c30b80f01d2889c89bc",
      "policy_passed": true
    }
  }
}
```

## verify
```json
{
  "ok": true,
  "status_code": 200,
  "data": {
    "valid": true,
    "reason": "ok",
    "receipt_id": "07a420a8bc16ac62590a1dbc12631bab706d9f0ef34f14cb087fde57f90b821c"
  }
}
```

## artifacts
```json
{
  "json_report": "/home/runner/work/entity-sandbox-runner/entity-sandbox-runner/brain_reports/headless_cmd_test.json",
  "md_report": "/home/runner/work/entity-sandbox-runner/entity-sandbox-runner/brain_reports/headless_cmd_test.md"
}
```
