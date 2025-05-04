import os
from dotenv import load_dotenv
from flask import jsonify, request

from wireguard.peer import add_peer
from dhcp import interfaceRequests
from dhcp import peerRequests

load_dotenv()

def addPeerToWG():
    """
    Add a peer to the WireGuard interface.

    Args:
        interface_name (str): The name of the WireGuard interface.
        peer_name (str): The name of the peer to add.
        public_key (str): The public key of the peer.
    """
    try:
        interface_name = request.get_json().get("interface_name")
        peer_name = request.get_json().get("peer_name")
        public_key = request.get_json().get("public_key")
        if not interface_name or not peer_name or not public_key:
            return jsonify(
                {
                    "status": "error",
                    "error": "Missing required parameters: interface_name, peer_name, public_key.",
                }
            ), 400
            
        # Add the peer to the WireGuard interface
        result = add_peer(
            interface_name=interface_name,
            peer_name=peer_name,
            public_key=public_key,
        )

        if "error" in result.keys():
            return jsonify(
                {
                    "status": "error",
                    "error": f"Error adding peer {peer_name} to {interface_name}: {result['error']}",
                }
            ), 500

    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "error": f"Error adding peer {peer_name} to {interface_name}: {e}",
            }
        ),500

    try:
        interface_ip = interfaceRequests.ip_for_interface(interface_name=interface_name)

        endpoint = os.getenv("ENDPOINT")

        interface_public_key = interfaceRequests.get_public_key_for_interface(interface_name=interface_name)

        peer_ip = peerRequests.ip_for_peer(peer_name=peer_name)

        if public_key and endpoint and interface_ip and peer_ip:

            # get the interface details to send to the client
            interface_details = {
                "peer_name": peer_name,
                "interface_name": interface_name,
                "interface_public_key": interface_public_key,
                "interface_allowed_ips": interface_ip,
                "interface_endpoint": endpoint,
                "peer_public_key": public_key,
                "peer_address": peer_ip,
            }

            # cache this peer details
            peerRequests.set_details_for_peer(details=interface_details)

            return jsonify(
                {
                    "status": "success",
                    "message": f"Peer {peer_name} added to {interface_name} with public key {public_key} and IP address {interface_ip}.",
                    "interface_details": interface_details,
                }
            ), 200

        else:
            
            raise ValueError("Missing required information to send to the client.")
    
    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "error": f"Error getting interface details: {e}",
            }
        ), 500
