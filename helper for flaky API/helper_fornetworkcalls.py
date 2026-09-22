import time
from functools import wraps

def retry(tries=3, delay=1, exceptions=(Exception,)):
    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            for attempt in range(tries):
                try:
                    return fn(*args, **kwargs)
                except exceptions:
                    if attempt == tries - 1:
                        raise
                    time.sleep(delay * 2 ** attempt)
        return wrapped
    return decorator

attempts = 0

@retry(tries=4, delay=0.5)
def fetch_data():
    global attempts
    attempts += 1
    if attempts < 3:
        raise ConnectionError("Temporary failure")
    return "Data fetched successfully!"

print(fetch_data())
