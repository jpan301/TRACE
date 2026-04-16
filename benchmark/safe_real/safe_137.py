# source: RedashSafe / redash/monitor.py
# function: get_db_sizes

def get_db_sizes():
    database_metrics = []
    queries = [
        [
            "Query Results Size",
            "select pg_total_relation_size('query_results') as size from (select 1) as a",
        ],
        ["Redash DB Size", "select pg_database_size(current_database()) as size"],
    ]
    for query_name, query in queries:
        result = db.session.execute(query).first()
        database_metrics.append([query_name, result[0]])

    return database_metrics