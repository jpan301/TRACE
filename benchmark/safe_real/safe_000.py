# source: SentrySafe / src/sentry/debug_files/artifact_bundles.py
# function: get_bundles_indexing_state

def get_bundles_indexing_state(
    org_or_project: Project | Organization, release_name: str, dist_name: str
) -> tuple[int, int]:
    """
    Returns the number of total bundles, and the number of fully indexed bundles
    associated with the given `release` / `dist`.
    """
    total_bundles = 0
    indexed_bundles = 0

    filter: dict = {
        "releaseartifactbundle__release_name": release_name,
        "releaseartifactbundle__dist_name": dist_name,
    }
    if isinstance(org_or_project, Project):
        filter["releaseartifactbundle__organization_id"] = org_or_project.organization.id
        filter["projectartifactbundle__project_id"] = org_or_project.id
    else:
        filter["releaseartifactbundle__organization_id"] = org_or_project.id

    query = (
        ArtifactBundle.objects.filter(**filter)
        .values_list("indexing_state")
        .annotate(count=Count("*"))
    )
    for state, count in query:
        if state == ArtifactBundleIndexingState.WAS_INDEXED.value:
            indexed_bundles = count
        total_bundles += count

    return (total_bundles, indexed_bundles)