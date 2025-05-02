def next_ipaddress(ip_address: str) -> str:
    """
    Get the next available IP address from Redis.
    """
    # Get the next available IP address from Redis
    # now set the next interface ip to the next one for the next interface
    ip, cidr = ip_address.split("/")
    
    ip_parts = ip.split(".")
    ip_parts = list(map(int, ip_parts))
    
    for i in range(3, -1, -1):
        if ip_parts[i] < 255:
            ip_parts[i] += 1
            ip_parts[i+1:] = [0] * (3 - i)
            break
    else:
        raise ValueError("No more IP addresses available")
    
    # Create the next IP address
    next_ip = ".".join(map(str, ip_parts))
    next_ip = f"{next_ip}/{cidr}"
    return next_ip