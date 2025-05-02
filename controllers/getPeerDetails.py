from flask import jsonify, request

from dhcp import peerRequests

def getPeerDetails():
    """
    Get peer details from the DHCP server.
    """
    # Get the peer ID from the request
    peer_id = request.get_json().get("peer_name")
    
    # Validate the peer ID
    if not peer_id:
        return jsonify({"error": "Peer ID is required"}), 400

    # Get the peer details from the DHCP server
    peer_details = peerRequests.get_peer_details(peer_id)

    # Check if the peer details were found
    if not peer_details:
        return jsonify({"error": "Peer not found"}), 404

    # Return the peer details as JSON
    return jsonify(peer_details), 200
