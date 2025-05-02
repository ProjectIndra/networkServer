import nacl.public
import base64

def generate_wireguard_keys():
    # Generate a new private key (32 random bytes)
    private_key = nacl.public.PrivateKey.generate()

    # Private key bytes
    private_key_bytes = private_key.encode()

    # Corresponding public key
    public_key_bytes = private_key.public_key.encode()

    # Base64 encode like wg expects
    private_key_b64 = base64.standard_b64encode(private_key_bytes).decode('ascii')
    public_key_b64 = base64.standard_b64encode(public_key_bytes).decode('ascii')

    return private_key_b64, public_key_b64