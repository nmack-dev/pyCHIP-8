import unittest

from chip8.memory import MemObj

class TestMemory(unittest.TestCase):

    def test_mem_get(self):
        mem = MemObj(64, 1)

        self.assertEqual(mem.mem_get('0x0004'), '0x0')
        
        # Ensures we don't access memory we don't have. 
        with self.assertRaises(Exception) as context:
            mem.mem_get('0xFFFF')

if __name__ == '__main__':
    unittest.main()