# source: RedashSafe / redash/handlers/alerts.py
# function: post

class AlertResource:
    def post(self, alert_id):
        req = request.get_json(True)
        params = project(req, ("options", "name", "query_id", "rearm"))
        alert = get_object_or_404(models.Alert.get_by_id_and_org, alert_id, self.current_org)
        require_admin_or_owner(alert.user.id)

        self.update_model(alert, params)
        models.db.session.commit()

        self.record_event({"action": "edit", "object_id": alert.id, "object_type": "alert"})

        return serialize_alert(alert)