# source: RedashSafe / redash/query_runner/query_results.py
# function: create_tables_from_query_ids

def create_tables_from_query_ids(user, connection, query_ids, query_params, cached_query_ids=[]):
    for query_id in set(cached_query_ids):
        results = get_query_results(user, query_id, True)
        table_name = "cached_query_{query_id}".format(query_id=query_id)
        create_table(connection, table_name, results)

    for query in set(query_params):
        results = get_query_results(user, query[0], False, query[1])
        table_hash = hashlib.md5(
            "query_{query}_{hash}".format(query=query[0], hash=query[1]).encode(), usedforsecurity=False
        ).hexdigest()
        table_name = "query_{query_id}_{param_hash}".format(query_id=query[0], param_hash=table_hash)
        create_table(connection, table_name, results)

    for query_id in set(query_ids):
        results = get_query_results(user, query_id, False)
        table_name = "query_{query_id}".format(query_id=query_id)
        create_table(connection, table_name, results)