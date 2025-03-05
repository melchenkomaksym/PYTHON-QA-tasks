import functools
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(time)s %(message)s')


def cache_decorator(enable_logging):
    cache = {}

    def decorator(func):
        @functools.wraps(func)
        def wrapper(n):
            if n in cache:
                if enable_logging:
                    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    logging.info(f"{current_time} Cache hit for number {n}")
                return cache[n]
            result = func(n)
            cache[n] = result
            return result
        return wrapper
    return decorator


@cache_decorator(True)
def factorial(n):
    if n < 2:
        return 1
    return factorial(n - 1) * n


# Test cases
print(factorial(3))  # Should calculate and print 6
print(factorial(3))  # Should print cache hit and 6
print(factorial(4))  # Should calculate and print 24, with cache hit for 3
