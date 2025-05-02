from flask import jsonify

from wireguard.peer import add_peer
from dhcp import interfaceRequests

def add_peer_to_wg(
    interface_name: str,
    peer_name: str,
    public_key: str,
):
    """
    Add a peer to the WireGuard interface.

    Args:
        interface_name (str): The name of the WireGuard interface.
        peer_name (str): The name of the peer to add.
        public_key (str): The public key of the peer.
    """
    try:
        # Add the peer to the WireGuard interface
        add_peer(
            interface_name=interface_name,
            peer_name=peer_name,
            public_key=public_key,
        )

    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "message": f"Error adding peer {peer_name} to {interface_name}: {e}",
            }
        ),500

    try:
        interface_ip = peerRequests.get_ip_for_peer(peer_name=peer_name)


        # get the interface details to send to the client
        interface_details = {
            "interface_name": interface_name,
            "public_key": public_key,
            "allowed_ips": interface_ip,
            "endpoint": interface_name
        }

        return jsonify(
            {
                "status": "success",
                "message": f"Peer {peer_name} added to {interface_name} with public key {public_key} and IP address {interface_ip}.",
                "interface_details": interface_details,
            }
        ), 200
    
    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "message": f"Error getting interface details: {e}",
            }
        ), 500
