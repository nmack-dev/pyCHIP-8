import unittest

from chip8.memory import MemObj

class TestMemory(unittest.TestCase):

    def test_mem_get(self):
        mem = MemObj(64)

        self.assertEqual(mem.mem_get('0x0004'), '0x0')


if __name__ == '__main__':
    unittest.main()