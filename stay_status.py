from database import Session as Ss
from models import User
import tornado.ioloop
import tornado.web
import tornado.websocket
from scapy.all import *
import time
import subprocess
import re
import threading


ip_fmt = "192.168.1.%d"
mac_list = []

def get_mac(ip_address):
    output = subprocess.Popen(['arping', '-c', '1', ip_address], stdout=subprocess.PIPE).communicate()
    pattern = r"(\[(.+)\])"
    try:
        match_result = re.split(pattern, output[0].decode('utf-8'))
        return match_result[2]
    except IndexError:
        pass


def get_stay_status(arp_mac, db_mac):
    return "state"

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("### connection started ###")

    def on_message(self, message):
        if message == 'hello':
            user = Ss.query(User)
            for i in range(user.count()):
                print(user[i].mac_address)

    def on_close(self):
        print("### connection closed ###")

app = tornado.web.Application([
    (r"/ws/", WebSocketHandler),
])

if __name__ == "__main__":
    app.listen(port=8888)
    mainloop = tornado.ioloop.IOLoop.instance()
    mainloop.start()

