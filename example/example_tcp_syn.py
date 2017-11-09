from scapy.all import *

target_ip = "192.168.1.1"
dst_port = 5003
src_port = 5002
frame = IP(dst=target_ip) / TCP(flags='S', sport=src_port, dport=dst_port)
send(frame)
