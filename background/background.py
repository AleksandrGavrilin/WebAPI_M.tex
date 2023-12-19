import requests
import os
import fcntl
import time


file = os.getenv("FILE_MOUNT", "../file_standart.log")

N = int(os.getenv("N", 10))
M = int(os.getenv("M", 100))

url = os.getenv("URL", "http://localhost:8000/api/data")


for _ in range(N):
    with open(file, 'at') as f:
        try:
            response = requests.get(url)
            response.raise_for_status()
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            response_JSON = response.json()
            for res in response_JSON:
                id = res.get('id')
                created = res.get('created')
                log = res.get('log')
                ip = log.get('ip')
                method = log.get('method')
                uri = log.get('uri')
                status_code = log.get('status_code')
                s = f'{id} {created} {ip} {method} {uri} {status_code}\n'
                f.write(s)
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)

        except Exception as e:
            f.write(f"Request failed: {e}")
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
    time.sleep(M)
