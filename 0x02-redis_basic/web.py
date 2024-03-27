#!/usr/bin/env python3
"""
Implements an expiring web cache and tracker
"""
import redis
import requests
from functools import wraps
from typing import Callable


redis = redis.Redis()


def catch_page(method: Callable) -> Callable:
    """
    Cache the result of a function
    """
    @wraps(method)
    def wrapper(url) -> str:
        """
        Check if the content is cached
        """
        redis.incr(f'count:{url}')
        result = redis.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis.set(f'count:{url}', 0)
        redis.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Obtains the HTML content of a particular URL.
    """
    return requests.get(url).text
