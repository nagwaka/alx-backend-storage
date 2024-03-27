#!/usr/bin/env python3
"""
Create a Cache class
"""
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that takes a single method Callable argument and
    returns a Callable.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Increments the count for that key every time the method is
        called and returns the value returned by the original method
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for
    a particular function in Redis.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Wrapper function to append input arguments and output values
        to Redis lists.
        """
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        # Append input arguments to Redis list
        self._redis.rpush(input_key, str(args))

        # Execute the wrapped function to retrieve the output
        output = method(self, *args, **kwargs)

        # Append the output value to Redis list
        self._redis.rpush(output_key, str(output))

        return output

    return wrapper


def replay(method: Callable) -> None:
    """
    Displays the history of calls of a particular function.
    """
    method_name = method.__qualname__
    inputs_key = method_name + ":inputs"
    outputs_key = method_name + ":outputs"

    # Retrieve input and output lists from Redis
    inputs = redis_instance.lrange(inputs_key, 0, -1)
    outputs = redis_instance.lrange(outputs_key, 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")
    for inp, out in zip(inputs, outputs):
        print(f"{method_name}
              (*{inp.decode('utf-8')}) -> {out.decode('utf-8')}")


class Cache:
    """
    Cache class for storing data into Redis db
    """
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using the random key and return the key.
        """
        rand_key = str(uuid.uuid4())
        self._redis.set(rand_key, data)
        return rand_key

    def get(self, key: str, fn: Callable = None) -> Union[str,
                                                          bytes, int, None]:
        """
        Retrives a value Redis
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Automatically parametrize Cache.get with the correc
        conversion function.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Automatically parametrize Cache.get with the correct
        conversion function.
        """
        return self.get(key, fn=int)
