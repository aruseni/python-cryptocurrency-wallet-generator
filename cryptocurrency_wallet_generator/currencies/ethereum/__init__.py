from ecdsa import SigningKey, SECP256k1
from ethereum.utils import privtoaddr, checksum_encode


class Ethereum:
    def get_address(self, priv):
        return checksum_encode(privtoaddr(priv.to_string()))

    def test(self):
        priv = SigningKey.generate(curve=SECP256k1)
        pub = priv.get_verifying_key().to_string()

        address = self.get_address(priv)

        print("Private key: ", priv.to_string().hex())
        print("Public key: ", pub.hex())
        print("Address: " + address)

    def generate_wallet(self):
        priv = SigningKey.generate(curve=SECP256k1)

        address = self.get_address(priv)

        return (priv.to_string().hex(), address)
