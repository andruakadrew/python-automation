"""Subnetting Calculator - IP/CIDR interface details from the command line."""
import argparse
import ipaddress

LABEL_WIDTH = 25

def parse_arg():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Show subnet details for an IP address with CIDR notation"
    )
    parser.add_argument(
        "ip_cidr",
        help="IP address with the CIDR notation (e.g., 192.168.1.0/24)"
    )
    return parser.parse_args()

def show(label, value):
    print(f"{label:<{LABEL_WIDTH}}{value}")

def calculate_subnet(ip_cidr):
    """Parse an IP/CIDR string and print its interface and subnet details."""
    try:
        interface = ipaddress.ip_interface(ip_cidr)
        network = interface.network

        print(f"\n--- Subnet Details for {ip_cidr} ---")
        show("IP Address:", interface.ip)
        show("Subnet Mask:", network.netmask)
        show("Wildcard Mask:", network.hostmask)
        show("CIDR Prefix:", f"/{network.prefixlen}")
        show("Network Address:", network.network_address)
        show("Broadcast Address:", network.broadcast_address)
        show("Private Address:", "Yes" if network.is_private else "No")
        show("Total Hosts:", network.num_addresses)
        show("Usable Hosts:", max(0, network.num_addresses - 2))



        if network.num_addresses > 2:
            hosts = list(network.hosts())
            show ("First usable IP address:", hosts[0])
            show ("Last usable IP address:", hosts[-1])
        else:
            print("No usable host range for this small subnet.")

    except ValueError as e:
        print(f"invalid input: {e}")

if __name__ == "__main__":
    args = parse_arg()
    calculate_subnet(args.ip_cidr)