# source: DjangoSafe / django/db/models/sql/compiler.py
# function: __init__

class SQLCompiler:
    def __init__(self, query, connection, using, elide_empty=True):
        self.query = query
        self.connection = connection
        self.using = using
        # Some queries, e.g. coalesced aggregation, need to be executed even if
        # they would return an empty result set.
        self.elide_empty = elide_empty
        self.quote_cache = {"*": "*"}
        # The select, klass_info, and annotations are needed by
        # QuerySet.iterator() these are set as a side-effect of executing the
        # query. Note that we calculate separately a list of extra select
        # columns needed for grammatical correctness of the query, but these
        # columns are not included in self.select.
        self.select = None
        self.annotation_col_map = None
        self.klass_info = None
        self._meta_ordering = None