import time
from collections import deque

class ChatRateMonitor:
    def __init__(self, window_size=10, cooldown_period=5):
        self.window_size = window_size  # seconds
        self.cooldown_period = cooldown_period  # seconds
        self.timestamps = deque()
        self.message_log = deque()
        self.last_check_time = 0
        self.last_spam_detected_time = 0
        self.slowmode_active = False

    def log_message(self, username=None, message_id=None):
        now = time.time()
        self.timestamps.append(now)
        self.message_log.append({
            "timestamp": now,
            "username": username,
            "message_id": message_id
        })
        self._trim()

    def _trim(self):
        cutoff = time.time() - self.window_size
        while self.timestamps and self.timestamps[0] < cutoff:
            self.timestamps.popleft()
        while self.message_log and self.message_log[0]["timestamp"] < cutoff:
            self.message_log.popleft()

    def get_rate(self):
        self._trim()
        return len(self.timestamps)

    def is_spammy(self, threshold):
        now = time.time()
        if now - self.last_check_time < self.cooldown_period:
            return False
        self.last_check_time = now
        if self.get_rate() >= threshold:
            self.last_spam_detected_time = now
            self.slowmode_active = True
            return True
        return False

    def should_disable_slowmode(self, disable_threshold=3):
        now = time.time()
        time_since_spam = now - self.last_spam_detected_time
        if self.slowmode_active and time_since_spam > disable_threshold:
            self.slowmode_active = False
            return True
        return False

    def get_recent_usernames(self):
        return [entry["username"] for entry in self.message_log if entry["username"] is not None]

    def get_recent_message_ids(self):
        return [entry["message_id"] for entry in self.message_log if entry["message_id"] is not None]
