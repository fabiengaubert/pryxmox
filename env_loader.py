import os
import sys
from typing import Dict, Any

from dotenv import load_dotenv


REQUIRED_ENV_VARS = [
    "PROXMOX_HOST",
    "PROXMOX_PORT",
    "PROXMOX_USER",
    "PROXMOX_TOKEN_NAME",
    "PROXMOX_TOKEN_VALUE"
]


load_dotenv()


def load_proxmox_env() -> Dict[str, Any]:
    """
    Loads Proxmox API connection parameters from .env.

    If any required environment variables are missing, it writes an error
    message to stderr and exits the program.

    Returns:
        dict: A dictionary containing the Proxmox connection parameters:
            - host (str): Proxmox server hostname or IP.
            - port (int): Proxmox API port number.
            - user (str): Username for authentication.
            - token_name (str): API token name.
            - token_value (str): API token value.
    """
    missing_var = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing_var:
        sys.stderr.write(f"Error: Missing required env vars: {', '.join(missing_var)}\n")
        sys.exit(1)

    return {
        "host": os.getenv("PROXMOX_HOST"),
        "port": int(os.getenv("PROXMOX_PORT")),
        "user": os.getenv("PROXMOX_USER"),
        "token_name": os.getenv("PROXMOX_TOKEN_NAME"),
        "token_value": os.getenv("PROXMOX_TOKEN_VALUE")
    }
