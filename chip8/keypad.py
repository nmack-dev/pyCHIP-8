import keyboard
import time

class Keypad:
    # Chip-8 Keypad Layout (hex, scancode)
    layout = {1  : 2,  2 : 3,  3  : 4,  12 : 5,
              4  : 17, 5 : 18, 6  : 19, 13 : 20,
              7  : 31, 8 : 32, 9  : 33, 14 : 34,
              10 : 46, 0 : 47, 11 : 48, 15 : 49}

    def __init__(self) -> None:
        pass


    def is_pressed(self, key) -> bool:
        if (self.layout.get(key) != None):
            return keyboard.is_pressed(self.layout.get(key))
        else:
            raise Exception('ERROR: Invalid key pressed')
    

    def poll_all_keys(self) -> int:
        for key in self.layout:
            if (keyboard.is_pressed(self.layout.get(key))):
                return key
        
        return -1
    

    def wait_for_key(self) -> bool:
        while (self.poll_all_keys() == -1):
            # TODO: This should block EVERYTHING else
            #       until a key is pressed. Figure out
            #       correct sleep value.
            time.sleep(0.05)