from redisClient import redis_client

#internal imports
from dhcp import ipaddresses
from dhcp import keyspace

def ip_for_peer(peer_name):
    """
    Get the IP address for a given peer name from Redis.
    """
    # Get the IP address for the given peer name
    ip_address = (
        (redis_client.get(keyspace.peer_space(peer_name)) or b"").decode("utf-8") or 
        (redis_client.get(keyspace.next_ipaddress()) or b"").decode("utf-8") or
        "10.0.0.2/32"
        )

    # Set the new IP available
    redis_client.set(keyspace.next_ipaddress(), ipaddresses.next_ipaddress(ip_address=ip_address))

    # Return the IP address
    return ip_address

def set_ip_for_peer(peer_name: str, ip_address: str) -> None:
    """
    Set the IP address for a given peer name in Redis.
    Args:
        peer_name (str): The name of the peer.
        ip_address (str): The IP address to set for the peer.
    """

    print(f"Setting IP address {ip_address} for peer {peer_name}")
    
    # Set the IP address for the given peer name
    redis_client.set(keyspace.peer_space(peer_name), ip_address)

    return ip_address