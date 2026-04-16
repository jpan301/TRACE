# source: RedashSafe / redash/handlers/groups.py
# function: post

class GroupResource:
    def post(self, group_id):
        group = models.Group.get_by_id_and_org(group_id, self.current_org)

        if group.type == models.Group.BUILTIN_GROUP:
            abort(400, message="Can't modify built-in groups.")

        group.name = request.json["name"]
        models.db.session.commit()

        self.record_event({"action": "edit", "object_id": group.id, "object_type": "group"})

        return group.to_dict()