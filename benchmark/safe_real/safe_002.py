# source: SentrySafe / src/sentry/integrations/bitbucket/client.py
# function: get_repos

class BitbucketApiClient:
    def get_repos(
        self, username: str, page_number_limit: int | None = None
    ) -> list[dict[str, Any]]:
        return self._get_all_from_paginated(
            BitbucketAPIPath.repositories.format(username=username),
            page_number_limit=page_number_limit,
        )