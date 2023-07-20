import functools

from .timer import Timer, SoundTimer

class MemObj:

    def __init__(self, size, byte_width):
        self.memory = [0] * size
        self.byte_width = byte_width
        self.size = size


    def check_memory_size(func):
        @functools.wraps(func)
        def wrapper(self, *args):
            if (int(args[0], 16) <= (self.size - 1)):
            # TODO add a check input size decorator based on byte_width
            # if (int(args[0], 16) <= ((2 ** (self.byte_width * 8)) - 1)):
                return func(self, *args)
            else:
                raise Exception('ERROR: Out of bounds memory access')
        return wrapper


    @check_memory_size
    def mem_get(self, location):
        loc = int(location, 16)
        return hex(self.memory[loc])
    

    @check_memory_size
    def mem_set(self, location, val):
        loc = int(location, 16)
        self.memory[loc] = int(val, 16)


class AddrStack(MemObj):

    def __init__(self, size):
        self.memory = []
        self.byte_width = 2
        self.size = size
        self.stack_ptr = 0

    
    def push_addr(self, addr):
        if (len(self.memory) < self.size):
            self.memory.append(addr)
        else:
            raise Exception('Stack is full, cannot push address')

    
    def pop_addr(self):
        return self.memory.pop()
    

    def get_stack_ptr(self):
        return hex(self.stack_ptr)
    

    def increment_stack_ptr(self):
        self.stack_ptr += 1


class TimerReg(MemObj):
    # TODO test me :D

    def __init__(self, timerType) -> None:
        super().__init__(1, 1)
        self.timer = timerType
    

    def mem_get(self, location) -> str:
        return hex(self.timer.current)
    

    @MemObj.check_memory_size
    def mem_set(self, location, val) -> None:
        self.timer.set(int(val, 16))


class Memory:
    ram = 4096
    registers = 16

    def __init__(self):
        self.memory = MemObj(self.ram, 1)
        
        self.program_counter = '0x0'
        
        self.registers = MemObj(self.registers, 1)

        self.index_reg = MemObj(1, 2)
        
        self.addr_stack = AddrStack(16)

        # Empty init timers
        self.delay_timer = TimerReg(Timer(0))
        self.sound_timer = TimerReg(SoundTimer(0))


    def get_pc_instruction(self):
        return self.memory.mem_get(self.program_counter)


    def increment_pc(self):
        numeric_pc = int(self.program_counter, 16)
        numeric_pc += 2
        self.program_counter = hex(numeric_pc)