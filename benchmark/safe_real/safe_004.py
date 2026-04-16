# source: SentrySafe / src/sentry/integrations/vsts/repository.py
# function: _format_commits

class VstsRepositoryProvider:
    def _format_commits(
        self, repo: Repository, commit_list: Sequence[Mapping[str, Any]]
    ) -> Sequence[Mapping[str, Any]]:
        return [
            {
                "id": c["commitId"],
                "repository": repo.name,
                "author_email": c["author"]["email"],
                "author_name": c["author"]["name"],
                "message": c["comment"],
                "patch_set": c.get("patch_set"),
                "timestamp": self.format_date(c["author"]["date"]),
            }
            for c in commit_list
        ]