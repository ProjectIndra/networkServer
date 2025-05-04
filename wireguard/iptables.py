import subprocess
import sys

# Function to execute system commands
def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(1)

def remove_peer_route(peer_ip):
    # Remove the route for the peer's IP
    run_command(f"ip route del {peer_ip}/32 dev wg0")
    print(f"Route for peer {peer_ip} removed from wg0.")

# Function to add route for a peer
def add_peer_route(peer_ip):
    # Add the route for the peer's IP
    run_command(f"ip route add {peer_ip}/32 dev wg0")
    print(f"Route for peer {peer_ip} added to wg0.")