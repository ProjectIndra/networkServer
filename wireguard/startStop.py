import os
import subprocess

def is_interface_up(interface_name: str) -> bool:
    """
    Check if a network interface is up.

    Args:
        interface_name (str): The name of the network interface.

    Returns:
        bool: True if the interface is up, False otherwise.
    """
    try:
        sudo_password = os.getenv("SUDO_PASSWORD")
        if not sudo_password:
            print("SUDO_PASSWORD environment variable is not set.")
            return False
        # Check the interface status
        result = subprocess.run(
            ["sudo", "-S", "wg", "show", interface_name],
            input=sudo_password + "\n",
            check=True,
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        return False

def stop_interface(interface_name: str) -> None:
    """
    Stop a WireGuard interface.

    Args:
        interface_name (str): The name of the WireGuard interface to stop.
    """
    try:
        sudo_password = os.getenv("SUDO_PASSWORD")
        if not sudo_password:
            print("SUDO_PASSWORD environment variable is not set.")
            return

        if not is_interface_up(interface_name):
            print(f"WireGuard interface {interface_name} is already stopped.")
            return

        # Bring the interface down
        subprocess.run(
            ["sudo", "-S", "wg-quick", "down", interface_name],
            input=sudo_password + "\n",
            check=True,
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"WireGuard interface {interface_name} has been stopped.")
    except subprocess.CalledProcessError as e:
        print(f"Error stopping WireGuard interface.")

def start_interface(interface_name: str) -> None:
    """
    Start a WireGuard interface.

    Args:
        interface_name (str): The name of the WireGuard interface to start.
    """
    try:
        sudo_password = os.getenv("SUDO_PASSWORD")
        if not sudo_password:
            print("SUDO_PASSWORD environment variable is not set.")
            return

        if is_interface_up(interface_name):
            print(f"WireGuard interface {interface_name} is already up. Stopping it first.")
            stop_interface(interface_name)

        # Start the WireGuard interface
        subprocess.run(
            ["sudo", "-S", "wg-quick", "up", interface_name],
            input=sudo_password + "\n",
            check=True,
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"WireGuard interface {interface_name} has been started.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting WireGuard interface.")
