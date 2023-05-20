class MemObj:

    def __init__(self, size):
        self.memory = [0] * size

    def mem_get(self, location):
        loc = int(location, 16)
        return hex(self.memory[loc])
    
    def mem_set(self, location, val):
        loc = int(location, 16)
        self.memory[loc] = int(val, 16)

    def bit_set(self, location, bit, val):
        if (bit > 7):
            raise Exception('Can only index bits of byte from 0-7 (8 bits)')
        
        loc = int(location, 16)
        bin_val = bin(self.memory[loc])
        
        bin_val[bit + 3] = val


class Memory:
    ram = 4096
    registers = 16

    def __init__(self):
        self.memory = MemObj(self.ram)
        
        self.program_counter = '0x0000'
        
        self.registers = MemObj(16)

        self.index_reg = '0x0000'
        
        self.addr_stack = []
        self.stack_ptr = 0


    def get_pc_instruction(self):
        return self.memory.mem_get(self.program_counter)


    def increment_pc(self):
        numeric_pc = int(self.program_counter, 16)
        numeric_pc += 2
        self.program_counter = hex(numeric_pc)


    def push_addr_stack(self, addr):
        if (len(self.addr_stack) < 16):
            self.addr_stack.append(addr)