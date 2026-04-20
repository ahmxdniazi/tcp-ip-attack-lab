# 📸 Screenshot Placement Guide

This document tells you exactly which screenshot goes where.

## How to Extract Screenshots from the PDF

1. Open `TCP_IP_Attack_Lab_Report.pdf` in any PDF viewer
2. For each screenshot described below, **crop/export it** and save it with the exact filename shown

---

## Task 1 — SYN Flood (`screenshots/task1-syn-flood/`)

| Filename | What to capture | Report Screenshot # |
|----------|----------------|---------------------|
| `01-disable-syn-cookies.png` | Terminal showing `sysctl -w net.ipv4.tcp_syncookies=0` confirmation | Screenshot 1 |
| `02-python-script.png` | The full Python Scapy flood script in editor/terminal | Screenshot 2 |
| `03-attack-running.png` | `python3 synflood.py` executing | Screenshot 3 |
| `04-telnet-blocked.png` | `telnet 10.9.0.5` hanging / failing to connect | Screenshot 4 |
| `05-netstat-syn-recv.png` | `netstat -na` output filled with `SYN_RECV` rows | Screenshot 5 |
| `06-established-immune.png` | Successful Telnet login showing `ESTABLISHED` is unaffected | Screenshot 6 |
| `07-c-source-code.png` | C source code / `netstat` baseline before C attack | Screenshot 8 |
| `08-compile.png` | `gcc -o synflood synflood.c` compilation | Screenshot 10 |
| `09-c-attack-running.png` | `synflood 10.9.0.5 23` running | Screenshot 11 |
| `10-full-queue.png` | `netstat -na` showing full queue during C attack | Screenshot 12 |
| `11-connection-timeout.png` | `telnet: Unable to connect to remote host: Connection timed out` | Screenshot 13 |
| `12-enable-syn-cookies.png` | `sysctl -w net.ipv4.tcp_syncookies=1` | Screenshot 14 |
| `13-flood-with-cookies.png` | C flood still running, `SYN_RECV` visible | Screenshot 15 |
| `14-telnet-succeeds.png` | Telnet connects successfully despite active flood | Screenshot 16 |

---

## Task 2 — RST Attack (`screenshots/task2-rst-attack/`)

| Filename | What to capture | Report Screenshot # |
|----------|----------------|---------------------|
| `01-live-telnet-session.png` | Active Telnet session, logged in as seed | Screenshot 17 |
| `02-wireshark-seq-number.png` | Wireshark with SEQ number highlighted in TCP details pane | Screenshot 18 |
| `03-rst-script.png` | The RST script code | Screenshot 19 |
| `04-execute-rst.png` | Running the script — Scapy printing packet with `Flag 4 (R)` | Screenshot 20 |
| `05-session-killed.png` | `Connection closed by foreign host` on victim terminal | Screenshot 21 |

---

## Task 3 — Session Hijacking (`screenshots/task3-session-hijacking/`)

| Filename | What to capture | Report Screenshot # |
|----------|----------------|---------------------|
| `01-create-test-file.png` | `touch myfile.txt` + `ll` showing file exists | Screenshot 22 |
| `02-active-session.png` | Active Telnet session to be hijacked | Screenshot 23 |
| `03-wireshark-params.png` | Wireshark with sport/seq/ack values visible | Screenshot 24 |
| `04-hijack-script.png` | The session hijack script code | Screenshot 25 |
| `05-execute-hijack.png` | Scapy output showing payload `b'\r rm *\n\r'` | Screenshot 26 |
| `06-injection-wireshark.png` | Wireshark confirming injected packet + retransmissions | Screenshot 27 |
| `07-file-deleted.png` | `ll` showing `total 0` — file deleted | Screenshot 28 |

---

## Task 4 — Reverse Shell (`screenshots/task4-reverse-shell/`)

| Filename | What to capture | Report Screenshot # |
|----------|----------------|---------------------|
| `01-new-telnet-session.png` | Fresh Telnet session before hijack | Screenshot 29 |
| `02-wireshark-params.png` | Wireshark — sport=39714, seq, ack values | Screenshot 30 |
| `03-reverse-shell-script.png` | The reverse shell script code | Screenshot 31 |
| `04-netcat-listener.png` | `nc -lv 9090` / `Listening on 0.0.0.0 9090` | Screenshot 33 |
| `05-send-payload.png` | Scapy output with reverse shell payload | Screenshot 32 |
| `06-shell-received.png` | `ifconfig` output inside the received shell on attacker | Screenshot 34 |
| `07-full-capture.png` | Final Wireshark capture showing full attack chain | Screenshot 35 |

---

## Tips for Clean Screenshots

- **Crop tightly** — remove unnecessary desktop chrome
- **Increase terminal font size** before capturing — makes text readable in GitHub
- **Use consistent terminal theme** across all screenshots for a professional look
- **Highlight key values** (sequence numbers, flags) before capturing if possible
