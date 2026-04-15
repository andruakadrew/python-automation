# ============================================================
# Level 008 - ARP Table Viewer with Vendor Identification
# ============================================================
# Reads the local ARP cache, parses each entry for IP and MAC
# pairs, and identifies the device manufacturer via OUI lookup
# using the Wireshark manuf database. Displays a formatted
# table with IP, MAC, vendor, entry type, and interface.
# Cross-platform — parses both Windows and Linux/macOS output.
#
# Usage:
#   python level_008_arp_viewer.py
#   python level_008_arp_viewer.py --dynamic-only
#   python level_008_arp_viewer.py -i 192.168.1.50
#
# Dependencies: requests
# ============================================================

import subprocess
import platform
import re
import os
import sys
import argparse
import requests

OUI_URL = "https://standards-oui.ieee.org/oui/oui.txt"
OUI_CACHE = os.path.join(os.path.expanduser("~"), ".oui_cache.txt")


def normalize_mac(mac):
    """Normalize a MAC address to uppercase colon-separated format."""
    mac_clean = re.sub(r"[.:\-]", "", mac.strip())
    if len(mac_clean) != 12 or not re.match(r"^[0-9A-Fa-f]{12}$", mac_clean):
        return None
    mac_upper = mac_clean.upper()
    return ":".join(mac_upper[i:i+2] for i in range(0, 12, 2))


def download_oui_database():
    """Download the OUI database and cache it locally."""
    print("  Downloading OUI database...")
    try:
        response = requests.get(OUI_URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        with open(OUI_CACHE, "w", encoding="utf-8") as f:
            f.write(response.text)
        return True
    except requests.RequestException as e:
        print(f"  Error downloading OUI database: {e}")
        return False


def parse_oui_database():
    """Parse the cached OUI database into a dictionary."""
    oui_dict = {}
    if not os.path.exists(OUI_CACHE):
        if not download_oui_database():
            return oui_dict
    with open(OUI_CACHE, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(
                r"^\s*([0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2})\s+\(hex\)\s+(.+)$",
                line
            )
            if match:
                oui = match.group(1).replace("-", ":").upper()
                vendor = match.group(2).strip()
                oui_dict[oui] = vendor
    return oui_dict


def lookup_vendor(mac, oui_dict):
    """Look up vendor for a MAC address."""
    normalized = normalize_mac(mac)
    if not normalized:
        return "Invalid MAC"
    oui_prefix = normalized[:8]
    return oui_dict.get(oui_prefix, "Unknown")


def read_arp_table():
    """Read the system ARP table and return raw output."""
    os_type = platform.system().lower()
    try:
        if os_type == "windows":
            result = subprocess.run(
                ["arp", "-a"],
                capture_output=True,
                text=True
            )
        else:
            result = subprocess.run(
                ["arp", "-an"],
                capture_output=True,
                text=True
            )
        if result.returncode != 0:
            print(f"  Error running arp command: {result.stderr}")
            return None
        return result.stdout
    except FileNotFoundError:
        print("  Error: arp command not found.")
        return None


def parse_windows_arp(output):
    """Parse Windows arp -a output into structured entries."""
    entries = []
    current_interface = None

    for line in output.strip().split("\n"):
        line = line.strip()

        iface_match = re.match(r"Interface:\s+([\d.]+)\s+---\s+0x([0-9a-fA-F]+)", line)
        if iface_match:
            current_interface = iface_match.group(1)
            continue

        entry_match = re.match(
            r"([\d.]+)\s+([0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2})\s+(\w+)",
            line
        )
        if entry_match:
            entries.append({
                "ip": entry_match.group(1),
                "mac": entry_match.group(2),
                "type": entry_match.group(3),
                "interface": current_interface
            })

    return entries


def parse_unix_arp(output):
    """Parse Linux/macOS arp -an output into structured entries."""
    entries = []

    for line in output.strip().split("\n"):
        match = re.match(
            r"\?\s+\(([\d.]+)\)\s+at\s+([0-9a-fA-F:]+)\s+.*on\s+(\S+)",
            line
        )
        if match:
            entries.append({
                "ip": match.group(1),
                "mac": match.group(2),
                "type": "dynamic",
                "interface": match.group(3)
            })

    return entries


def get_arp_entries():
    """Read and parse the ARP table based on the current OS."""
    output = read_arp_table()
    if not output:
        return []

    os_type = platform.system().lower()

    if os_type == "windows":
        return parse_windows_arp(output)
    else:
        return parse_unix_arp(output)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="ARP Table Viewer - View local ARP cache with vendor identification"
    )
    parser.add_argument(
        "-i", "--interface",
        help="Filter results by interface IP (Windows) or name (Linux/macOS)",
        default=None
    )
    parser.add_argument(
        "-d", "--dynamic-only",
        action="store_true",
        help="Show only dynamic (learned) entries"
    )
    return parser.parse_args()


def display_results(entries, oui_dict, iface_filter=None, dynamic_only=False):
    """Display ARP entries in a formatted table with vendor info."""
    filtered = entries

    if iface_filter:
        filtered = [e for e in filtered if e["interface"] == iface_filter]

    if dynamic_only:
        filtered = [e for e in filtered if e["type"].lower() == "dynamic"]

    print("=" * 90)
    print("  ARP TABLE VIEWER")
    print("=" * 90)

    header = f"  {'IP Address':<18} {'MAC Address':<20} {'Vendor':<22} {'Type':<10} {'Interface'}"
    print(header)
    print("-" * 90)

    for entry in filtered:
        vendor = lookup_vendor(entry["mac"], oui_dict)
        normalized = normalize_mac(entry["mac"]) or entry["mac"]

        print(
            f"  {entry['ip']:<18} {normalized:<20} {vendor:<22} {entry['type']:<10} {entry['interface']}"
        )

    print("-" * 90)
    print(f"  Total entries: {len(filtered)}")

    if iface_filter:
        print(f"  Filtered by interface: {iface_filter}")
    if dynamic_only:
        print(f"  Showing dynamic entries only")


if __name__ == "__main__":
    args = parse_args()

    print("  Loading OUI database...")
    oui_dict = parse_oui_database()

    if not oui_dict:
        print("  Warning: Could not load OUI database. Vendor info will be unavailable.")
        oui_dict = {}

    entries = get_arp_entries()

    if not entries:
        print("  No ARP entries found.")
        sys.exit(0)

    display_results(entries, oui_dict, args.interface, args.dynamic_only)