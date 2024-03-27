#!/usr/bin/env python3
"""
Create a Cache class
"""
import redis
import uuid
from typing import Union, Callable


class Cache:
    """
    cache class for storing data into Redis db
    """
    def __init__(self) -> None:
        self.__redis = redis.Redis()
        self.__redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store the input data in Redis using the random key and return the key.
        """
        rand_key = str(uuid.uuid4())
        self.__redis.set(rand_key, data)
        return rand_key
