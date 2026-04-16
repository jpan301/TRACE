# source: SentrySafe / src/sentry/replays/endpoints/project_replay_viewed_by.py
# function: get

class ProjectReplayViewedByEndpoint:
    def get(self, request: Request, project: Project, replay_id: str) -> Response:
        """Return a list of users who have viewed a replay."""
        self.check_replay_access(request, project)

        try:
            uuid.UUID(replay_id)
        except ValueError:
            return Response(status=404)

        # query for user ids who viewed the replay
        filter_params = self.get_filter_params(request, project, date_filter_optional=False)

        # If no rows were found then the replay does not exist and a 404 is returned.
        viewed_by_ids_response: list[dict[str, Any]] = query_replay_viewed_by_ids(
            project_id=project.id,
            replay_id=replay_id,
            start=filter_params["start"],
            end=filter_params["end"],
            request_user_id=request.user.id,
            organization=project.organization,
        )
        if not viewed_by_ids_response:
            return Response(status=404)

        viewed_by_ids = viewed_by_ids_response[0]["viewed_by_ids"]
        if viewed_by_ids == []:
            return Response({"data": {"viewed_by": []}}, status=200)

        serialized_users = user_service.serialize_many(
            filter=dict(user_ids=viewed_by_ids, organization_id=project.organization.id),
            as_user=serialize_generic_user(request.user),
        )

        serialized_users = [_normalize_user(user) for user in serialized_users]

        return Response({"data": {"viewed_by": serialized_users}}, status=200)