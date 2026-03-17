def should_retry(attempts, max_attempts=3):
    return attempts < max_attempts
