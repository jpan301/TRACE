# source: SentrySafe / src/sentry/preprod/vcs/status_checks/size/tasks.py
# function: _get_artifact_filter_context

def _get_artifact_filter_context(artifact: PreprodArtifact) -> dict[str, str]:
    """
    Extract build metadata from an artifact for filter matching.

    Returns a dict with keys matching the filter key format:
    - git_head_ref: The git_head_ref name (from commit_comparison.head_ref)
    - platform_name: "apple" or "android" (derived from artifact_type)
    - app_id: The app ID (e.g., "com.example.app")
    - build_configuration_name: The build configuration name
    """
    context: dict[str, str] = {}

    if artifact.commit_comparison and artifact.commit_comparison.head_ref:
        context["git_head_ref"] = artifact.commit_comparison.head_ref

    if artifact.artifact_type is not None:
        if artifact.artifact_type == PreprodArtifact.ArtifactType.XCARCHIVE:
            context["platform_name"] = "apple"
        elif artifact.artifact_type in (
            PreprodArtifact.ArtifactType.AAB,
            PreprodArtifact.ArtifactType.APK,
        ):
            context["platform_name"] = "android"

    if artifact.app_id:
        context["app_id"] = artifact.app_id

    if artifact.build_configuration:
        try:
            context["build_configuration_name"] = artifact.build_configuration.name
        except Exception:
            pass

    return context