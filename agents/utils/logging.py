import datetime

def log_audit(message: str):
    """
    Logs an audit message to the console with a timestamp.

    Args:
        message: The message to log.
    """
    timestamp = datetime.datetime.now().isoformat()
    print(f"[AUDIT] [{timestamp}] {message}")
