def create_postgres_db(connection_dict, config):
    if check_db_or_user_exists(connection_dict["db_name"], connection_dict["db_username"], config):
        raise ValueError("db or user already exists")
    with _create_pg_connection(config) as con:
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with con.cursor() as cur:
            create_role = "CREATE USER {db_username} WITH PASSWORD '{db_pwd}';".format(**connection_dict)
            drop_role = "DROP ROLE {db_username};".format(**connection_dict)
            grant_role = 'GRANT {db_username} TO "{postgraas_user}";'.format(
                db_username=connection_dict['db_username'], postgraas_user=get_normalized_username(config['username'])
            )
            create_database = "CREATE DATABASE {db_name} OWNER {db_username};".format(**connection_dict)
            try:
                cur.execute(create_role)
                cur.execute(grant_role)
            except psycopg2.ProgrammingError as e:
                raise ValueError(e.args[0])
            # cleanup role in case database creation fails
            # saidly 'CREATE DATABASE' cannot run inside a transaction block
            try:
                cur.execute(create_database)
            except psycopg2.ProgrammingError as e:
                cur.execute(drop_role)
                raise ValueError(e.args[0])
