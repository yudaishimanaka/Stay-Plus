from database import Session as Ss
from models import User
from tornado import gen
from tornado.ioloop import IOLoop
import tornado.web
import tornado.websocket
import json
import subprocess
import re
import datetime


ip_fmt = "192.168.1.%d"
clients = []


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


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("### connection started ###")
        clients.append(self)

    def on_message(self, message):
        print(message)

    def on_close(self):
        print("### connection closed ###")
        clients.remove(self)


@gen.coroutine
def send_message_to_client():
    while True:
        for c in clients:
            data = []
            result = get_mac()
            user = Ss.query(User)
            for z in range(len(result)):
                for x in range(user.count()):
                    if result[z][1].lower() == user[x].mac_address.lower():
                        print(user[x].user_name + ":" + user[x].mac_address + " is alive")
                        data.append({"user_name": str(user[x].user_name),
                                     "email_address": str(user[x].email_address),
                                     "mac_address": str(user[x].mac_address),
                                     "avatar": str(user[x].avatar),
                                     "ip_address": str(result[z][0])})
            c.write_message(json.dumps(data))
            Ss.close()

        yield gen.Task(
            IOLoop.current().add_timeout,
            datetime.timedelta(milliseconds=15000)
        )


app = tornado.web.Application([
    (r"/ws/", WebSocketHandler),
])

if __name__ == "__main__":
    send_message_to_client()
    app.listen(port=8888)
    IOLoop.current().start()
