#!/usr/bin/env python3
"""
A module that uses the requests module to obtain the HTML content
of a particular URL and returns it
"""
import requests
import redis
import time
from typing import Callable

# Redis connection
redis = redis.Redis()


def cache_page(expiration_time: int) -> Callable:
    """
    Decorator to cache the result of a function with
    a specified expiration time.
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(url: str) -> str:
            # Check if the content is cached
            cached_content = redis.get(f"page:{url}")
            if cached_content:
                print("Content retrieved from cache")
                return cached_content.decode('utf-8')

            # If not cached, fetch content from URL
            content = func(url)

            # Cache the content with expiration time
            redis.setex(f"page:{url}", expiration_time, content)
            print("Content cached")

            return content
        return wrapper
    return decorator


@cache_page(expiration_time=10)
def get_page(url: str) -> str:
    """
    Obtains the HTML content of a particular URL.
    """
    response = requests.get(url)
    return response.text
