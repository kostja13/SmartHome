import requests
import time
import os

for i in range(10):
    pid = os.fork()
    if pid == 0:  # child
        for x in range(100):
            start = int(round(time.time()*1000))
            r = requests.get('http://localhost/overview')
            stop = int(round(time.time()*1000))
            print(stop-start)
        break