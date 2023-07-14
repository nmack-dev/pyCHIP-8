def get_nibble(byte, pos):
    return byte[pos + 1]


def last_three_nibbles(byte1, byte2):
    nibbles = get_nibble(byte1, 2)
    nibbles += get_nibble(byte2, 1)
    nibbles += get_nibble(byte2, 2)

    return nibbles


def add_bytes(byte1, byte2):
    return hex(int(byte1, 16) + int(byte2, 16))


def or_bytes(byte1, byte2):
    return hex(int(byte1, 16) | int(byte2, 16))


def and_bytes(byte1, byte2):
    return hex(int(byte1, 16) & int(byte2, 16))


def xor_bytes(byte1, byte2):
    return hex(int(byte1, 16) ^ int(byte2, 16))