import unittest
import keyboard
import time

from chip8.keypad import Keypad

class TestKeypad(unittest.TestCase):

    def test_is_pressed(self):
        pass

        keypad = Keypad()

        self.assertEqual(keypad.is_pressed(1), False)
        keyboard.press(2)
        time.sleep(0.15)
        self.assertEqual(keypad.is_pressed(1), True)
        keyboard.release(2)

        self.assertEqual(keypad.is_pressed(10), False)
        keyboard.press(46)
        time.sleep(0.15)
        self.assertEqual(keypad.is_pressed(10), True)
        keyboard.release(46)


if __name__ == '__main__':
    unittest.main()