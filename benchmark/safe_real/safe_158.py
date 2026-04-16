# source: DjangoSafe / django/db/backends/sqlite3/_functions.py
# function: _sqlite_exp

def _sqlite_exp(x):
    if x is None:
        return None
    return exp(x)