import unittest

import chip8.utils as utils

class TestUtils(unittest.TestCase):

    def test_get_nibble(self):
        byte = '0x51'

        self.assertEqual(utils.get_nibble(byte, 1), '5')
        self.assertEqual(utils.get_nibble(byte, 2), '1')
    

    def test_last_three_nibbles(self):
        byte1 = '0x51'
        byte2 = '0xAC'

        self.assertEqual(utils.last_three_nibbles(byte1, byte2), '1AC')


    def test_add_bytes(self):
        byte1 = '0x51'
        byte2 = '0xAC'

        self.assertEqual(utils.add_bytes(byte1, byte2), '0xfd')

    
    def test_or_bytes(self):
        byte1 = '0x51'
        byte2 = '0xAC'

        self.assertEqual(utils.or_bytes(byte1, byte2), '0xfd')
    

    def test_and_bytes(self):
        byte1 = '0x51'
        byte2 = '0xAC'

        self.assertEqual(utils.and_bytes(byte1, byte2), '0x0')
    

    def test_xor_bytes(self):
        byte1 = '0x51'
        byte2 = '0xAC'

        self.assertEqual(utils.xor_bytes(byte1, byte2), '0xfd')


if __name__ == '__main__':
    unittest.main()