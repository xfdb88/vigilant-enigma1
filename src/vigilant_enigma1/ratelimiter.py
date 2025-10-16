import threading
import time
import asyncio
__all__ = ["RateLimiter","AsyncRateLimiter"]

class RateLimiter:
    def __init__(self, qps: float):
        self.min_interval = 1.0 / qps if qps > 0 else 0
        self._lock = threading.Lock(); self._last = 0.0
    def wait(self):
        if self.min_interval <= 0: return
        with self._lock:
            now = time.time(); delta = now - self._last
            sleep_for = self.min_interval - delta
            if sleep_for > 0: time.sleep(sleep_for)
            self._last = time.time()

class AsyncRateLimiter:
    def __init__(self, qps: float):
        self.min_interval = 1.0 / qps if qps > 0 else 0
        self._lock = asyncio.Lock(); self._next_ts = 0.0
    async def wait(self):
        if self.min_interval <= 0: return
        async with self._lock:
            loop = asyncio.get_running_loop(); now = loop.time()
            if now < self._next_ts: await asyncio.sleep(self._next_ts - now); now = self._next_ts
            self._next_ts = now + self.min_interval
