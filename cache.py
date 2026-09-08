# cache.py
# Simple Redis cache wrapper for storing and retrieving JSON-serializable data.

import os
import json
import redis

# Redis connection URL from environment, default localhost
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Create Redis client (decode responses to strings)
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def cache_set(key: str, value, ttl: int = 60):
    """Store a value in Redis with a time-to-live (seconds)."""
    redis_client.setex(key, ttl, json.dumps(value))

def cache_get(key: str):
    """Retrieve a value from Redis; returns None if missing."""
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def cache_delete(key: str):
    """Delete a key from Redis."""
    redis_client.delete(key)