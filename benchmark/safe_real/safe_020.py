# source: RedashSafe / redash/handlers/groups.py
# function: get

class GroupListResource:
    def get(self):
        if self.current_user.has_permission("admin"):
            groups = models.Group.all(self.current_org)
        else:
            groups = models.Group.query.filter(models.Group.id.in_(self.current_user.group_ids))

        self.record_event({"action": "list", "object_id": "groups", "object_type": "group"})

        return [g.to_dict() for g in groups]