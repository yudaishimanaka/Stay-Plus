from scapy.all import *
from flask_socketio import *
from flask import *

app = Flask(__name__)


def packet_capture(interface):
    obj = sniff(iface=interface, filter="tcp and port 80")
    obj.summary()
