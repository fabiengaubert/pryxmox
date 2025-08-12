#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pryxmox: A CLI tool to manage Proxmox VMs.
"""

import argparse
import sys

from env_loader import load_proxmox_env
from proxmox.proxmox_api import connect_proxmox, get_version_proxmox, print_all_vms, start_vm, stop_vm

DEFAULT_NODE = "pve"


def pryxmox(args: argparse.Namespace) -> None:
    config_proxmox = load_proxmox_env()
    proxmox = connect_proxmox(config_proxmox)
    if not proxmox:
        print("Failed to connect to Proxmox server.")
        sys.exit(1)

    print(f"Connected to Proxmox server at {config_proxmox['host']}")

    if args.command == "list":
        print_all_vms(proxmox)
    elif args.command == "start":
        start_vm(proxmox, node=DEFAULT_NODE, vmid=args.name)
    elif args.command == "stop":
        stop_vm(proxmox, node=DEFAULT_NODE, vmid=args.name)
    elif args.command == "version":
        version = get_version_proxmox(proxmox)
        print(f"Proxmox version: {version}")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Pryxmox: Proxmox CLI Tool")

    subparsers = arg_parser.add_subparsers(dest="command", required=True)

    p_start = subparsers.add_parser("start", help="Start a VM")
    p_start.add_argument("name", help="Name or ID of the VM")

    p_stop = subparsers.add_parser("stop", help="Stop a VM")
    p_stop.add_argument("name", help="Name or ID of the VM")

    p_list = subparsers.add_parser("list", help="List available VMs")

    p_version = subparsers.add_parser("version", help="Get Proxmox server version")

    args = arg_parser.parse_args()

    pryxmox(args)
