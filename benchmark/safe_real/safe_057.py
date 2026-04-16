# source: SentrySafe / src/sentry/integrations/github/integration.py
# function: format_source_url

class GitHubIntegration:
    def format_source_url(self, repo: Repository, filepath: str, branch: str | None) -> str:
        # Must format the url ourselves since `check_file` is a head request
        # "https://github.com/octokit/octokit.rb/blob/master/README.md"
        return f"https://github.com/{repo.name}/blob/{branch}/{filepath}"