# source: RedashSafe / redash/query_runner/__init__.py
# function: query_is_select_no_limit

class BaseSQLQueryRunner:
    def query_is_select_no_limit(self, query):
        parsed_query_list = sqlparse.parse(query)
        if len(parsed_query_list) == 0:
            return False
        parsed_query = parsed_query_list[0]
        last_keyword_idx = find_last_keyword_idx(parsed_query)
        # Either invalid query or query that is not select
        if last_keyword_idx == -1 or parsed_query.tokens[0].value.upper() != "SELECT":
            return False

        no_limit = parsed_query.tokens[last_keyword_idx].value.upper() not in self.limit_keywords

        return no_limit