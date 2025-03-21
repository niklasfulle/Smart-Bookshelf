"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0116,C0103,C0415
import struct


class MD4:
    """An implementation of the MD4 hash algorithm."""

    width = 32
    mask = 0xFFFFFFFF

    # Unlike, say, SHA-1, MD4 uses little-endian. Fascinating!
    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]

    def __init__(self, msg=None):
        """:param ByteString msg: The message to be hashed."""
        if msg is None:
            msg = b""

        self.msg = msg

        # Pre-processing: Total length is a multiple of 512 bits.
        ml = len(msg) * 8
        msg += b"\x80"
        msg += b"\x00" * (-(len(msg) + 8) % 64)
        msg += struct.pack("<Q", ml)

        # Process the message in successive 512-bit chunks.
        self._process([msg[i : i + 64] for i in range(0, len(msg), 64)])

    def __repr__(self):
        if self.msg:
            return "{}({})".format(self.__class__.__name__, self.msg)
        return "{}()".format(self.__class__.__name__)

    def __str__(self):
        return self.hexdigest()

    def __eq__(self, other):
        return self.h == other.h

    def bytes(self):
        """:return: The final hash value as a `bytes` object."""
        return struct.pack("<4L", *self.h)

    def hexbytes(self):
        """:return: The final hash value as hexbytes."""
        return self.hexdigest().encode()

    def hexdigest(self):
        """:return: The final hash value as a hexstring."""
        return "".join("{:02x}".format(value) for value in self.bytes())

    def _process(self, chunks):
        for chunk in chunks:
            X, h = list(struct.unpack("<16I", chunk)), self.h.copy()

            # Round 1.
            Xi = [3, 7, 11, 19]
            for n in range(16):
                i, j, k, l = map(lambda x: x % 4, range(-n, -n + 4))  # noqa: E741
                K, S = n, Xi[n % 4]
                hn = h[i] + MD4.F(h[j], h[k], h[l]) + X[K]
                h[i] = MD4.lrot(hn & MD4.mask, S)

            # Round 2.
            Xi = [3, 5, 9, 13]
            for n in range(16):
                i, j, k, l = map(lambda x: x % 4, range(-n, -n + 4))  # noqa: E741
                K, S = n % 4 * 4 + n // 4, Xi[n % 4]
                hn = h[i] + MD4.G(h[j], h[k], h[l]) + X[K] + 0x5A827999
                h[i] = MD4.lrot(hn & MD4.mask, S)

            # Round 3.
            Xi = [3, 9, 11, 15]
            Ki = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
            for n in range(16):
                i, j, k, l = map(lambda x: x % 4, range(-n, -n + 4))  # noqa: E741
                K, S = Ki[n], Xi[n % 4]
                hn = h[i] + MD4.H(h[j], h[k], h[l]) + X[K] + 0x6ED9EBA1
                h[i] = MD4.lrot(hn & MD4.mask, S)

            self.h = [((v + n) & MD4.mask) for v, n in zip(self.h, h)]

    @staticmethod
    def F(x, y, z):
        return (x & y) | (~x & z)

    @staticmethod
    def G(x, y, z):
        return (x & y) | (x & z) | (y & z)

    @staticmethod
    def H(x, y, z):
        return x ^ y ^ z

    @staticmethod
    def lrot(value, n):
        lbits, rbits = (value << n) & MD4.mask, value >> (MD4.width - n)
        return lbits | rbits


def main():
    # Import is intentionally delayed.
    import sys

    if len(sys.argv) > 1:
        messages = [msg.encode() for msg in sys.argv[1:]]
        for message in messages:
            print(MD4(message).hexdigest())
    else:
        messages = [b"", b"The quick brown fox jumps over the lazy dog", b"BEES"]
        known_hashes = [
            "31d6cfe0d16ae931b73c59d7e0c089c0",
            "1bee69a46ba811185c194762abaeae90",
            "501af1ef4b68495b5b7e37b15b4cda68",
        ]

        print("Testing the MD4 class.")
        print()

        for message, expected in zip(messages, known_hashes):
            print("Message: ", message)
            print("Expected:", expected)
            print("Actual:  ", MD4(message).hexdigest())
            print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
