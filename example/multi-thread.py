import threading
import time

def job():
    index = 0
    while True:
        print("Child thread:", index)
        index = index + 1
        time.sleep(1)

t = threading.Thread(target = job)
t.start()

while True:
    print("H")
    time.sleep(1)

t.join()
