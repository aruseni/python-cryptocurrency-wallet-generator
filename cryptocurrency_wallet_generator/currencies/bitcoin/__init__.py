import ctypes
import ctypes.util
import hashlib

from .base58 import encode as base58_encode


class Bitcoin:
    ssl_library = ctypes.cdll.LoadLibrary(ctypes.util.find_library("ssl"))

    # Since "1" is a zero byte, it won’t be present in the output address.
    addr_prefix = "1"

    version = 0

    def gen_ecdsa_pair(self):
        NID_secp160k1 = 708
        NID_secp256k1 = 714
        k = self.ssl_library.EC_KEY_new_by_curve_name(NID_secp256k1)

        if self.ssl_library.EC_KEY_generate_key(k) != 1:
            raise Exception("internal error?")

        bignum_private_key = self.ssl_library.EC_KEY_get0_private_key(k)
        size = (self.ssl_library.BN_num_bits(bignum_private_key)+7)//8
        storage = ctypes.create_string_buffer(size)
        self.ssl_library.BN_bn2bin(bignum_private_key, storage)
        private_key = storage.raw

        size = self.ssl_library.i2o_ECPublicKey(k, 0)
        storage = ctypes.create_string_buffer(size)
        self.ssl_library.i2o_ECPublicKey(
            k,
            ctypes.byref(ctypes.pointer(storage))
        )
        public_key = storage.raw

        self.ssl_library.EC_KEY_free(k)
        return public_key, private_key

    def ecdsa_get_coordinates(self, public_key):
        x = bytes(public_key[1:33])
        y = bytes(public_key[33:65])
        return x, y

    def generate_address(self, public_key):
        assert isinstance(public_key, bytes)

        x, y = self.ecdsa_get_coordinates(public_key)

        s = b"\x04" + x + y

        hasher = hashlib.sha256()
        hasher.update(s)
        r = hasher.digest()

        hasher = hashlib.new("ripemd160")
        hasher.update(r)
        r = hasher.digest()

        addr = self.base58_check(r, version=self.version)
        if self.addr_prefix:
            return "{}{}".format(self.addr_prefix, addr)
        else:
            return addr

    def base58_check(self, src, version):
        src = bytes([version]) + src
        hasher = hashlib.sha256()
        hasher.update(src)
        r = hasher.digest()

        hasher = hashlib.sha256()
        hasher.update(r)
        r = hasher.digest()

        checksum = r[:4]
        s = src + checksum

        return base58_encode(int.from_bytes(s, "big"))

    def test(self):
        public_key, private_key = self.gen_ecdsa_pair()

        hex_private_key = "".join(["{:02x}".format(i) for i in private_key])
        assert len(hex_private_key) == 64

        print(
            "ECDSA private key (random number / secret exponent) = {}".format(
                hex_private_key
            )
        )
        print("ECDSA public key = {}".format(
            "".join(["{:02x}".format(i) for i in public_key])
        ))
        print("Private key (Base58Check) = {}".format(
            self.base58_check(private_key, version=128+self.version)
        ))

        addr = self.generate_address(public_key)
        print("Address: {} (length={})".format(addr, len(addr)))

    def generate_wallet(self):
        public_key, private_key = self.gen_ecdsa_pair()

        return(
            self.base58_check(private_key, version=128+self.version),
            self.generate_address(public_key),
        )
