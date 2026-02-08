import time
import sqlite3
from functools import wraps

def sqlite_retry_on_locked(max_retries=5, initial_delay=0.2, backoff=2):
    """
    Décorateur pour réessayer une opération si la base SQLite est temporairement verrouillée (persistence is locked).
    max_retries : nombre maximal de tentatives
    initial_delay : délai initial en secondes
    backoff : multiplicateur pour le délai (exponentiel)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            delay = initial_delay
            for attempt in range(1, max_retries + 1):
                try:
                    return func(self, *args, **kwargs)
                except sqlite3.OperationalError as e:
                    self.db.rollback()
                    if "persistence is locked" in str(e):
                        if attempt == max_retries:
                            raise
                        time.sleep(delay)
                        delay *= backoff
                        continue
                    raise
        return wrapper
    return decorator

