from scapy.all import *

obj = sniff(iface="wlp2s0", prn=lambda x: x.show())
obj.nsummary()
