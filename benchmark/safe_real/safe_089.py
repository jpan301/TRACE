# source: RedashSafe / redash/query_runner/dgraph.py
# function: run_query

class Dgraph:
    def run_query(self, query, user):
        data = None
        error = None

        try:
            data = self.run_dgraph_query_raw(query)

            first_key = next(iter(list(data.keys())))
            first_node = data[first_key]

            data_to_be_processed = first_node

            processed_data = []
            header = []
            # use logic from https://github.com/vinay20045/json-to-csv
            for item in data_to_be_processed:
                reduced_item = {}
                reduce_item(reduced_item, first_key, item)

                header += reduced_item.keys()

                processed_data.append(reduced_item)

            header = list(set(header))

            columns = [{"name": c, "friendly_name": c, "type": "string"} for c in header]

            # finally, assemble both the columns and data
            data = {"columns": columns, "rows": processed_data}
        except Exception as e:
            error = e

        return data, error