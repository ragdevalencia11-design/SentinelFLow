import requests
import random
import time
import threading
from urllib.parse import urlencode

TARGETS = [
    "http://172.16.226.2:8000/health",
    "http://httpbin.org/get",
    "http://httpbin.org/post",
    "http://httpbin.org/put",
]


def normal_traffic():
    """Regular requests that should score as normal."""
    while True:
        try:
            url = random.choice(TARGETS)
            requests.get(url, timeout=2)
            time.sleep(random.uniform(0.5, 2.0))
        except:
            pass


def suspicious_traffic():
    """Rapid requests and unusual patterns to trigger anomalies."""
    while True:
        try:
            # Rapid-fire requests (high packet rate)
            for _ in range(50):
                requests.get("http://172.16.226.2:8000/health", timeout=1)

            # Large payload request (unusual packet size)
            requests.post("http://httpbin.org/post", data={"x": "A" * 10000}, timeout=2)

            time.sleep(random.uniform(5, 10))
        except:
            pass


if __name__ == "__main__":
    print("Starting traffic generator...")
    print("Normal traffic thread: low volume, varied destinations")
    print("Suspicious traffic thread: rapid bursts, large payloads")

    t1 = threading.Thread(target=normal_traffic, daemon=True)
    t2 = threading.Thread(target=suspicious_traffic, daemon=True)
    t1.start()
    t2.start()

    input("\nPress Enter to stop...\n")