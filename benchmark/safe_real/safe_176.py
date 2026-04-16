# source: SentrySafe / src/sentry/integrations/github/integration.py
# function: get_repositories

class GitHubIntegration:
    def get_repositories(
        self,
        query: str | None = None,
        page_number_limit: int | None = None,
        accessible_only: bool = False,
        use_cache: bool = False,
    ) -> list[RepositoryInfo]:
        """
        args:
        * query - a query to filter the repositories by
        * accessible_only - when True with a query, fetch only installation-
          accessible repos and filter locally instead of using the Search API
          (which may return repos outside the installation's scope)
        * use_cache - when True, serve repos from a short-lived cache instead
          of re-fetching all pages from GitHub on every call

        This fetches all repositories accessible to the Github App
        https://docs.github.com/en/rest/apps/installations#list-repositories-accessible-to-the-app-installation
        """
        client = self.get_client()

        def to_repo_info(raw_repos: Iterable[Mapping[str, Any]]) -> list[RepositoryInfo]:
            return [
                {
                    "name": i["name"],
                    "identifier": i["full_name"],
                    "external_id": self.get_repo_external_id(i),
                    "default_branch": i.get("default_branch"),
                }
                for i in raw_repos
            ]

        def _get_all_repos():
            if use_cache:
                return client.get_repos_cached()
            return client.get_repos(page_number_limit=page_number_limit)

        if not query:
            all_repos = _get_all_repos()
            return to_repo_info(r for r in all_repos if not r.get("archived"))

        if accessible_only:
            all_repos = _get_all_repos()
            query_lower = query.lower()
            return to_repo_info(
                r
                for r in all_repos
                if not r.get("archived") and query_lower in r["full_name"].lower()
            )

        assert not use_cache, "use_cache is not supported with the Search API path"
        full_query = build_repository_query(self.model.metadata, self.model.name, query)
        response = client.search_repositories(full_query)
        return to_repo_info(response.get("items", []))