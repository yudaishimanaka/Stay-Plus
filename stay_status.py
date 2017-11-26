from database import Session as Ss
from models import User
import subprocess
import websocket
import threading


def stay_status(mac_address):
    def run():
        return "1"
    threading._start_new_thread(run,())


if __name__ == '__main__':
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1/")
    ws.on_open = stay_status()
    ws.run_forever()c