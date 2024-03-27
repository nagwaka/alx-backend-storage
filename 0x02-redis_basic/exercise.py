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
    def __init__(self):
        self.__redis = redis.Redis()
        self.__redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        rand_key = str(uuid.uuid4())
        self.__redis.set(rand_key, data)
        return rand_key

    def get(self, key: str, fn: Callable = None) -> Union[str,
                                                          bytes, int, None]:
        data = self.__redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(sel, key: str) -> Union[str, None]:
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, fn=int)
