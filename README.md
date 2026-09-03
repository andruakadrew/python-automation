# Network Automation Scripts

A collection of Python automation scripts for network diagnostics, monitoring, and reporting.

## Requirements
- Python 3.x
- macOS or Linux

## Scripts

| File | Description | How-To-Run |
|---|---|---|
| [subnetting-calculator](./subnetting-calculator.py) | Takes an IP address in CIDR notation and reports its network address, broadcast address, subnet mask, wildcard mask, and usable host range. |```python3 subnetting-calculator.py <ip-address><CIDR>``` (e.g. python3 subnetting-calculator.py 192.168.1.0/24)
| [network-interfaces](./network-interfaces.py) | Discovers all network interfaces on the local machine and reports their names, IPv4/IPv6 addresses, MAC addresses, and subnet masks. |
| [interface-status](./interface-status.py) | Pulls operational status, link speed, MTU, and live traffic counters. |
| [network-report](./network-report.py) | Merges interface address data and status into a formatted JSON report. |
| [ping](./ping.py) | Reads a list of IP addresses from ```ips.txt``` and determines if the host are reachable by using _ping_. |
| [ping-trace](./ping-trace.py) | Reads a list of IP addresses from ```devices.txt``` and use tracert to track the path a packet takes to it's destination. Results for each address are assigned to a _.txt_ report.  |



