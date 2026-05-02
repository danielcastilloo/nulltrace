# NullTrace — Network Anonymization Tool

> Three-layer identity rotation for Linux: MAC spoofing · IP renewal · VPN tunneling.

NullTrace is a lightweight utility that automates a three-step anonymization workflow on Linux systems. Designed for security researchers, penetration testers, and privacy-conscious professionals who need a reproducible, auditable process for rotating their network identity before sensitive operations.

---

## How it works

| Step | Action | Result |
|------|--------|--------|
| 1/3  | MAC address rotation | Hardware identity replaced at layer 2 |
| 2/3  | IP renewal (DHCP or static) | Network identity replaced at layer 3 |
| 3/3  | ProtonVPN tunnel | Traffic exits through encrypted VPN node |

---

## Features

- Interactive interface — select network interface, IP method, and VPN country
- ProtonVPN integration — supports free tier (NL, US, JP) and premium countries
- No persistent config required — stateless, run it when you need it
- Auditable output — each step confirms success before proceeding

---

## Requirements

- Linux (tested on Debian/Ubuntu)
- `macchanger`
- `NetworkManager` (`nmcli`)
- `protonvpn-cli`

---

## Installation

```bash
git clone https://github.com/danielcastilloo/nulltrace.git
cd nulltrace
```

## Usage

```bash
sudo python3 nulltrace.py
```

---

## Disclaimer

This tool is intended for lawful use only — security research, privacy protection, and authorized penetration testing. The authors are not responsible for any misuse.

---

## License

MIT
EOF
