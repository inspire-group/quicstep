#!/usr/bin/env python3

from scapy.all import *
import sys

INITIAL = 0xC
RTT = 0xD
HANDSHAKE = 0xE

def handle_quic_handshake(pkt):
    # only want QUIC packets
    if Raw not in pkt:
        return

    # extract the first four bits from the QUIC header 
    header = (pkt[Raw].load[0] & 0xF0) >> 4

    # want to match long headers: initial, 0-rtt, and handshake
    # https://www.rfc-editor.org/rfc/rfc9000.html#name-long-header-packets
    if header == INITIAL or header == RTT or header == HANDSHAKE:
        sendp(pkt, iface="veth0")

def enable_bridge(iface: str):
    sniff(iface=[iface], store=False, prn=handle_quic_handshake, filter="udp", lfilter=lambda pkt: pkt[Ether].src == Ether().src)

if __name__ == "__main__":
    conf.sniff_promisc = True

    enable_bridge("enp0s3")