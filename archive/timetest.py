import time
import math
import threading


def printTime():
    print(math.floor(time.time()))
    time.sleep(3)
    

def run_threaded(func):
    job_thread = threading.Thread(target = func)
    job_thread.start()
    

while 1:
    run_threaded(printTime)
    time.sleep(5)
