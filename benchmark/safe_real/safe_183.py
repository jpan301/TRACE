# source: RedashSafe / redash/query_runner/corporate_memory.py
# function: run_query

class CorporateMemoryQueryRunner:
    def run_query(self, query, user):
        """send a sparql query to corporate memory"""
        query_text = query
        logger.info("about to execute query (user='{}'): {}".format(user, query_text))
        query = SparqlQuery(query_text)
        query_type = query.get_query_type()
        # type of None means, there is an error in the query
        # so execution is at least tried on endpoint
        if query_type not in ["SELECT", None]:
            raise ValueError("Queries of type {} can not be processed by redash.".format(query_type))

        self._setup_environment()
        try:
            data = self._transform_sparql_results(query.get_results())
        except Exception as error:
            logger.info("Error: {}".format(error))
            try:
                # try to load Problem Details for HTTP API JSON
                details = json.loads(error.response.text)
                error = ""
                if "title" in details:
                    error += details["title"] + ": "
                if "detail" in details:
                    error += details["detail"]
                    return None, error
            except Exception:
                pass

            return None, error

        error = None
        return data, error