#!/usr/bin/env python3
"""
Create a Cache class
"""
import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        self.__redis = redis.Redis()
        self.__redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        rand_key = str(uuid.uuid4())
        self.__redis.set(rand_key, data)
        return rand_key
