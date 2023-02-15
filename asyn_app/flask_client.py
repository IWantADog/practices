import gevent
from gevent import monkey
monkey.patch_all()

import time
import requests

def greet(ident):
    print(f"{time.time()} - {ident}: greet")
    requests.get(f"http://127.0.0.1:8000/greet/?ident={ident}")
    print(f"{time.time()} - {ident}: greet finished")


if __name__ == '__main__':
    jobs = []
    for i in range(10):
        jobs.append(gevent.spawn(greet, i))
    gevent.joinall(jobs)