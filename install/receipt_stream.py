import time
import json

RECEIPT_LOG = []

def emit_receipt(event: dict):
    entry = {
        "timestamp": time.time(),
        "event": event
    }
    RECEIPT_LOG.append(entry)

def get_receipts():
    return RECEIPT_LOG
