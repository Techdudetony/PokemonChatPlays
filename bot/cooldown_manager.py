import time

class CooldownManager:
    def __init__(self, cooldown_seconds=2):
        self.cooldown_seconds = cooldown_seconds
        self.user_timestamps = {}

    def is_on_cooldown(self, username):
        now = time.time()
        last_time = self.user_timestamps.get(username, 0)
        return (now - last_time) < self.cooldown_seconds

    def update_timestamp(self, username):
        self.user_timestamps[username] = time.time()
