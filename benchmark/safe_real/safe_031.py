# source: RedashSafe / redash/models/__init__.py
# function: init_db

def init_db():
    default_org = Organization(name="Default", slug="default", settings={})
    admin_group = Group(
        name="admin",
        permissions=Group.ADMIN_PERMISSIONS,
        org=default_org,
        type=Group.BUILTIN_GROUP,
    )
    default_group = Group(
        name="default",
        permissions=Group.DEFAULT_PERMISSIONS,
        org=default_org,
        type=Group.BUILTIN_GROUP,
    )

    db.session.add_all([default_org, admin_group, default_group])
    # XXX remove after fixing User.group_ids
    db.session.commit()
    return default_org, admin_group, default_group