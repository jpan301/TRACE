# source: RedashSafe / redash/tasks/queries/execution.py
# function: _annotate_query

class QueryExecutor:
    def _annotate_query(self, query_runner):
        self.metadata["Job ID"] = self.job.id
        self.metadata["Query Hash"] = self.query_hash
        self.metadata["Scheduled"] = self.is_scheduled_query

        return query_runner.annotate_query(self.query, self.metadata)