from .memory import Memory
from .display import Display
from .keypad import Keypad
from .emulator_ui import EmulatorUI
from . import utils

from random import randint

class Emulator:

    def __init__(self):
        self.memory = Memory()
        self.emulator_ui = EmulatorUI()
        self.display = Display(self.emulator_ui)
        self.keypad = Keypad()

    
    def load_rom(self, rom_path):
        '''
        Load a ROM into memory.
        '''
        self.memory.load_rom(rom_path)

    
    def run(self):
        '''
        Run the emulator.
        '''
        self.memory.program_counter = '0x200'
        
        while True:
            if int(self.memory.program_counter, 16) < self.memory.ram - 1:
                self.emulator_ui.root.update()

                byte1 = self.memory.memory.mem_get(self.memory.program_counter)
                byte2 = self.memory.memory.mem_get(utils.add_bytes(self.memory.program_counter, '0x1'))
                self.decode_instr(byte1, byte2)
                self.memory.increment_pc()


    def decode_instr(self, byte1, byte2):
        match utils.get_nibble(byte1, 1):
            case '0':
                self.CLS(byte1, byte2)
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
                    case '7':
                        self.SUBN(byte1, byte2)
                    case 'e':
                        self.SHL(byte1, byte2)
            case '9':
                self.SNE(byte1, byte2)
            case 'a':
                self.LD_ADDR(byte1, byte2) 
            case 'b':
                self.JP_LOC_ADDR(byte1, byte2)
            case 'c':
                self.RND(byte1, byte2) 
            case 'd':
                self.DRW(byte1, byte2)
            case 'e':
                match utils.get_nibble(byte2, 1):
                    case '9':
                        self.SKP(byte1, byte2)
                    case 'a':
                        self.SKNP(byte1, byte2)
            case 'f':
                match utils.get_nibble(byte2, 1):
                    case '0':
                        match utils.get_nibble(byte2, 2):
                            case '7':
                                self.LD_REG_DEL_TIMER(byte1, byte2)
                            case 'a':
                                self.LD_KEY(byte1, byte2)
                    case '1':
                        match utils.get_nibble(byte2, 2):
                            case '5':
                                self.LD_DEL_TIMER(byte1, byte2)
                            case '8':
                                self.LD_S_TIMER(byte1, byte2)
                            case 'e':
                                self.ADD_LOC(byte1, byte2)
                    case '2':
                        self.LD_SPRITE(byte1, byte2)
                    case '3':
                        self.LD_BCD(byte1, byte2)
                    case '5':
                        self.LD_MEM_LOC(byte1, byte2)
                    case '6':
                        self.LD_READ_LOC(byte1, byte2)


    def CLS(self, byte1, byte2):
        '''
        Clear the display.
        '''
        self.display.clear_screen()


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
        # TODO: this is wrong, fix
        '''
        Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.

        The interpreter reads n bytes from memory, starting at the address stored in I. These bytes are then
        displayed as sprites on screen at coordinates (Vx, Vy). Sprites are XORed onto the existing screen.
        If this causes any pixels to be erased, VF is set to 1, otherwise it is set to 0. If the sprite is
        positioned so part of it is outside the coordinates of the display, it wraps around to the opposite
        side of the screen.
        '''
        x_coord = int(self.memory.registers.mem_get(utils.get_nibble_byte(byte1, 2)), 16) % 64
        y_coord = int(self.memory.registers.mem_get(utils.get_nibble_byte(byte2, 1)), 16) % 32
        num_bytes = int(utils.get_nibble_byte(byte2, 2), 16)

        self.memory.registers.mem_set('0x0F', '0x00')

        byte_list = []

        for _ in range(num_bytes):
            working_byte = self.memory.memory.mem_get(self.memory.index_reg.mem_get('0x00'))
            byte_list.append(working_byte)
            self.memory.index_reg.mem_set('0x00', utils.add_bytes(self.memory.index_reg.mem_get('0x00'), '0x01'))
        
        self.display.process_bytes(x_coord, y_coord, byte_list)
        

    def SKP(self, byte1, byte2):
        '''
        Skip next instruction if key with the value of Vx is pressed.

        Checks the keyboard, and if the key corresponding to the value of Vx is currently in the down position,
        PC is increased by 2.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)
        key = int(self.memory.registers.mem_get(second_nibble), 16)

        if self.keypad.is_pressed(key):
            # TODO make a program_counter a MemObj and use the mem_set method
            # TODO add default value of 0x00 for MemObj
            self.memory.program_counter = utils.add_bytes(self.memory.program_counter, '0x02')

    
    def SKNP(self, byte1, byte2):
        '''
        Skip next instruction if key with the value of Vx is not pressed.

        Checks the keyboard, and if the key corresponding to the value of Vx is currently in the up position,
        PC is increased by 2.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)
        key = int(self.memory.registers.mem_get(second_nibble), 16)

        if not self.keypad.is_pressed(key):
            # TODO make a program_counter a MemObj and use the mem_set method
            # TODO add default value of 0x00 for MemObj
            self.memory.program_counter = utils.add_bytes(self.memory.program_counter, '0x02')


    def LD_REG_DEL_TIMER(self, byte1, byte2):
        '''
        Set Vx = delay timer value.

        The value of DT is placed into Vx.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)

        self.memory.registers.mem_set(second_nibble, self.memory.delay_timer.mem_get('0x00'))


    def LD_KEY(self, byte1, byte2):
        '''
        Wait for a key press, store the value of the key in Vx.

        All execution stops until a key is pressed, then the value of that key is stored in Vx.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)

        self.memory.delay_timer.timer.stop()

        self.memory.registers.mem_set(second_nibble, self.keypad.wait_for_key())

        self.memory.delay_timer.timer.resume()

    
    def LD_DEL_TIMER(self, byte1, byte2):
        '''
        Set delay timer = Vx.

        DT is set equal to the value of Vx.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)
        val = self.memory.registers.mem_get(second_nibble)

        self.memory.load_delay_timer(val)

    
    def LD_S_TIMER(self, byte1, byte2):
        '''
        Set sound timer = Vx.

        ST is set equal to the value of Vx.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)
        val = self.memory.registers.mem_get(second_nibble)

        self.memory.load_sound_timer(val)

    
    def ADD_LOC(self, byte1, byte2):
        '''
        Set I = I + Vx.

        The values of I and Vx are added, and the results are stored in I.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)

        self.memory.add_to_index_reg(second_nibble)

    
    def LD_SPRITE(self, byte1, byte2):
        '''
        Set I = location of sprite for digit Vx.

        The value of I is set to the location for the hexadecimal sprite corresponding to the value of Vx.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)

        self.memory.load_sprite(second_nibble)

    
    def LD_BCD(self, byte1, byte2):
        '''
        Store BCD representation of Vx in memory locations I, I+1, and I+2.

        The interpreter takes the decimal value of Vx, and places the hundreds digit in memory at location in I,
        the tens digit at location I+1, and the ones digit at location I+2.
        '''
        second_nibble = utils.get_nibble_byte(byte1, 2)

        val = str(int(self.memory.registers.mem_get(second_nibble), 16))

        # TODO this is awful but it probably works
        mem_loc = self.memory.index_reg.mem_get('0x00')

        for digit in val:
            self.memory.memory.mem_set(mem_loc, digit)
            mem_loc = utils.add_bytes(mem_loc, '0x01')

    
    def LD_MEM_LOC(self, byte1, byte2):
        '''
        Store registers V0 through Vx in memory starting at location I.

        The interpreter copies the values of registers V0 through Vx into memory, starting at the address in I.
        '''
        second_nibble = int(utils.get_nibble_byte(byte1, 2), 16)

        mem_loc = self.memory.index_reg.mem_get('0x00')

        for i in range(second_nibble + 1):
            self.memory.memory.mem_set(mem_loc, self.memory.registers.mem_get(hex(i)))
            mem_loc = utils.add_bytes(mem_loc, '0x01')

    
    def LD_READ_LOC(self, byte1, byte2):
        '''
        Read registers V0 through Vx from memory starting at location I.

        The interpreter reads values from memory starting at location I into registers V0 through Vx.
        '''
        second_nibble = int(utils.get_nibble_byte(byte1, 2), 16)

        mem_loc = self.memory.index_reg.mem_get('0x00')

        for i in range(second_nibble + 1):
            mem_val = self.memory.memory.mem_get(mem_loc)
            self.memory.registers.mem_set(hex(i), mem_val)
