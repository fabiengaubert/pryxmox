from typing import List

from proxmoxer import ProxmoxAPI


def connect_proxmox(config: dict) -> ProxmoxAPI:
    """
    Establishes a connection to the Proxmox API using the provided configuration.

    Args:
        config (dict): Dictionary containing connection parameters:
            - host (str): Proxmox server hostname or IP address.
            - user (str): Username for authentication.
            - port (int): Port number for the API.
            - token_name (str): API token name.
            - token_value (str): API token value.

    Returns:
        ProxmoxAPI: An authenticated ProxmoxAPI instance ready for requests.
    """
    print(f'Connecting to Proxmox server at {config['host']}')
    return ProxmoxAPI(
        host=config['host'],
        user=config['user'],
        port=config['port'],
        token_name=config['token_name'],
        token_value=config['token_value'],
        verify_ssl=False
    )


def get_version_proxmox(proxmox: ProxmoxAPI) -> bool:
    """
    Retrieves the version string of the connected Proxmox server.

    Args:
        proxmox (ProxmoxAPI): An authenticated ProxmoxAPI instance.

    Returns:
        str: Version string of the Proxmox server (e.g., "7.1-15").
    """
    return proxmox.version.get()['version']
