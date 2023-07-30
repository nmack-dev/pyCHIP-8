import unittest

from chip8.display import Display

class TestDisplay(unittest.TestCase):

    def test_draw_pixel(self):
        display = Display()

        self.assertEqual(display.draw_pixel(0, 0, 1), 0)
        self.assertEqual(display.draw_pixel(0, 0, 1), 1)


    def test_process_bytes(self):
        display = Display()

        # Test drawing a single byte
        self.assertEqual(display.process_bytes(0, 0, ['0xFF']), 0)

        for _ in range(8):
            self.assertEqual(display.screen[0][_], 1)

        self.assertEqual(display.screen[0][8], 0)

        display.clear_screen()

        # Test drawing two bytes
        self.assertEqual(display.process_bytes(0, 0, ['0xFF', '0xFF']), 0)

        for _ in range(8):
            self.assertEqual(display.screen[0][_], 1)
            self.assertEqual(display.screen[1][_], 1)

        self.assertEqual(display.screen[0][16], 0)

        display.clear_screen()

        # Test NOT rolling over to the next line
        self.assertEqual(display.process_bytes(60, 0, ['0xFF']), 0)

        for _ in range(60, 64):
            self.assertEqual(display.screen[0][_], 1)

        self.assertEqual(display.screen[0][1], 0)
        

if __name__ == '__main__':
    unittest.main()