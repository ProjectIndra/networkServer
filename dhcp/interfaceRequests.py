from redisClient import redis_client

#internal imports
from dhcp import ipaddresses
from dhcp import keyspace

def ip_for_interface(interface_name):
    """
    Get the IP address for a given interface name from Redis.
    """
    # Get the IP address for the given interface name
    ip_address = (
        (redis_client.get(keyspace.interface_space(interface_name)) or b"").decode("utf-8") or 
        (redis_client.get(keyspace.next_ipaddress()) or b"").decode("utf-8") or
        "10.0.0.1/32"
        )
    
    # set this interface ip to the redis
    redis_client.set(keyspace.interface_space(interface_name), ip_address)

    # set the new ip available
    redis_client.set(keyspace.next_ipaddress(), ipaddresses.next_ipaddress(ip_address=ip_address))

    # Return the IP address
    return ip_address