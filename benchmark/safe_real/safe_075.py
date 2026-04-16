# source: SentrySafe / src/sentry/sentry_metrics/querying/data/postprocessing/base.py
# function: run

class PostProcessingStep:
    def run(self, query_results: list[QueryResult]) -> list[QueryResult]:
        """
        Runs the post-processing steps on a list of query results.

        Returns:
            A list of post-processed query results.
        """
        raise NotImplementedError