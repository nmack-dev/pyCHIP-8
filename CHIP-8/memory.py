class Memory:
    size = 4096

    def __init__(self):
        self.memory = ['0x00'] * self.size
        
        self.program_counter = 0
        
        self.registers = ['0x00'] * 16

        self.index_reg = '0x0000'
        
        self.addr_stack = []
        self.stack_ptr = 0


    def get_pc_instruction(self):
        return self.memory[self.program_counter]


    def increment_pc(self):
        self.program_counter += 2


    def push_addr_stack(self, addr):
        if (len(self.addr_stack) < 16):
            self.addr_stack.append(addr)