from flask import request, jsonify

from dhcp import peerRequests
from wireguard import configerations
from wireguard import peer

def removePeerFromWG():
    """
    Remove a peer from the WireGuard interface.
    """
    peer_name = request.json.get('peer_name')
    if not peer_name:
        return jsonify({"error": "Peer name is required"}), 400

    # Check if the peer exists
    peer_details = peerRequests.get_peer_details(peer_name)
    if not peer_details:
        return jsonify({"error": "Peer not found"}), 404

    # remove the peer from the interface
    interface_name = peer_details['interface_name']

    # remove the peer from the interface
    result = peer.remove_peer(
        interface_name=interface_name,
        peer_name=peer_name,
        public_key=peer_details['peer_public_key'],
    )
    if result:
        return jsonify({"message": "Peer removed successfully"}), 200
    else:
        return jsonify({"error": "Failed to remove peer"}), 500
    
