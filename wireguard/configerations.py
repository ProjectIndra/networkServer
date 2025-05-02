def generate_interface_configuration(private_key: str, address: str, listen_port: int) -> str:
    """
    Generate the WireGuard interface configuration.

    Args:
        private_key (str): The private key for the WireGuard interface.
        address (str): The IP address for the WireGuard interface.
        listen_port (int): The port for the WireGuard interface to listen on.

    Returns:
        str: The generated WireGuard interface configuration.
    """
    
    return f"""
[Interface]
PrivateKey = {private_key}
Address = {address}
ListenPort = {listen_port}
"""

def write_interface_configuration(interface_name: str, config: str) -> None:
    """
    Write the WireGuard interface configuration to a file.

    Args:
        interface_name (str): The name of the WireGuard interface.
        config (str): The WireGuard interface configuration.
    """
    
    try:
        # Write the configuration to a file
        config_file_path = f"/etc/wireguard/{interface_name}.conf"
        with open(config_file_path, "w") as config_file:
            config_file.write(config)
    except IOError as e:
        print(f"Error writing configuration file: {e}")
        return

