from database import Session as Ss
from models import User
import tornado.ioloop
import tornado.web
import tornado.websocket
from queue import Queue
import time
import subprocess
import re
import threading


ip_fmt = "192.168.1.%d"
mac_list = []
lock = threading.Lock()


def get_mac(ip_address):
    output = subprocess.Popen(['arping', '-c', '1', ip_address], stdout=subprocess.PIPE).communicate()
    pattern = r"(\[(.+)\])"
    try:
        match_result = re.split(pattern, output[0].decode('utf-8'))
        with lock:
            if match_result is not None:
                print(match_result[2])
            else:
                pass
    except IndexError:
        pass


def dummy_func(num):
    return num


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("### connection started ###")

    def on_message(self, message):
        if message == 'hello':
            def threader():
                while True:
                    worker = q.get()
                    get_mac(worker)
                    q.task_done()

            q = Queue()

            for x in range(255):
                t = threading.Thread(target=threader)
                t.daemon = True
                t.start()

            for i in range(1, 255):
                ip = ip_fmt % i
                q.put(ip)

            q.join()

    def on_close(self):
        print("### connection closed ###")

app = tornado.web.Application([
    (r"/ws/", WebSocketHandler),
])

if __name__ == "__main__":
    app.listen(port=8888)
    mainloop = tornado.ioloop.IOLoop.instance()
    mainloop.start()

