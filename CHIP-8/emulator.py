from memory import Memory

class Emulator:

    def __init__(self):
        self.memory = Memory()

    def get_nibble(self, byte, pos):
        return byte[pos + 1]
    
    
    def last_three_nibbles(self, byte1, byte2):
        nibbles = self.get_nibble(byte1, 2)
        nibbles += self.get_nibble(byte2, 1)
        nibbles += self.get_nibble(byte2, 2)

        return nibbles


    def decode_instr(self, byte1, byte2):
        match get_nibble(byte1, 1):
            case '0':
                CLS(byte1, byte2)
            case '1':
                self.JP_ADDR(byte1, byte2)
            case '2': 
                self.CALL(byte1, byte2)
            case '3':
                self.SE_BYTE(byte1, byte2)
            case '4':
                self.SNE(byte1, byte2) 
            case '5':
                self.SE_REG(byte1, byte2)
            case '6':
                LD_BYTE(byte1, byte2) 
            case '7':
                ADD_BYTE(byte1, byte2)
            case '8': 
                match get_nibble(byte2, 2):
                    case '0':
                        LD_REG(byte1, byte2)
                    case '1':
                        OR(byte1, byte2)
                    case '2':
                        AND(byte1, byte2)
                    case '3':
                        XOR(byte1, byte2)
                    case '4':
                        ADD_REG(byte1, byte2)
                    case '5':
                        SUB(byte1, byte2)
                    case '6':
                        SHR(byte1, byte2)
                    case '7':
                        SUBN(byte1, byte2)
                    case 'E':
                        SHL(byte1, byte2)
            case '9':
                SNE(byte1, byte2)
            case 'A':
                LD_ADDR(byte1, byte2) 
            case 'B':
                JP_LOC_ADDR(byte1, byte2)
            case 'C':
                RND(byte1, byte2) 
            case 'D':
                DRW(byte1, byte2)
            case 'E':
                match get_nibble(byte2, 1):
                    case '9':
                        SKP(byte1, byte2)
                    case 'A':
                        SKNP(byte1, byte2)
            case 'F':
                match get_nibble(byte2, 1):
                    case '1':
                        match get_nibble(byte2, 2):
                            case '5':
                                LD_DEL_TIMER(byte1, byte2)
                            case '8':
                                LD_S_TIMER(byte1, byte2)
                            case 'E':
                                ADD_LOC(byte1, byte2)
                    case '2':
                        LD_SPRITE(byte1, byte2)
                    case '3':
                        LD_BCD(byte1, byte2)
                    case '5':
                        LD_MEM_LOC(byte1, byte2)
                    case '6':
                        LD_READ_LOC(byte1, byte2)

    def CLS(self, byte1, byte2):


    def JP_ADDR(self, byte1, byte2):
        '''
        Jump to location nnn.

        The interpreter sets the program counter to nnn.
        '''
        location = int('0x0' + self.last_three_nibbles(byte1, byte2), 16)
        self.memory.program_counter = location


    def CALL(self, byte1, byte2):
        '''
        Call subroutine at nnn.

        The interpreter increments the stack pointer, then puts the current PC on the top of the stack. 
        The PC is then set to nnn.
        '''
        self.memory.stack_ptr += 1
        self.memory.push_addr_stack(self.memory.program_counter)

        location = int('0x0' + self.last_three_nibbles(byte1, byte2), 16)
        self.memory.program_counter = location


    def SE_BYTE(self, byte1, byte2):
        '''
        Skip next instruction if Vx = kk.

        The interpreter compares register Vx to kk, and if they are equal, increments the program counter by 2.
        '''
        second_nibble = int('0x0' + self.get_nibble(byte1, 2), 16)
        
        if (self.memory.registers[second_nibble] == self.memory.registers[int(byte2, 16)]):
            self.memory.increment_pc()


    def SNE(self, byte1, byte2):
        '''
        Skip next instruction if Vx != kk.

        The interpreter compares register Vx to kk, and if they are not equal, increments the program counter by 2.
        '''
        second_nibble = int('0x0' + self.get_nibble(byte1, 2), 16)
        
        if (self.memory.registers[second_nibble] == self.memory.registers[int(byte2, 16)]):
            self.memory.increment_pc()


    def SE_REG(self, byte1, byte2):
        '''
        Skip next instruction if Vx = Vy.

        The interpreter compares register Vx to register Vy, and if they are equal, increments the program counter by 2.
        '''
        second_nibble = int('0x0' + self.get_nibble(byte1, 2), 16)
        third_nibble = int('0x0' + self.get_nibble(byte2, 1), 16)

        if (self.memory.registers[second_nibble] == self.memory.registers[third_nibble]):
            self.memory.increment_pc()


    def LD_BYTE(self, byte1, byte2): 
    def ADD_BYTE(self, byte1, byte2):
    def LD_REG(self, byte1, byte2):
    def OR(self, byte1, byte2):
    def AND(self, byte1, byte2):
    def XOR(self, byte1, byte2):
    def ADD_REG(self, byte1, byte2):
    def SUB(self, byte1, byte2):
    def SHR(self, byte1, byte2):
    def SUBN(self, byte1, byte2):
    def SHL(self, byte1, byte2):
    def SNE(self, byte1, byte2):
    def LD_ADDR(self, byte1, byte2): 
    def JP_LOC_ADDR(self, byte1, byte2):
    def RND(self, byte1, byte2): 
    def DRW(self, byte1, byte2):
    def SKP(self, byte1, byte2):
    def SKNP(self, byte1, byte2):
    def LD_DEL_TIMER(self, byte1, byte2):
    def LD_S_TIMER(self, byte1, byte2):
    def ADD_LOC(self, byte1, byte2):
    def LD_SPRITE(self, byte1, byte2):
    def LD_BCD(self, byte1, byte2):
    def LD_MEM_LOC(self, byte1, byte2):
    def LD_READ_LOC(self, byte1, byte2):
