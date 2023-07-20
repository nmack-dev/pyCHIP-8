import unittest
import keyboard
import time

from chip8.memory import Memory
from chip8.emulator import Emulator

class TestEmulator(unittest.TestCase):

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


    def test_LD_BYTE(self):
        emu = Emulator()

        emu.LD_BYTE('0x07', '0x02')
        self.assertEqual(emu.memory.registers.mem_get('0x07'), '0x2')


    def test_ADD_BYTE(self):
        emu = Emulator()

        emu.memory.registers.mem_set('0x07', '0x2')
        emu.ADD_BYTE('0x07', '0x02')
        self.assertEqual(emu.memory.registers.mem_get('0x07'), '0x4')

    
    def test_LD_REG(self):
        emu = Emulator()

        emu.memory.registers.mem_set('0x07', '0x2')
        emu.LD_REG('0x07', '0x10')
        self.assertEqual(emu.memory.registers.mem_get('0x07'), '0x0')


    def test_OR(self):
        emu = Emulator()

        emu.memory.registers.mem_set('0x07', '0x2')
        emu.memory.registers.mem_set('0x08', '0x4')
        emu.OR('0x07', '0x80')
        self.assertEqual(emu.memory.registers.mem_get('0x07'), '0x6')


    def test_AND(self):
        emu = Emulator()

        emu.memory.registers.mem_set('0x07', '0x2')
        emu.memory.registers.mem_set('0x08', '0x4')
        emu.AND('0x07', '0x80')
        self.assertEqual(emu.memory.registers.mem_get('0x07'), '0x0')


    def test_XOR(self):
        emu = Emulator()

        emu.memory.registers.mem_set('0x07', '0x2')
        emu.memory.registers.mem_set('0x08', '0x4')
        emu.XOR('0x07', '0x80')
        self.assertEqual(emu.memory.registers.mem_get('0x07'), '0x6')


    def test_ADD_REG(self):
        emu = Emulator()

        # Test carry 0
        emu.memory.registers.mem_set('0x07', '0x2')
        emu.memory.registers.mem_set('0x08', '0x4')
        emu.ADD_REG('0x07', '0x80')
        self.assertEqual(emu.memory.registers.mem_get('0x07'), '0x6')
        self.assertEqual(emu.memory.registers.mem_get('0x0F'), '0x0')

        # Test carry 1
        emu.memory.registers.mem_set('0x07', '0xFF')
        emu.memory.registers.mem_set('0x08', '0x01')
        emu.ADD_REG('0x07', '0x80')
        self.assertEqual(emu.memory.registers.mem_get('0x07'), '0x0')
        self.assertEqual(emu.memory.registers.mem_get('0x0F'), '0x1')

    
    def test_SUB(self):
        emu = Emulator()
        
        emu.memory.registers.mem_set('0x07', '0x2')
        emu.memory.registers.mem_set('0x08', '0x4')
        emu.SUB('0x07', '0x80')
        self.assertEqual(emu.memory.registers.mem_get('0x07'), '0xfd')
        self.assertEqual(emu.memory.registers.mem_get('0x0F'), '0x0')

        emu.memory.registers.mem_set('0x07', '0x4')
        emu.memory.registers.mem_set('0x08', '0x2')
        emu.SUB('0x07', '0x80')
        self.assertEqual(emu.memory.registers.mem_get('0x07'), '0x2')
        self.assertEqual(emu.memory.registers.mem_get('0x0F'), '0x1')

    
    def test_SHR(self):
        emu = Emulator()

        emu.memory.registers.mem_set('0x07', '0x2')
        emu.SHR('0x07', '0x80')
        self.assertEqual(emu.memory.registers.mem_get('0x07'), '0x1')
        self.assertEqual(emu.memory.registers.mem_get('0x0F'), '0x0')

        emu.memory.registers.mem_set('0x07', '0x3')
        emu.SHR('0x07', '0x80')
        self.assertEqual(emu.memory.registers.mem_get('0x07'), '0x1')
        self.assertEqual(emu.memory.registers.mem_get('0x0F'), '0x1')

    
    def test_SUBN(self):
        emu = Emulator()

        emu.memory.registers.mem_set('0x07', '0x2')
        emu.memory.registers.mem_set('0x08', '0x4')
        emu.SUBN('0x07', '0x80')
        self.assertEqual(emu.memory.registers.mem_get('0x07'), '0x2')
        self.assertEqual(emu.memory.registers.mem_get('0x0F'), '0x1')

        emu.memory.registers.mem_set('0x07', '0x4')
        emu.memory.registers.mem_set('0x08', '0x2')
        emu.SUBN('0x07', '0x80')
        self.assertEqual(emu.memory.registers.mem_get('0x07'), '0xfd')
        self.assertEqual(emu.memory.registers.mem_get('0x0F'), '0x0')
    

    def test_SHL(self):
        emu = Emulator()

        emu.memory.registers.mem_set('0x07', '0x2')
        emu.SHL('0x07', '0x80')
        self.assertEqual(emu.memory.registers.mem_get('0x07'), '0x4')
        self.assertEqual(emu.memory.registers.mem_get('0x0F'), '0x0')

        emu.memory.registers.mem_set('0x07', '0x80')
        emu.SHL('0x07', '0x80')
        self.assertEqual(emu.memory.registers.mem_get('0x07'), '0x100')
        self.assertEqual(emu.memory.registers.mem_get('0x0F'), '0x1')

    
    def test_SNE(self):
        emu = Emulator()

        emu.memory.registers.mem_set('0x07', '0x2')
        emu.memory.registers.mem_set('0x08', '0x4')
        emu.SNE('0x07', '0x80')
        self.assertEqual(emu.memory.program_counter, '0x2')

        emu.memory.registers.mem_set('0x07', '0x2')
        emu.memory.registers.mem_set('0x08', '0x2')
        emu.SNE('0x07', '0x80')
        self.assertEqual(emu.memory.program_counter, '0x2')


    def test_LD_ADDR(self):
        emu = Emulator()

        emu.LD_ADDR('0x01', '0x23')
        self.assertEqual(emu.memory.index_reg.mem_get('0x00'), '0x123')


    def test_JP_LOC_ADDR(self):
        emu = Emulator()

        emu.memory.registers.mem_set('0x00', '0x01')
        emu.JP_LOC_ADDR('0x01', '0x23')
        self.assertEqual(emu.memory.program_counter, '0x124')


    def test_RND(self):
        emu = Emulator()

        emu.RND('0x01', '0x23')
        # Can't really test this (because it's random), but we can test that it's not zero
        self.assertNotEqual(emu.memory.registers.mem_get('0x01'), '0x0')

    
    def test_DRW(self):
        emu = Emulator()

        emu.memory.index_reg.mem_set('0x00', '0x00')
        emu.memory.memory.mem_set('0x00', '0xFF')
        emu.DRW('0x00', '0x01')

        row1 = sum(emu.display.screen[0])

        # 0xFF is 1111 1111, so the sum of those bits should be 8
        self.assertEqual(row1, 8)


    def test_SKP(self):
        emu = Emulator()

        emu.SKP('0x01', '0x00')
        self.assertEqual(emu.memory.program_counter, '0x0')
        
        keyboard.press(2)
        time.sleep(0.05)
        
        emu.SKP('0x01', '0x00')
        
        keyboard.release(2)
        
        self.assertEqual(emu.memory.program_counter, '0x2')
        

    def test_SKNP(self):
        emu = Emulator()

        emu.SKNP('0x02', '0x00')
        self.assertEqual(emu.memory.program_counter, '0x2')
        
        keyboard.press(3)
        time.sleep(0.05)
        
        emu.SKNP('0x02', '0x00')
        
        keyboard.release(3)
        
        self.assertEqual(emu.memory.program_counter, '0x2')


    def test_LD_REG_DEL_TIMER(self):
        emu = Emulator()

        emu.memory.delay_timer.mem_set('0x00', '0x0F')
        emu.LD_REG_DEL_TIMER('0x00', '0x00')
        self.assertEqual(emu.memory.registers.mem_get('0x00'), '0xf')

    
    def test_LD_KEY(self):
        emu = Emulator()

        keyboard.press(4)
        
        emu.LD_KEY('0x00', '0x00')
        self.assertEqual(False, emu.memory.delay_timer.timer.running)
        
        time.sleep(0.05)
        keyboard.release(4)
        
        self.assertEqual(True, emu.memory.delay_timer.timer.running)
        self.assertEqual(emu.memory.registers.mem_get('0x00'), '0x4')


if __name__ == '__main__':
    unittest.main()