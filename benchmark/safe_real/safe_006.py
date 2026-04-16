# source: DjangoSafe / django/db/backends/base/introspection.py
# function: get_names

class BaseDatabaseIntrospection:
        def get_names(cursor):
            return sorted(
                ti.name
                for ti in self.get_table_list(cursor)
                if include_views or ti.type == "t"
            )