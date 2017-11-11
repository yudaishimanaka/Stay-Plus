from scapy.all import *


def http_header(pkt):
    http_packet = str(pkt)
    if http_packet.find('GET'):
        return get_url(pkt)


def get_url(pkt):
    return pkt[http].show

sniff(iface="enp0s25", filter="tcp and port 80", prn=get_url)
