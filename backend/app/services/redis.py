from datetime import timedelta

import redis

# Connect to Redis
# In a real app, connection details should come from config
r = redis.Redis(host="localhost", port=6379, db=0)


def reserve_slot(
    slot_key: str, freelancer_id: str, duration: timedelta = timedelta(minutes=10)
):
    """
    Reserves a time slot for a freelancer for a given duration.
    Returns True if the slot was successfully reserved, False otherwise.
    """
    # The value can be anything, we're just using SET with NX option
    # which means "set only if the key does not already exist".
    return r.set(f"slot:{freelancer_id}:{slot_key}", "reserved", ex=duration, nx=True)


def release_slot(slot_key: str, freelancer_id: str):
    """Releases a reserved time slot."""
    r.delete(f"slot:{freelancer_id}:{slot_key}")
