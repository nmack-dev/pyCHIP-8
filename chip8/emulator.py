from .memory import Memory

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
        match self.get_nibble(byte1, 1):
            # case '0':
            #     CLS(byte1, byte2)
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
                self.LD_BYTE(byte1, byte2) 
            case '7':
                self.ADD_BYTE(byte1, byte2)
            case '8': 
                match self.get_nibble(byte2, 2):
                    case '0':
                        self.LD_REG(byte1, byte2)
                    case '1':
                        self.OR(byte1, byte2)
                    case '2':
                        self.AND(byte1, byte2)
                    case '3':
                        self.XOR(byte1, byte2)
                    case '4':
                        self.ADD_REG(byte1, byte2)
                    case '5':
                        self.SUB(byte1, byte2)
                    case '6':
                        self.SHR(byte1, byte2)
            #         case '7':
            #             SUBN(byte1, byte2)
            #         case 'E':
            #             SHL(byte1, byte2)
            # case '9':
            #     SNE(byte1, byte2)
            # case 'A':
            #     LD_ADDR(byte1, byte2) 
            # case 'B':
            #     JP_LOC_ADDR(byte1, byte2)
            # case 'C':
            #     RND(byte1, byte2) 
            # case 'D':
            #     DRW(byte1, byte2)
            # case 'E':
            #     match self.get_nibble(byte2, 1):
            #         case '9':
            #             SKP(byte1, byte2)
            #         case 'A':
            #             SKNP(byte1, byte2)
            # case 'F':
            #     match self.get_nibble(byte2, 1):
            #         case '1':
            #             match get_nibble(byte2, 2):
            #                 case '5':
            #                     LD_DEL_TIMER(byte1, byte2)
            #                 case '8':
            #                     LD_S_TIMER(byte1, byte2)
            #                 case 'E':
            #                     ADD_LOC(byte1, byte2)
            #         case '2':
            #             LD_SPRITE(byte1, byte2)
            #         case '3':
            #             LD_BCD(byte1, byte2)
            #         case '5':
            #             LD_MEM_LOC(byte1, byte2)
            #         case '6':
            #             LD_READ_LOC(byte1, byte2)


    # def CLS(self, byte1, byte2):


    def JP_ADDR(self, byte1, byte2):
        '''
        Jump to location nnn.

        The interpreter sets the program counter to nnn.
        '''
        location = '0x0' + self.last_three_nibbles(byte1, byte2)
        self.memory.program_counter = location


    def CALL(self, byte1, byte2):
        '''
        Call subroutine at nnn.

        The interpreter increments the stack pointer, then puts the current PC on the top of the stack. 
        The PC is then set to nnn.
        '''
        self.memory.addr_stack.increment_stack_ptr()
        self.memory.addr_stack.push_addr(self.memory.program_counter)

        location = '0x0' + self.last_three_nibbles(byte1, byte2)
        self.memory.program_counter = location


    def SE_BYTE(self, byte1, byte2):
        '''
        Skip next instruction if Vx = kk.

        The interpreter compares register Vx to kk, and if they are equal, increments the program counter by 2.
        '''
        second_nibble = '0x0' + self.get_nibble(byte1, 2)

        x = self.memory.registers.mem_get(byte2)
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
        '''
        Set Vx = kk.

        The interpreter puts the value kk into register Vx.
        '''
        second_nibble = int('0x0' + self.get_nibble(byte1, 2), 16)
        self.memory.registers[second_nibble] = byte2


    def ADD_BYTE(self, byte1, byte2):
        '''
        Set Vx = Vx + kk.

        Adds the value kk to the value of register Vx, then stores the result in Vx. 
        '''
        second_nibble = int('0x0' + self.get_nibble(byte1, 2), 16)
        self.memory.registers[second_nibble] = hex(second_nibble + int(byte2, 16))


    def LD_REG(self, byte1, byte2):
        '''
        Set Vx = Vy.

        Stores the value of register Vy in register Vx.
        '''
        second_nibble = int('0x0' + self.get_nibble(byte1, 2), 16)
        third_nibble = int('0x0' + self.get_nibble(byte2, 1), 16)

        self.memory.registers[second_nibble] = self.memory.registers[third_nibble]


    def OR(self, byte1, byte2):
        '''
        Set Vx = Vx OR Vy.

        Performs a bitwise OR on the values of Vx and Vy, then stores the result in Vx. 
        '''
        second_nibble = int('0x0' + self.get_nibble(byte1, 2), 16)
        third_nibble = int('0x0' + self.get_nibble(byte2, 1), 16)

        reg1_val = int(self.memory.registers[second_nibble], 16)
        reg2_val = int(self.memory.registers[third_nibble], 16)

        self.memory.registers[second_nibble] = hex(reg1_val | reg2_val)


    def AND(self, byte1, byte2):
        '''
        Set Vx = Vx AND Vy.

        Performs a bitwise AND on the values of Vx and Vy, then stores the result in Vx.      
        '''
        second_nibble = int('0x0' + self.get_nibble(byte1, 2), 16)
        third_nibble = int('0x0' + self.get_nibble(byte2, 1), 16)

        reg1_val = int(self.memory.registers[second_nibble], 16)
        reg2_val = int(self.memory.registers[third_nibble], 16)

        self.memory.registers[second_nibble] = hex(reg1_val & reg2_val)


    def XOR(self, byte1, byte2):
        '''
        Set Vx = Vx XOR Vy.

        Performs a bitwise exclusive OR on the values of Vx and Vy, then stores the result in Vx.
        '''
        second_nibble = int('0x0' + self.get_nibble(byte1, 2), 16)
        third_nibble = int('0x0' + self.get_nibble(byte2, 1), 16)

        reg1_val = int(self.memory.registers[second_nibble], 16)
        reg2_val = int(self.memory.registers[third_nibble], 16)

        self.memory.registers[second_nibble] = hex(reg1_val ^ reg2_val)


    def ADD_REG(self, byte1, byte2):
        '''
        Set Vx = Vx + Vy, set VF = carry.

        The values of Vx and Vy are added together. 
        If the result is greater than 8 bits (i.e., > 255,) VF is set to 1, otherwise 0. 
        Only the lowest 8 bits of the result are kept, and stored in Vx.
        '''
        second_nibble = int('0x0' + self.get_nibble(byte1, 2), 16)
        third_nibble = int('0x0' + self.get_nibble(byte2, 1), 16)

        reg1_val = int(self.memory.registers[second_nibble], 16)
        reg2_val = int(self.memory.registers[third_nibble], 16)

        if ((reg1_val + reg2_val) <= 255):
            self.memory.registers[second_nibble] = hex(reg1_val + reg2_val)
            self.memory.registers[15] = '0x00'
        else:
            self.memory.registers[15] = '0x01'
            op_res = bin(reg1_val + reg2_val)
            setval = '0b'
            
            op_res_len = len(op_res)

            for i in range(8):
                setval += op_res[((op_res_len - 1) - 8) + i]

            setval = hex(int(setval, 2))
            self.memory.registers[second_nibble] = setval


    def SUB(self, byte1, byte2):
        '''
        Set Vx = Vx - Vy, set VF = NOT borrow.

        If Vx > Vy, then VF is set to 1, otherwise 0. Then Vy is subtracted from Vx, and the results stored in Vx.
        '''
        second_nibble = int('0x0' + self.get_nibble(byte1, 2), 16)
        third_nibble = int('0x0' + self.get_nibble(byte2, 1), 16)

        reg1_val = int(self.memory.registers[second_nibble], 16)
        reg2_val = int(self.memory.registers[third_nibble], 16)

        if (reg1_val > reg2_val):
            self.memory.registers[15] = '0x01'
            self.memory.registers[second_nibble] = hex(reg1_val - reg2_val)
        else:
            self.memory.registers[15] = '0x00'
            self.memory.registers[second_nibble] = hex(reg1_val - reg2_val)
        

    def SHR(self, byte1, byte2):
        '''
        Set Vx = Vx SHR 1.

        If the least-significant bit of Vx is 1, then VF is set to 1, otherwise 0. Then Vx is divided by 2.
        '''
        second_nibble = int('0x0' + self.get_nibble(byte1, 2), 16)
        reg1_val = int(self.memory.registers[second_nibble], 16)

        self.memory.registers[second_nibble] = hex(reg1_val >> 1)
        
        bin_val = bin(reg1_val)

        if (bin_val[-1] == '1'):
            self.memory.registers[15] = '0x01'
        else:
            self.memory.registers[15] = '0x00'

    # TODO: Implement
    # def SUBN(self, byte1, byte2):
    # def SHL(self, byte1, byte2):
    # def SNE(self, byte1, byte2):
    # def LD_ADDR(self, byte1, byte2): 
    # def JP_LOC_ADDR(self, byte1, byte2):
    # def RND(self, byte1, byte2): 
    # def DRW(self, byte1, byte2):
    # def SKP(self, byte1, byte2):
    # def SKNP(self, byte1, byte2):
    # def LD_DEL_TIMER(self, byte1, byte2):
    # def LD_S_TIMER(self, byte1, byte2):
    # def ADD_LOC(self, byte1, byte2):
    # def LD_SPRITE(self, byte1, byte2):
    # def LD_BCD(self, byte1, byte2):
    # def LD_MEM_LOC(self, byte1, byte2):
    # def LD_READ_LOC(self, byte1, byte2):
