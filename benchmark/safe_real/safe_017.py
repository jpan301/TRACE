# source: RedashSafe / redash/models/__init__.py
# function: recent

class Query:
    def recent(cls, group_ids, user_id=None, limit=20):
        query = (
            cls.query.filter(Event.created_at > (db.func.current_date() - 7))
            .join(Event, Query.id == Event.object_id.cast(db.Integer))
            .join(DataSourceGroup, Query.data_source_id == DataSourceGroup.data_source_id)
            .filter(
                Event.action.in_(["edit", "execute", "edit_name", "edit_description", "view_source"]),
                Event.object_id is not None,
                Event.object_type == "query",
                DataSourceGroup.group_id.in_(group_ids),
                or_(Query.is_draft.is_(False), Query.user_id is user_id),
                Query.is_archived.is_(False),
            )
            .group_by(Event.object_id, Query.id)
            .order_by(db.desc(db.func.count(0)))
        )

        if user_id:
            query = query.filter(Event.user_id == user_id)

        query = query.limit(limit)

        return query