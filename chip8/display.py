class Display:
    width = 64
    height = 32

    def __init__(self):
        # 64 x 32 display
        self.screen = [[0 for i in range(self.width)] for j in range(self.height)]
    

    def draw_pixel(self, x, y, val):
        '''
        Set a bit on the screen given an x and y coordinate and a value.

        Returns 1 if a pixel was erased, 0 otherwise.
        '''
        # TODO don't need to do this anymore
        # x_adj = x
        # y_adj = y

        # # wrap around if x or y is out of bounds
        # while (x_adj > (self.width - 1)):
        #     x_adj -= self.width
        
        # while (y_adj > (self.height - 1)):
        #     y_adj -= self.height

        screen_val = self.screen[y][x]

        # XOR the value with the screen value
        if (screen_val ^ val):
            self.screen[y][x] = 1
            return 0
        else:
            self.screen[y][x] = 0
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
            byte_bin = bin(int(byte, 16))[2:]

            for bit in byte_bin:
                if x > (self.width - 1):
                    x = 0
                    y += 1
                
                pixel_erased += self.draw_pixel(x, y, int(bit))
                x += 1
        
        return pixel_erased
    

    def clear_screen(self):
        '''
        Clear the screen.
        '''
        self.screen = [[0 for i in range(self.width)] for j in range(self.height)]