# source: RedashSafe / redash/query_runner/mongodb.py
# function: _flatten

class DummyClass:
    def _flatten(x, name=""):
        if isinstance(x, dict):
            for k, v in x.items():
                _flatten(v, "{}.{}".format(name, k))
        elif isinstance(x, list):
            for idx, item in enumerate(x):
                _flatten(item, "{}.{}".format(name, idx))
        else:
            res[name[1:]] = x