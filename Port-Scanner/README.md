# Port Scanner
A threaded TCP port scanner built in Python using the `socket` and `threading` modules. Probes a target host for open ports and attempts to retrieve service banners from 
responsive ports. I built this project to strengthen my understanding of TCP connections, multithreading, and how real-world scanning tools like Nmap operate at the socket 
level.

---

## Features
- Threaded scanning — one thread per port for fast concurrent results
- Accepts both IP addresses and hostnames with automatic DNS resolution
- Default common port list for quick scans
- Custom port range support via command line argument
- Banner grabbing on open ports to identify running services
- Scan duration timer

---

## Requirements
- Windows, macOS, or Linux
- Python 3.10 or higher
- No external dependencies — standard library only (`socket`, `threading`, `sys`, `datetime`)

---

## Installation

### Prerequisites
- Python 3.10 or higher
- Git installed on your system

### Step 1 — Clone the repository

```
git clone https://github.com/andruakadrew/network-programming.git
cd network-programming/port-scanner
```

---

## Usage

**Scan using default common ports**

```
python scanner.py <target>
```

**Scan using a custom port range**

```
python scanner.py <target> <start-end>
```

**Examples**

```
python scanner.py 127.0.0.1
python scanner.py scanme.nmap.org
python scanner.py scanme.nmap.org 1-1024
python scanner.py 192.168.1.1 20-500
```

---

## Example Output

```
--------------------------------------------------
Scanner target: 45.33.32.156
Ports: [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3389, 8080, 8443]
Started at: 04/01/2026 09:42:00 AM
--------------------------------------------------
Port 22    OPEN | SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13
Port 21    OPEN | No banner
Port 80    OPEN | HTTP/1.1 200 OK
--------------------------------------------------
Scan completed in 1.05 seconds
--------------------------------------------------
```

---

## Default Common Ports

| Port | Service |
|---|---|
| 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP |
| 53 | DNS |
| 80 | HTTP |
| 110 | POP3 |
| 135 | Microsoft RPC |
| 139 | NetBIOS |
| 143 | IMAP |
| 443 | HTTPS |
| 445 | SMB |
| 3389 | RDP |
| 8080 | HTTP Alternate |
| 8443 | HTTPS Alternate |

---

Developed on Python 3.13 / PowerShell / Windows
