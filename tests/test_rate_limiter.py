import time
from igscraper.rate_limiter import RateLimiter

def test_rate_limiter_interval():
    rl = RateLimiter(1.0)
    t0 = time.time()
    rl.wait()
    rl.wait()
    assert time.time() - t0 >= 1.0
