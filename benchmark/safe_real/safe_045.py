# source: RedashSafe / redash/query_runner/yandex_disk.py
# function: _get_tables

class YandexDisk:
    def _get_tables(self, schema):
        offset = 0
        limit = 100

        while True:
            tmp_response = self._send_query(
                "resources/public", media_type="spreadsheet,text", limit=limit, offset=offset
            )

            tmp_items = tmp_response["items"]

            for file_info in tmp_items:
                file_name = file_info["name"]
                file_path = file_info["path"].replace("disk:", "")

                file_extension = file_name.split(".")[-1].lower()
                if file_extension not in EXTENSIONS_READERS:
                    continue

                schema[file_name] = {"name": file_name, "columns": [file_path]}

            if len(tmp_items) < limit:
                break

            offset += limit

        return list(schema.values())