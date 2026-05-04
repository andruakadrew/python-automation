# device_ops.py
from netmiko import ConnectHandler
from datetime import datetime
import pathlib
import sys
import os
from pathlib import Path


class NetworkDevice:
    def __init__(self, hostname, ip, device_type):
        self.hostname = hostname
        self.ip = ip
        self.device_type = device_type

    def send_command(self, command):
        """Connect to device, run command, return output."""
        device_params = {
            'device_type': self.device_type,
            'host': self.ip,
            'username': 'admin',
            'password': 'cisco',   # In production, use env vars
            'secret': 'cisco',
            'timeout': 10,
        }
        connection = ConnectHandler(**device_params)
        output = connection.send_command(command)
        connection.disconnect()
        return output

def save_to_backup(device_name, command, output):
    """Save command output to backups/ folder with timestamp."""
    backups_dir = pathlib.Path("backups")
    backups_dir.mkdir(exist_ok=True)          # create if missing
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{device_name}_{timestamp}.txt"
    filepath = backups_dir / filename
    with open(filepath, 'w') as f:
        f.write(f"Command: {command}\n\n{output}")
    return str(filepath)


def main():
    # 1. Use sys.argv to get command from CLI, default = "show version"
    command = sys.argv[1] if len(sys.argv) > 1 else "show version"

    # 2. Use pathlib to read device list
    devices_file = Path("devices.txt")
    if not devices_file.exists():
        print("Error: devices.txt not found.")
        sys.exit(1)

    with open(devices_file, 'r') as f:
        lines = f.read().strip().splitlines()

    for line in lines:
        if not line or line.startswith('#'):
            continue
        hostname, ip, device_type = [item.strip() for item in line.split(',')]
        print(f"\n--- Connecting to {hostname} ({ip}) ---")
        device = NetworkDevice(hostname, ip, device_type)

        try:
            output = device.send_command(command)
            saved_path = save_to_backup(hostname, command, output)
            print(f"Saved output to {saved_path}")
        except Exception as e:
            print(f"Failed on {hostname}: {e}")

if __name__ == "__main__":
    main()