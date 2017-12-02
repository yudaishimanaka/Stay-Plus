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
lock = threading.Lock()


def get_mac():
    mac_and_ip_list = []
    buf = []
    output = subprocess.Popen('python get_mac.py', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    pattern = r"(.........(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).+\[(.+)\])(.+])"
    try:
        while True:
            line = output.stdout.readline()
            buf.append(line)

            if not line and output.poll() is not None:
                break
        for i in range(255):
            match_result = re.match(pattern, buf[i].decode('utf-8'))
            if match_result is not None:
                mac_and_ip_list.append([match_result.group(2), match_result.group(3)])
            else:
                pass
        return mac_and_ip_list
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
            while True:
                data = []
                result = get_mac()
                user = Ss.query(User)
                for z in range(len(result)):
                    for x in range(user.count()):
                        if result[z][1].lower() == user[x].mac_address.lower():
                            print(user[x].user_name + ":" + user[x].mac_address + " is alive")
                            data.append([user[x].user_name, user[x].email_address, user[x].mac_address, user[x].avatar])
                self.write_message(str(data))
                time.sleep(15)

    def on_close(self):
        print("### connection closed ###")

app = tornado.web.Application([
    (r"/ws/", WebSocketHandler),
])

if __name__ == "__main__":
    app.listen(port=8888)
    mainloop = tornado.ioloop.IOLoop.instance()
    mainloop.start()

