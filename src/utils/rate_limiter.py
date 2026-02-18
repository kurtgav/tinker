import time
from collections import defaultdict, deque

class RateLimiter:
    def __init__(self, max_requests: int = 5, period_seconds: int = 600):
        self.max_requests = max_requests
        self.period_seconds = period_seconds
        # Dictionary to store request timestamps for each user
        self.requests = defaultdict(deque)

    def is_allowed(self, user_id: str) -> bool:
        now = time.time()
        user_requests = self.requests[user_id]

        # Remove requests older than the period
        while user_requests and user_requests[0] < now - self.period_seconds:
            user_requests.popleft()

        # Check if limit reached
        if len(user_requests) >= self.max_requests:
            return False

        # Add new request
        user_requests.append(now)
        return True

    def toggle_limit(self, user_id: str, active: bool):
       # Optional: Manual override if needed
       pass
