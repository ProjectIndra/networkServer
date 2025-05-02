import subprocess
import os

#internal imports
from wireguard import configerations
from wireguard import keys
from wireguard import startStop

from dhcp import interfaceRequests

def new_interface(interface_name: str) -> None:
    """
    Start a WireGuard interface.

    Args:
        interface_name (str): The name of the WireGuard interface to start.
    """

    private_key, public_key = keys.generate_wireguard_keys()
    
    address = interfaceRequests.ip_for_interface(interface_name=interface_name)
    
    # generate the interface configuration
    interface_configeration = configerations.generate_interface_configuration(private_key=private_key, address=address, listen_port=5000)

    # write the interface configuration to a file
    configerations.write_interface_configuration(interface_name=interface_name, config=interface_configeration)

    # bring the interface up with new configuration
    startStop.start_interface(interface_name=interface_name)

    return private_key, public_key