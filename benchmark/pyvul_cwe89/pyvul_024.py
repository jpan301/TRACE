def check_db_or_user_exists(db_name, db_user, config):
    with _create_pg_connection(config) as con:
        with con.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname='{}';".format(db_name))
            db_exists = cur.fetchone() is not None
            cur.execute("SELECT 1 FROM pg_roles WHERE rolname='{}';".format(db_user))
            user = cur.fetchone()
            user_exists = user is not None
            return db_exists or user_exists
