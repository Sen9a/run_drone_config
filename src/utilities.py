import time
from typing import Callable


def retry_read(number_of_retries: int):
    def argument_wrapper(fn: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            result = ''
            for i in range(number_of_retries):
                result_fn = fn(*args, **kwargs)
                if result_fn.endswith('#'):
                    result += result_fn
                    return result
                else:
                    result += result_fn
                    time.sleep(0.1)
        return wrapper
    return argument_wrapper

