from env_loader import load_proxmox_env
from proxmox.proxmox import connect_proxmox, get_version_proxmox


def main():
    config_proxmox = load_proxmox_env()
    proxmox = connect_proxmox(config_proxmox)
    print(f"Proxmox version: {get_version_proxmox(proxmox)}")


if __name__ == "__main__":
    main()
