# Headless Command Test Report

**Mode:** steggate_live_test
**Status:** ok
**Timestamp:** 2026-03-28T01:32:56.431773

## health
```json
{
  "ok": true,
  "status_code": 200,
  "data": {
    "status": "ok",
    "service": "steggate-api",
    "ts": 1774661597
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
    "token": "27bcb423cdf1e9e7747e30e243c0a369b27e19f9ae4e85e8e7ff01ff32e0b7cc",
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
      "body": "{\n  \"args\": {}, \n  \"data\": \"{\\\"t\\\": 1}\", \n  \"files\": {}, \n  \"form\": {}, \n  \"headers\": {\n    \"Accept-Encoding\": \"identity\", \n    \"Content-Length\": \"8\", \n    \"Content-Type\": \"application/json\", \n    \"Host\": \"httpbin.org\", \n    \"User-Agent\": \"Python-urllib/3.11\", \n    \"X-Amzn-Trace-Id\": \"Root=1-69c72fde-538ebbc737328f621e86bddf\"\n  }, \n  \"json\": {\n    \"t\": 1\n  }, \n  \"origin\": \"74.220.48.248\", \n  \"url\": \"https://httpbin.org/post\"\n}\n"
    },
    "receipt": {
      "receipt_id": "22cb80ba517d6915e388df7ebf90252b961188595121c46c4980e445e7c27815",
      "timestamp": 1774661598,
      "target": "https://httpbin.org/post",
      "action_hash": "4834945f7bf91f82efc5cf881d902ec1cfa58f1be01cb35fe602b8ad4620c552",
      "result_hash": "a1a51218dbb09a9190cb15b1bfaa8fcb7aae419e33596002e746cf1ad1863c5d",
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
    "receipt_id": "22cb80ba517d6915e388df7ebf90252b961188595121c46c4980e445e7c27815"
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
