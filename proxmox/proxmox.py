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


def list_vms(proxmox: ProxmoxAPI, node: str) -> List[dict]:
    """
    Lists all virtual machines on a specified Proxmox node.

    Args:
        proxmox (ProxmoxAPI): An authenticated ProxmoxAPI instance.
        node (str): The name of the Proxmox node to query.

    Returns:
        List[dict]: A list of dictionaries containing VM details.
    """
    return proxmox.nodes(node).qemu.get()


def list_nodes(proxmox: ProxmoxAPI) -> List[str]:
    """
    Lists all nodes in the Proxmox cluster.

    Args:
        proxmox (ProxmoxAPI): An authenticated ProxmoxAPI instance.

    Returns:
        List[str]: A list of node names in the Proxmox cluster.
    """
    return [node['node'] for node in proxmox.nodes.get()]


def print_vm_list(vms: List[dict]) -> None:
    """
    Prints a formatted list of virtual machines.

    Args:
        vms (List[dict]): A list of dictionaries containing VM details.
    """
    print(f"{'VM ID':<10} {'Name':<30} {'Status':<10}")
    print("=" * 50)
    for vm in vms:
        print(f"{vm['vmid']:<10} {vm['name']:<30} {vm['status']:<10}")


def print_all_vms(proxmox: ProxmoxAPI) -> None:
    """
    Prints all virtual machines across all nodes in the Proxmox cluster.

    Args:
        proxmox (ProxmoxAPI): An authenticated ProxmoxAPI instance.
    """
    nodes = list_nodes(proxmox)
    print()
    for node in nodes:
        print(f"Node: {node}")
        print()
        vms = list_vms(proxmox, node)
        print_vm_list(vms)
        print("\n")
