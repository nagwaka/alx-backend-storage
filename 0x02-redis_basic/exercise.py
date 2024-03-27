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
        self.__redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store the input data in Redis using the random key and return the key.
        """
        rand_key = str(uuid.uuid4())
        self.__redis.set(rand_key, data)
        return rand_key

    def get(self, key: str, fn: Callable = None) -> Union[str,
                                                          bytes, int, None]:
        """
        take a key string argument and an optional Callable argument named fn
        """
        data = self.__redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(sel, key: str) -> Union[str, None]:
        """
        automatically parametrize Cache.get with the correc
        conversion function.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        automatically parametrize Cache.get with the correct
        conversion function.
        """
        return self.get(key, fn=int)
