# Headless Command Test Report

**Mode:** steggate_live_test
**Status:** ok
**Timestamp:** 2026-03-28T04:45:41.030665

## health
```json
{
  "ok": true,
  "status_code": 200,
  "data": {
    "status": "ok",
    "service": "steggate-api",
    "ts": 1774673141
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
    "token": "4ae3990d22517a9e8e09928680f260fb7b6a553b898f1a4d6f03df5b4ec23fb3",
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
      "body": "{\n  \"args\": {}, \n  \"data\": \"{\\\"t\\\": 1}\", \n  \"files\": {}, \n  \"form\": {}, \n  \"headers\": {\n    \"Accept-Encoding\": \"identity\", \n    \"Content-Length\": \"8\", \n    \"Content-Type\": \"application/json\", \n    \"Host\": \"httpbin.org\", \n    \"User-Agent\": \"Python-urllib/3.11\", \n    \"X-Amzn-Trace-Id\": \"Root=1-69c75cf5-5e321dca1b85b06676904521\"\n  }, \n  \"json\": {\n    \"t\": 1\n  }, \n  \"origin\": \"74.220.48.248\", \n  \"url\": \"https://httpbin.org/post\"\n}\n"
    },
    "receipt": {
      "receipt_id": "f53021e6ffb03995bca8efb94383f6b7a26530a8950772514d0740b54240cfb2",
      "timestamp": 1774673141,
      "target": "https://httpbin.org/post",
      "action_hash": "4834945f7bf91f82efc5cf881d902ec1cfa58f1be01cb35fe602b8ad4620c552",
      "result_hash": "3b3e78de182ddfe2d0d31a88281a5a05a81b30ff08232cd67ef723c4b56dad9f",
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
    "receipt_id": "f53021e6ffb03995bca8efb94383f6b7a26530a8950772514d0740b54240cfb2"
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
