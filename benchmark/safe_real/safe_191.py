# source: SentrySafe / src/sentry/testutils/factories.py
# function: create_service_hook

class Factories:
    def create_service_hook(
        actor=None, org=None, project=None, events=None, url=None, project_ids=None, **kwargs
    ):
        if project:
            if project_ids is not None:
                raise ValueError("Cannot provide both project and project_ids")
            project_ids = [project.id]
        if not actor:
            actor = Factories.create_user()
        if not org:
            if project:
                org = project.organization
            else:
                org = Factories.create_organization(owner=actor)
        if project_ids is None:  # empty list for project_ids is valid and means no project filter
            project_ids = [Factories.create_project(organization=org).id]
        if events is None:
            events = ["event.created"]
        if not url:
            url = "https://example.com/sentry/webhook"

        app_id = kwargs.pop("application_id", None)
        if app_id is None and "application" in kwargs:
            app_id = kwargs["application"].id
        installation_id = kwargs.pop("installation_id", None)
        if installation_id is None and "installation" in kwargs:
            installation_id = kwargs["installation"].id
        hook_id = hook_service.create_service_hook(
            application_id=app_id,
            actor_id=actor.id,
            installation_id=installation_id,
            organization_id=org.id,
            project_ids=project_ids,
            events=events,
            url=url,
        ).id
        return ServiceHook.objects.get(id=hook_id)