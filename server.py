from flask import Flask, request, jsonify
from flask_cors import CORS
import sys

#internal imports
from redisClient import test_redis_connection
from wireguard import interface
from wireguard import peer
from controllers import addPeer, getPeerDetails, removePeer


# main Flask app
app = Flask(__name__)
CORS(app)

app.add_url_rule('/api/addPeer', view_func=addPeer.addPeerToWG, methods=['POST'])
app.add_url_rule('/api/removePeer', view_func=removePeer.removePeerFromWG, methods=['POST'])
app.add_url_rule('/api/getPeerDetails', view_func=getPeerDetails.getPeerDetails, methods=['POST'])


if __name__ == '__main__':

    # create main configeration
    print(interface.new_interface(interface_name="wg0"))

    # Test Redis connection
    if test_redis_connection():
        print("Redis connection is successful.")
    else:
        print("Redis connection failed.")
        sys.exit(1)

    app.run(debug=True, host='0.0.0.0', port=3000)