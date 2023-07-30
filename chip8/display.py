from . import utils

class Display:
    width = 64
    height = 32

    def __init__(self, emulator_ui=None):
        # 64 x 32 display
        self.screen = [[0 for i in range(self.width)] for j in range(self.height)]
        self.emulator_ui = emulator_ui
    

    def draw_pixel(self, x, y, val):
        '''
        Set a bit on the screen given an x and y coordinate and a value.

        Returns 1 if a pixel was erased, 0 otherwise.
        '''
        screen_val = self.screen[y][x]

        # XOR the value with the screen value
        if (screen_val ^ val):
            self.screen[y][x] = 1
            if self.emulator_ui:
                self.emulator_ui.draw_pixel(x, y, 1)
            return 0
        else:
            self.screen[y][x] = 0
            if self.emulator_ui:
                self.emulator_ui.draw_pixel(x, y, 0)
            return 1
    

    def process_bytes(self, x_init, y_init, byte_list):
        '''
        Given an initial x and y coordinate, and a list of bytes, draw the
        bytes on the screen. Returns 1 if a pixel was erased, 0 otherwise.
        '''
        x = x_init
        y = y_init
        pixel_erased = 0

        for byte in byte_list:
            byte_bin = utils.get_byte_bin(byte)

            if y < self.height:
                for bit in byte_bin:
                    if x < self.width:
                        pixel_erased += self.draw_pixel(x, y, int(bit))
                        x += 1
                x = x_init
                y += 1
            else:
                break
        
        return pixel_erased
    

    def clear_screen(self):
        '''
        Clear the screen.
        '''
        self.screen = [[0 for i in range(self.width)] for j in range(self.height)]