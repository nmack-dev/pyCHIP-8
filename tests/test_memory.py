import unittest

from chip8.memory import MemObj, AddrStack, Memory

class TestMemory(unittest.TestCase):

    def test_mem_get(self):
        mem = MemObj(64, 1)

        self.assertEqual(mem.mem_get('0x0004'), '0x0')
        
        # Ensures we don't access memory we don't have. 
        with self.assertRaises(Exception) as context:
            mem.mem_get('0xFFFF')


    def test_mem_set(self):
        mem = MemObj(64, 1)

        mem.mem_set('0x0004', '0x1')
        self.assertEqual(mem.mem_get('0x0004'), '0x1')

        # Ensures we don't access memory we don't have. 
        with self.assertRaises(Exception) as context:
            mem.mem_set('0xFFFF', '0x1')

    # TODO: Implement bit_set, currently broken
    # def test_bit_set(self):
    #     mem = MemObj(64, 1)

    #     mem.mem_set('0x0004', '0x1')
    #     mem.bit_set('0x0004', 0, '0x1')

    #     self.assertEqual(mem.mem_get('0x0004'), '0x3')

    #     # Ensures we don't access memory we don't have.
    #     with self.assertRaises(Exception) as context:
    #         mem.bit_set('0xFFFF', 0, '0x1')

    #     # Ensures we don't access bits we don't have.
    #     with self.assertRaises(Exception) as context:
    #         mem.bit_set('0x0004', 8, '0x1')


class TestAddrStack(unittest.TestCase):

    def test_push_addr(self):
        stack = AddrStack(16)

        stack.push_addr('0x0004')
        self.assertEqual('0x0004', stack.pop_addr())


    def test_pop_addr(self):
        stack = AddrStack(16)

        stack.push_addr('0x0004')
        self.assertEqual('0x0004', stack.pop_addr())

        # Ensures we don't pop from an empty stack.
        with self.assertRaises(Exception) as context:
            stack.pop_addr()

    
    def test_get_stack_ptr(self):
        stack = AddrStack(16)

        self.assertEqual(stack.get_stack_ptr(), '0x0')

        stack.increment_stack_ptr()
        self.assertEqual(stack.get_stack_ptr(), '0x1')


class TestMemObj(unittest.TestCase):

    def test_increment_pc(self):
        memory = Memory()
        self.assertEqual('0x0', memory.program_counter)

        memory.increment_pc()
        self.assertEqual('0x2', memory.program_counter)


if __name__ == '__main__':
    unittest.main()