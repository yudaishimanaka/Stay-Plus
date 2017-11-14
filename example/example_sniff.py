from scapy.all import *


def http_header(pkt):
    http_packet = str(pkt)
    if http_packet.find('GET'):
        return get_url(pkt)


def get_url(pkt):
    ret = "---------------------------------------TCP PACKET----------------------------------------------------\n"
    ret += "\n".join(pkt.sprintf("{Raw:%Raw.load%}\n").split(r"\r\n"))
    ret += "----------------------------------------------------------------------------------------------------\n"
    return ret

sniff(iface="enp0s25", filter="tcp and port 443", prn=get_url)
