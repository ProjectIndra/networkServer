import os
import time
import subprocess

from redisClient import redis_client
from dhcp import keyspace
from dhcp import peerRequests
from wireguard import startStop
from wireguard import configerations

def run_peer_add_command(
    interface_name: str,
    peer_name: str,
    public_key: str,
):
    """
    Run the command to add a peer to the WireGuard interface.

    Args:
        interface_name (str): The name of the WireGuard interface.
        peer_name (str): The name of the peer to be added.
        public_key (str): The public key of the peer.

    Returns:
        str: A message indicating the result of the operation.
    """
    # Get the IP address for the peer
    ip_address = peerRequests.ip_for_peer(peer_name)

    try:
        sudo_password = os.getenv("SUDO_PASSWORD")
        result = subprocess.run(
            [
            "sudo",
            "-S",
            "wg",
            "set",
            interface_name,
            "peer",
            public_key,
            "allowed-ips",
            ip_address,
            ],
            input=sudo_password + "\n",
            check=True,
            text=True,
            # stdout=subprocess.DEVNULL,
            # stderr=subprocess.DEVNULL,
        )

        peerRequests.set_ip_for_peer(
            peer_name=peer_name,
            ip_address=ip_address,
        )
        
        return f"Peer {peer_name} added to {interface_name} with public key {public_key} and IP address {ip_address}."

    except subprocess.CalledProcessError as e:
        return f"Error adding peer {peer_name} to {interface_name}: {e}"


def peer_exists(peer_name: str) -> bool:
    """
    Check if a peer exists redis.
    Args:
        peer_name (str): The name of the peer to check.
    Returns:
        bool: True if the peer exists, False otherwise.
    """

    return redis_client.exists(keyspace.peer_space(peer_name))

def add_peer(
    interface_name: str,
    peer_name: str,
    public_key: str,
):
    """
    Add a peer to the WireGuard interface.

    Args:
        interface_name (str): The name of the WireGuard interface.
        peer_name (str): The name of the peer to be added.
        public_key (str): The public key of the peer.

    Returns:
        str: A message indicating the result of the operation.
    """
    # Check if the interface exists
    if not startStop.is_interface_up(interface_name):
        return f"Interface {interface_name} does not exist."

    # Check if the peer already exists
    if peer_exists(peer_name):
        return f"Peer {peer_name} already exists on {interface_name}."

    run_peer_add_command(
        interface_name=interface_name,
        peer_name=peer_name,
        public_key=public_key,
    )

    return f"Peer {peer_name} added to {interface_name} with public key {public_key}."