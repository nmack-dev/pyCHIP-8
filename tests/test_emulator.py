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

        self.assertEqual(emu.memory.addr_stack.stack_ptr, 1)
        self.assertEqual(emu.memory.addr_stack.memory[-1], '0x0')
        self.assertEqual(emu.memory.program_counter, '0x0004')


    def test_SE_BYTE(self):
        emu = Emulator()

        byte1 = '0x00'
        byte2 = '0x04'

        emu.memory.registers.mem_set('0x4', '0x2')
        emu.SE_BYTE(byte1, byte2)
        self.assertEqual(emu.memory.program_counter, '0x0')

        emu.memory.registers.mem_set('0x4', '0x0')
        emu.SE_BYTE(byte1, byte2)
        self.assertEqual(emu.memory.program_counter, '0x2')


    def test_SNE(self):
        emu = Emulator()

        byte1 = '0x00'
        byte2 = '0x04'

        emu.memory.registers.mem_set('0x4', '0x2')
        emu.SNE(byte1, byte2)
        self.assertEqual(emu.memory.program_counter, '0x2')

        emu.memory.registers.mem_set('0x4', '0x0')
        emu.SNE(byte1, byte2)
        self.assertEqual(emu.memory.program_counter, '0x2')

    
    def test_SE_REG(self):
        emu = Emulator()

        emu.memory.registers.mem_set('0x07', '0x2')
        emu.memory.registers.mem_set('0x08', '0x2')
        emu.SE_REG('0x07', '0x80')
        self.assertEqual(emu.memory.program_counter, '0x2')


    # def test_LD_BYTE(self):

    # def test_ADD_BYTE(self):

    # def test_LD_REG(self):

    # def test_OR(self):

    # def test_AND(self):

    # def test_XOR(self):

    # def test_ADD_REG(self):

    # def test_SUB(self):

    # def test_SHR(self):

if __name__ == '__main__':
    unittest.main()