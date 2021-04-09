class task_eto:
    def __init__(self, _id, action, queued_timestamp):
        self.id = _id
        self.action = action
        self.queued_timestamp = int(queued_timestamp)
        self.expires = self.queued_timestamp + int(24 * 60 * 60)