from .memory import Memory
from . import utils

from random import randint

class Emulator:

    def __init__(self):
        self.memory = Memory()


    def decode_instr(self, byte1, byte2):
        match utils.get_nibble(byte1, 1):
            case '0':
                match utils.get_nibble(byte2, 1):
                    case 'E':
                        self.CLS(byte1, byte2)
                    case _:
                        self.SYS(byte1, byte2)
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
                match utils.get_nibble(byte2, 2):
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
            #     match utils.get_nibble(byte2, 1):
            #         case '9':
            #             SKP(byte1, byte2)
            #         case 'A':
            #             SKNP(byte1, byte2)
            # case 'F':
            #     match utils.get_nibble(byte2, 1):
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

    # def SYS(self, byte1, byte2):

    # def CLS(self, byte1, byte2):


    def JP_ADDR(self, byte1, byte2):
        '''
        Jump to location nnn.

        The interpreter sets the program counter to nnn.
        '''
        location = '0x0' + utils.last_three_nibbles(byte1, byte2)
        self.memory.program_counter = location


    def CALL(self, byte1, byte2):
        '''
        Call subroutine at nnn.

        The interpreter increments the stack pointer, then puts the current PC on the top of the stack. 
        The PC is then set to nnn.
        '''
        self.memory.addr_stack.increment_stack_ptr()
        self.memory.addr_stack.push_addr(self.memory.program_counter)

        location = '0x0' + utils.last_three_nibbles(byte1, byte2)
        self.memory.program_counter = location


    def SE_BYTE(self, byte1, byte2):
        '''
        Skip next instruction if Vx = kk.

        The interpreter compares register Vx to kk, and if they are equal, increments the program counter by 2.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)

        if (self.memory.registers.mem_get(second_nibble) == self.memory.registers.mem_get(byte2)):
            self.memory.increment_pc()


    def SNE(self, byte1, byte2):
        '''
        Skip next instruction if Vx != kk.

        The interpreter compares register Vx to kk, and if they are not equal, increments the program counter by 2.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)
        
        if (self.memory.registers.mem_get(second_nibble) != self.memory.registers.mem_get(byte2)):
            self.memory.increment_pc()


    def SE_REG(self, byte1, byte2):
        '''
        Skip next instruction if Vx = Vy.

        The interpreter compares register Vx to register Vy, and if they are equal, increments the program counter by 2.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)
        third_nibble = utils.get_nibble_byte(byte2, 1)

        if (self.memory.registers.mem_get(second_nibble) == self.memory.registers.mem_get(third_nibble)):
            self.memory.increment_pc()


    def LD_BYTE(self, byte1, byte2):
        '''
        Set Vx = kk.

        The interpreter puts the value kk into register Vx.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)
        self.memory.registers.mem_set(second_nibble, byte2)


    def ADD_BYTE(self, byte1, byte2):
        '''
        Set Vx = Vx + kk.

        Adds the value kk to the value of register Vx, then stores the result in Vx. 
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)
        self.memory.registers.mem_set(second_nibble, utils.add_bytes(self.memory.registers.mem_get(second_nibble), byte2))


    def LD_REG(self, byte1, byte2):
        '''
        Set Vx = Vy.

        Stores the value of register Vy in register Vx.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)
        third_nibble = utils.get_nibble_byte(byte2, 1)

        self.memory.registers.mem_set(second_nibble, self.memory.registers.mem_get(third_nibble))


    def OR(self, byte1, byte2):
        '''
        Set Vx = Vx OR Vy.

        Performs a bitwise OR on the values of Vx and Vy, then stores the result in Vx. 
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)
        third_nibble = utils.get_nibble_byte(byte2, 1)

        reg1_val = self.memory.registers.mem_get(second_nibble)
        reg2_val = self.memory.registers.mem_get(third_nibble)

        self.memory.registers.mem_set(second_nibble, utils.or_bytes(reg1_val, reg2_val))


    def AND(self, byte1, byte2):
        '''
        Set Vx = Vx AND Vy.

        Performs a bitwise AND on the values of Vx and Vy, then stores the result in Vx.      
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)
        third_nibble = utils.get_nibble_byte(byte2, 1)

        reg1_val = self.memory.registers.mem_get(second_nibble)
        reg2_val = self.memory.registers.mem_get(third_nibble)

        self.memory.registers.mem_set(second_nibble, utils.and_bytes(reg1_val, reg2_val))


    def XOR(self, byte1, byte2):
        '''
        Set Vx = Vx XOR Vy.

        Performs a bitwise exclusive OR on the values of Vx and Vy, then stores the result in Vx.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)
        third_nibble = utils.get_nibble_byte(byte2, 1)

        reg1_val = self.memory.registers.mem_get(second_nibble)
        reg2_val = self.memory.registers.mem_get(third_nibble)

        self.memory.registers.mem_set(second_nibble, utils.xor_bytes(reg1_val, reg2_val))


    def ADD_REG(self, byte1, byte2):
        '''
        Set Vx = Vx + Vy, set VF = carry.

        The values of Vx and Vy are added together. 
        If the result is greater than 8 bits (i.e., > 255,) VF is set to 1, otherwise 0. 
        Only the lowest 8 bits of the result are kept, and stored in Vx.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)
        third_nibble = utils.get_nibble_byte(byte2, 1)

        reg1_val = self.memory.registers.mem_get(second_nibble)
        reg2_val = self.memory.registers.mem_get(third_nibble)

        if (int(utils.add_bytes(reg1_val, reg2_val), 16) <= 255):
            self.memory.registers.mem_set(second_nibble, utils.add_bytes(reg1_val, reg2_val))
            self.memory.registers.mem_set('0x0F', '0x00')
        else:
            self.memory.registers.mem_set('0x0F', '0x01')
            op_res = utils.add_bytes(reg1_val, reg2_val)
            setval = utils.mask_to_byte(op_res)
            self.memory.registers.mem_set(second_nibble, setval)


    def SUB(self, byte1, byte2):
        '''
        Set Vx = Vx - Vy, set VF = NOT borrow.

        If Vx > Vy, then VF is set to 1, otherwise 0. Then Vy is subtracted from Vx, and the results stored in Vx.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)
        third_nibble = utils.get_nibble_byte(byte2, 1)

        reg1_val = self.memory.registers.mem_get(second_nibble)
        reg2_val = self.memory.registers.mem_get(third_nibble)

        if (int(reg1_val, 16) > int(reg2_val, 16)):
            self.memory.registers.mem_set('0x0F', '0x01')
            self.memory.registers.mem_set(second_nibble, utils.sub_bytes(reg1_val, reg2_val))
        else:
            self.memory.registers.mem_set('0x0F', '0x00')
            self.memory.registers.mem_set(second_nibble, utils.sub_bytes(reg1_val, reg2_val))
        

    def SHR(self, byte1, byte2):
        '''
        Set Vx = Vx SHR 1.

        If the least-significant bit of Vx is 1, then VF is set to 1, otherwise 0. Then Vx is divided by 2.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)
        reg1_val = self.memory.registers.mem_get(second_nibble)

        self.memory.registers.mem_set(second_nibble, hex(int(reg1_val, 16) >> 1))
        
        bin_val = bin(int(reg1_val, 16))

        if (bin_val[-1] == '1'):
            self.memory.registers.mem_set('0x0F', '0x01')
        else:
            self.memory.registers.mem_set('0x0F', '0x00')


    def SUBN(self, byte1, byte2):
        '''
        Set Vx = Vy - Vx, set VF = NOT borrow.

        If Vy > Vx, then VF is set to 1, otherwise 0. Then Vx is subtracted from Vy, and the results stored in Vx.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)
        third_nibble = utils.get_nibble_byte(byte2, 1)

        reg1_val = self.memory.registers.mem_get(second_nibble)
        reg2_val = self.memory.registers.mem_get(third_nibble)

        if (int(reg2_val, 16) > int(reg1_val, 16)):
            self.memory.registers.mem_set('0x0F', '0x01')
            self.memory.registers.mem_set(second_nibble, utils.sub_bytes(reg2_val, reg1_val))
        else:
            self.memory.registers.mem_set('0x0F', '0x00')
            self.memory.registers.mem_set(second_nibble, utils.sub_bytes(reg2_val, reg1_val))


    def SHL(self, byte1, byte2):
        '''
        Set Vx = Vx SHL 1.

        If the most-significant bit of Vx is 1, then VF is set to 1, otherwise to 0. 
        Then Vx is multiplied by 2.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)
        reg1_val = self.memory.registers.mem_get(second_nibble)

        self.memory.registers.mem_set(second_nibble, hex(int(reg1_val, 16) << 1))

        bin_val = bin(int(reg1_val, 16))

        # HACK: This is a hacky way to check the most significant bit
        # Size of bin_val is 10 because of the '0b' prefix, so we check the 3rd index
        if (len(bin_val) < 10):
            self.memory.registers.mem_set('0x0F', '0x00')
        else:
            if (bin_val[2] == '1'):
                self.memory.registers.mem_set('0x0F', '0x01')
            else:
                self.memory.registers.mem_set('0x0F', '0x00')


    def SNE(self, byte1, byte2):
        '''
        Skip next instruction if Vx != Vy.

        The values of Vx and Vy are compared, and if they are not equal, the program counter is increased by 2.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)
        third_nibble = utils.get_nibble_byte(byte2, 1)

        reg1_val = self.memory.registers.mem_get(second_nibble)
        reg2_val = self.memory.registers.mem_get(third_nibble)

        if (reg1_val != reg2_val):
            # TODO make a program_counter a MemObj and use the mem_set method
            self.memory.program_counter = utils.add_bytes(self.memory.program_counter, '0x02')


    def LD_ADDR(self, byte1, byte2): 
        '''
        Set I = nnn.

        The value of register I is set to nnn.
        '''
        two_bytes = utils.last_three_nibbles_byte(byte1, byte2)
        self.memory.index_reg.mem_set('0x00', two_bytes)

    
    def JP_LOC_ADDR(self, byte1, byte2):
        '''
        Jump to location nnn + V0.

        The program counter is set to nnn plus the value of V0.
        '''
        two_bytes = utils.last_three_nibbles_byte(byte1, byte2)
        # TODO make a program_counter a MemObj and use the mem_set method
        self.memory.program_counter = utils.add_bytes(two_bytes, self.memory.registers.mem_get('0x00'))

    
    def RND(self, byte1, byte2):
        '''
        Set Vx = random byte AND kk.

        The interpreter generates a random number from 0 to 255, which is then ANDed with the value kk. 
        The results are stored in Vx. See instruction 8xy2 for more information on AND.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)

        random_byte = hex(randint(0, 255))
        self.memory.registers.mem_set(second_nibble, utils.and_bytes(random_byte, byte2))

    
    def DRW(self, byte1, byte2):
        pass

    
    def SKP(self, byte1, byte2):
        pass

    
    def SKNP(self, byte1, byte2):
        pass

    
    def LD_DEL_TIMER(self, byte1, byte2):
        pass

    
    def LD_S_TIMER(self, byte1, byte2):
        pass

    
    def ADD_LOC(self, byte1, byte2):
        pass

    
    def LD_SPRITE(self, byte1, byte2):
        pass

    
    def LD_BCD(self, byte1, byte2):
        pass

    
    def LD_MEM_LOC(self, byte1, byte2):
        pass

    
    def LD_READ_LOC(self, byte1, byte2):
        pass
