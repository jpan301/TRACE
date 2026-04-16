# source: RedashSafe / redash/serializers/__init__.py
# function: serialize_dashboard

def serialize_dashboard(obj, with_widgets=False, user=None, with_favorite_state=True):
    layout = obj.layout

    widgets = []

    if with_widgets:
        for w in obj.widgets:
            if w.visualization_id is None:
                widgets.append(serialize_widget(w))
            elif user and has_access(w.visualization.query_rel, user, view_only):
                widgets.append(serialize_widget(w))
            else:
                widget = project(
                    serialize_widget(w),
                    (
                        "id",
                        "width",
                        "dashboard_id",
                        "options",
                        "created_at",
                        "updated_at",
                    ),
                )
                widget["restricted"] = True
                widgets.append(widget)
    else:
        widgets = None

    d = {
        "id": obj.id,
        "slug": obj.name_as_slug,
        "name": obj.name,
        "user_id": obj.user_id,
        "user": {
            "id": obj.user.id,
            "name": obj.user.name,
            "email": obj.user.email,
            "profile_image_url": obj.user.profile_image_url,
        },
        "layout": layout,
        "dashboard_filters_enabled": obj.dashboard_filters_enabled,
        "widgets": widgets,
        "options": obj.options,
        "is_archived": obj.is_archived,
        "is_draft": obj.is_draft,
        "tags": obj.tags or [],
        "updated_at": obj.updated_at,
        "created_at": obj.created_at,
        "version": obj.version,
    }

    return d