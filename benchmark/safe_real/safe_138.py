# source: RedashSafe / redash/handlers/queries.py
# function: get_queries

class BaseQueryListResource:
    def get_queries(self, search_term):
        if search_term:
            results = models.Query.search(
                search_term,
                self.current_user.group_ids,
                self.current_user.id,
                include_drafts=True,
                multi_byte_search=current_org.get_setting("multi_byte_search_enabled"),
            )
        else:
            results = models.Query.all_queries(self.current_user.group_ids, self.current_user.id, include_drafts=True)
        return filter_by_tags(results, models.Query.tags)