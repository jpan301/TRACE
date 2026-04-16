# source: SentrySafe / src/sentry/integrations/bitbucket/integration.py
# function: get_repositories

class BitbucketIntegration:
    def get_repositories(
        self,
        query: str | None = None,
        page_number_limit: int | None = None,
        accessible_only: bool = False,
        use_cache: bool = False,
    ) -> list[RepositoryInfo]:
        username = self.model.metadata.get("uuid", self.username)
        if not query:
            all_repos = self.get_client().get_repos(username, page_number_limit=page_number_limit)
            return [
                {
                    "identifier": repo["full_name"],
                    "name": repo["full_name"],
                    "external_id": self.get_repo_external_id(repo),
                }
                for repo in all_repos
            ]

        client = self.get_client()
        exact_query = f'name="{query}"'
        fuzzy_query = f'name~"{query}"'
        exact_search_resp = client.search_repositories(username, exact_query)
        fuzzy_search_resp = client.search_repositories(username, fuzzy_query)

        seen: OrderedSet[str] = OrderedSet()
        repos: list[RepositoryInfo] = []
        for repo in chain(
            exact_search_resp.get("values", []),
            fuzzy_search_resp.get("values", []),
        ):
            if repo["full_name"] not in seen:
                seen.add(repo["full_name"])
                repos.append(
                    {
                        "identifier": repo["full_name"],
                        "name": repo["full_name"],
                        "external_id": self.get_repo_external_id(repo),
                    }
                )

        return repos