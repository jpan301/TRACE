# source: SentrySafe / src/sentry/integrations/bitbucket_server/utils.py
# function: build_raw

class BitbucketServerAPIPath:
    def build_raw(project: str, repo: str, path: str, sha: str | None) -> str:
        project = quote(project)
        repo = quote(repo)

        params = {}
        if sha:
            params["at"] = sha

        return f"/projects/{project}/repos/{repo}/raw/{path}?{urlencode(params)}"