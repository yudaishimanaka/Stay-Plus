from scapy.all import *


counter = 0
def http_header(pkt):
    http_packet = str(pkt)
    if http_packet.find('TCP'):
        if http_packet.find('HTTP'):
            if http_packet.find('GET'):
                return get_url(pkt)


def get_url(pkt):
    global counter
    counter += 1
    return 'Packet #{}: {} ==> {}'.format(counter, pkt[0][1].src, pkt[0][1].dst)

sniff(iface="enp0s25", filter="tcp and port 80", prn=get_url)
