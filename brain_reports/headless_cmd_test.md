# Headless Command Test Report

**Mode:** steggate_live_test
**Status:** ok
**Timestamp:** 2026-03-28T03:52:45.801073

## health
```json
{
  "ok": true,
  "status_code": 200,
  "data": {
    "status": "ok",
    "service": "steggate-api",
    "ts": 1774669966
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
    "token": "0c989d9ff00c4423d305364e525249040196922dc4766bf22f7f9ef2fd3678d5",
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
      "body": "{\n  \"args\": {}, \n  \"data\": \"{\\\"t\\\": 1}\", \n  \"files\": {}, \n  \"form\": {}, \n  \"headers\": {\n    \"Accept-Encoding\": \"identity\", \n    \"Content-Length\": \"8\", \n    \"Content-Type\": \"application/json\", \n    \"Host\": \"httpbin.org\", \n    \"User-Agent\": \"Python-urllib/3.11\", \n    \"X-Amzn-Trace-Id\": \"Root=1-69c7508f-283d674027ee82e16d7d9f8f\"\n  }, \n  \"json\": {\n    \"t\": 1\n  }, \n  \"origin\": \"74.220.48.248\", \n  \"url\": \"https://httpbin.org/post\"\n}\n"
    },
    "receipt": {
      "receipt_id": "847e0073c48032feed1325bb9e5d50efe5a81bf0ef792a1a21d2f9c1b76290ab",
      "timestamp": 1774669967,
      "target": "https://httpbin.org/post",
      "action_hash": "4834945f7bf91f82efc5cf881d902ec1cfa58f1be01cb35fe602b8ad4620c552",
      "result_hash": "1322d79d8f62d9f10aa06c38014fe238a11811614274ff38ca9189e171c57da3",
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
    "receipt_id": "847e0073c48032feed1325bb9e5d50efe5a81bf0ef792a1a21d2f9c1b76290ab"
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
