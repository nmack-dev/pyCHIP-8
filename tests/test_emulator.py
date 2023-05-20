import unittest

from chip8.memory import Memory
from chip8.emulator import Emulator

class TestEmulator(unittest.TestCase):

    def test_get_nibble(self):
        emu = Emulator()
        
        byte = '0x51'
        
        test = emu.get_nibble(byte, 1)

        self.assertEqual(emu.get_nibble(byte, 1), '5')
        self.assertEqual(emu.get_nibble(byte, 2), '1')


    def test_last_three_nibbles(self):
        emu = Emulator()

        byte1 = '0x51'
        byte2 = '0xAC'

        self.assertEqual(emu.last_three_nibbles(byte1, byte2), '1AC')


    def test_JP_ADDR(self):
        emu = Emulator()

        byte1 = '0x00'
        byte2 = '0x04'

        emu.JP_ADDR(byte1, byte2)

        self.assertEqual(emu.memory.program_counter, '0x0004')


    def test_CALL(self):
        emu = Emulator()

        byte1 = '0x00'
        byte2 = '0x04'

        emu.CALL(byte1, byte2)

        self.assertEqual(emu.memory.stack_ptr, 1)
        self.assertEqual(emu.memory.addr_stack[-1], '0x0000')
        self.assertEqual(emu.memory.program_counter, '0x0004')


    def test_SE_BYTE(self):
        emu = Emulator()

        byte1 = '0x00'
        byte2 = '0x04'

        emu.memory.memory[4] = '0x02'
        emu.SE_BYTE(byte1, byte2)
        self.assertEqual(emu.memory.program_counter, '0x0000')

        emu.memory.memory[4] = '0x00'
        emu.SE_BYTE(byte1, byte2)
        self.assertEqual(emu.memory.program_counter, '0x0002')


if __name__ == '__main__':
    unittest.main()