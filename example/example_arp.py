from scapy.all import *

target_ip = "192.168.1.254"
frame = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=1, pdst=target_ip)
sendp(frame)
