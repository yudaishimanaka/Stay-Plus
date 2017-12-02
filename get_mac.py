import subprocess
import threading
import time
from queue import Queue
import re


lock=threading.Lock()
_start=time.time()
ip_fmt = "192.168.1.%d"


def get_mac(ip):
    output = subprocess.Popen(["arping", "-c", "1", ip], stdout=subprocess.PIPE).communicate()
    pattern = r"(\[(.+)\])"
    try:
        match_result = re.split(pattern, output[0].decode('utf-8'))
        with lock:
            if match_result is not None:
                print(match_result)
            else:
                pass
    except IndexError:
        pass

def threader():
    while True:
        worker=q.get()
        get_mac(worker)
        q.task_done()

q=Queue()

for x in range(255):
    t=threading.Thread(target=threader)
    t.daemon=True
    t.start()

for worker in range(1, 255):
    ip = ip_fmt % worker
    q.put(ip)

q.join()

print("Process completed in: ",time.time()-_start)
