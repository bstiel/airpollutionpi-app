import random
import time
import requests

from datetime import datetime, timezone


for i in range(1000):
    payload = {
        'ts': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
        'id': 'pibot-2',
        'data': {
            'temperature': round(random.uniform(15., 30.), 2)
        }
    }
    requests.post('http://api:8000', json=[payload])
    time.sleep(0.1)