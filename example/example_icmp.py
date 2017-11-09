from scapy.all import *

target_ip = "192.168.1.1"
frame = Ether() / IP(dst=target_ip) / ICMP()
sendp(frame)
