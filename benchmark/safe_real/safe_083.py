# source: RedashSafe / redash/query_runner/json_ds.py
# function: _apply_path_search

def _apply_path_search(response, path, default=None):
    if path is None:
        return response

    path_parts = path.split(".")
    path_parts.reverse()
    while len(path_parts) > 0:
        current_path = path_parts.pop()
        if current_path in response:
            response = response[current_path]
        elif default is not None:
            return default
        else:
            raise Exception("Couldn't find path {} in response.".format(path))

    return response