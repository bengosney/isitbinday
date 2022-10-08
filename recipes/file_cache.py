# Standard Library
import functools
import os
import pickle
from collections.abc import Callable
from hashlib import sha256
from tempfile import gettempdir


def file_cache(func: Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        hashed_key = sha256(pickle.dumps([args, kwargs], 0)).hexdigest()
        name = f"cache_{func.__name__}_{hashed_key}"
        cache_file_path = os.path.join(gettempdir(), name)

        try:
            with open(cache_file_path, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            pass
        except pickle.UnpicklingError:
            os.remove(cache_file_path)

        res = func(*args, **kwargs)

        with open(cache_file_path, "ab") as f:
            pickle.dump(res, f)

        return res

    return wrapper
