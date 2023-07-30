def get_nibble(byte, pos):
    if (len(byte) <= 3):
        byte = '0x0' + byte[2]

    return byte[pos + 1]


def get_nibble_byte(byte, pos):
    return '0x0'+ byte[pos + 1]


def last_three_nibbles(byte1, byte2):
    nibbles = get_nibble(byte1, 2)
    nibbles += get_nibble(byte2, 1)
    nibbles += get_nibble(byte2, 2)

    return nibbles


def last_three_nibbles_byte(byte1, byte2):
    return '0x0' + last_three_nibbles(byte1, byte2)


def get_byte_bin(byte):
    byte_bin = bin(int(byte, 16))[2:]

    if len(byte_bin) < 8:
        byte_bin = '0' * (8 - len(byte_bin)) + byte_bin

    return byte_bin


def add_bytes(byte1, byte2):
    return hex(int(byte1, 16) + int(byte2, 16))


def sub_bytes(byte1, byte2):
    res = int(byte1, 16) - int(byte2, 16)

    # add 0xFF to negative values for wrap around
    # TODO: is this correct?
    if res < 0:
        res += 256
    
    return hex(res)


def or_bytes(byte1, byte2):
    return hex(int(byte1, 16) | int(byte2, 16))


def and_bytes(byte1, byte2):
    return hex(int(byte1, 16) & int(byte2, 16))


def xor_bytes(byte1, byte2):
    return hex(int(byte1, 16) ^ int(byte2, 16))


def mask_to_byte(hex_val):
    return hex(int(hex_val, 16) & 0x00FF)


def byte_equals(byte1, byte2):
    return int(byte1, 16) == int(byte2, 16)