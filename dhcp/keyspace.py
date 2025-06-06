def interface_space(interface_name: str) -> str:
    """
    convert the interface name to a redis keyspace
    Args:
        interface_name (str): The name of the interface.
    """
    return "interface_ips:"+interface_name+":"

def peer_space(peer_name: str) -> str:
    """
    convert the peer name to a redis keyspace
    Args:
        peer_name (str): The name of the peer.
    """
    return "peer:"+peer_name+":"

def peer_details(peer_name: str) -> str:
    """
    convert the peer name to a redis keyspace
    Args:
        peer_name (str): The name of the peer.
    """
    return "peer_details:"+peer_name+":"

def next_ipaddress() -> str:
    """
    define the next available ip address keyspace
    """
    return "next_availaible_ip:"

def public_key(interface_name: str) -> str:
    """
    define the public key keyspace
    """
    return "public_key:"+interface_name+":"