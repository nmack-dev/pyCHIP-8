import unittest
import keyboard
import time

from chip8.keypad import Keypad

class TestKeypad(unittest.TestCase):

    def test_is_pressed(self):
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

    
    def test_poll_all_keys(self):
        keypad = Keypad()

        time.sleep(0.15)

        poll_result = keypad.poll_all_keys()
        self.assertEqual(poll_result, -1)
        
        keyboard.press(2)
        time.sleep(0.15)
        self.assertEqual(keypad.poll_all_keys(), 1)
        keyboard.release(2)
        time.sleep(0.15)

        poll_result = keypad.poll_all_keys()
        self.assertEqual(poll_result, -1)

    
    # TODO someday
    def test_wait_for_key(self):
        pass


if __name__ == '__main__':
    unittest.main()