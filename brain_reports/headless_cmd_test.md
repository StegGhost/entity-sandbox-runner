# Headless Command Test Report

**Mode:** steggate_live_test
**Status:** ok
**Timestamp:** 2026-03-28T04:01:24.401461

## health
```json
{
  "ok": true,
  "status_code": 200,
  "data": {
    "status": "ok",
    "service": "steggate-api",
    "ts": 1774670484
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
    "token": "f42b059eace3b7128d034588bad5364ee57394a0a361a4b5c43e2f2755fa0ff4",
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
      "body": "{\n  \"args\": {}, \n  \"data\": \"{\\\"t\\\": 1}\", \n  \"files\": {}, \n  \"form\": {}, \n  \"headers\": {\n    \"Accept-Encoding\": \"identity\", \n    \"Content-Length\": \"8\", \n    \"Content-Type\": \"application/json\", \n    \"Host\": \"httpbin.org\", \n    \"User-Agent\": \"Python-urllib/3.11\", \n    \"X-Amzn-Trace-Id\": \"Root=1-69c75295-068357f80ec45329322f3100\"\n  }, \n  \"json\": {\n    \"t\": 1\n  }, \n  \"origin\": \"74.220.48.248\", \n  \"url\": \"https://httpbin.org/post\"\n}\n"
    },
    "receipt": {
      "receipt_id": "52acf6e9c5644eb0cadb5c0cfb3ae68b4165acfd47c824c7a844fbb7bfabc3c9",
      "timestamp": 1774670485,
      "target": "https://httpbin.org/post",
      "action_hash": "4834945f7bf91f82efc5cf881d902ec1cfa58f1be01cb35fe602b8ad4620c552",
      "result_hash": "c85a8d5039a758b980743670df923f1365744332e658652796084ee8065d5d68",
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
    "receipt_id": "52acf6e9c5644eb0cadb5c0cfb3ae68b4165acfd47c824c7a844fbb7bfabc3c9"
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
