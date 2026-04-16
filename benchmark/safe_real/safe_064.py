# source: SentrySafe / src/sentry/notifications/utils/participants.py
# function: determine_eligible_recipients

def determine_eligible_recipients(
    project: Project,
    target_type: ActionTargetType,
    target_identifier: int | None = None,
    event: Event | GroupEvent | None = None,
    fallthrough_choice: FallthroughChoiceType | None = None,
) -> Iterable[Actor]:
    """
    Either get the individual recipient from the target type/id or the
    owners as determined by rules for this project and event.
    """
    if not (project and project.teams.exists()):
        logger.debug("Tried to send notification to invalid project: %s", project)

    elif target_type == ActionTargetType.MEMBER:
        user = get_user_from_identifier(project, target_identifier)
        if user:
            return [Actor.from_object(user)]

    elif target_type == ActionTargetType.TEAM:
        team = get_team_from_identifier(project, target_identifier)
        if team:
            return [Actor.from_orm_team(team)]

    elif target_type == ActionTargetType.ISSUE_OWNERS:
        if not event:
            return []

        suggested_assignees, outcome = get_owners(project, event, fallthrough_choice)

        # We're adding the current assignee to the list of suggested assignees because
        # a new issue could have multiple codeowners and one of them got auto-assigned.
        group_assignee = (
            GroupAssignee.objects.filter(group_id=event.group_id).first()
            if event.group_id is not None
            else None
        )
        if group_assignee:
            outcome = "match"
            assignee_actor = group_assignee.assigned_actor()
            suggested_assignees.append(assignee_actor)

        suspect_commit_users = None

        try:
            suspect_commit_users = Actor.many_from_object(get_suspect_commit_users(project, event))
            suggested_assignees.extend(suspect_commit_users)
        except (Release.DoesNotExist, Commit.DoesNotExist):
            logger.info("Skipping suspect committers because release does not exist.")
        except Exception:
            logger.exception("Could not get suspect committers. Continuing execution.")

        metrics.incr(
            "features.owners.send_to",
            tags={
                "outcome": (
                    outcome
                    if outcome == "match" or fallthrough_choice is None
                    else fallthrough_choice.value
                ),
                "hasSuspectCommitters": str(bool(suspect_commit_users)),
            },
        )

        if suggested_assignees:
            return dedupe_suggested_assignees(suggested_assignees)

        return Actor.many_from_object(get_fallthrough_recipients(project, fallthrough_choice))

    return set()