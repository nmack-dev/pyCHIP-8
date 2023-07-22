import unittest

from chip8.timer import Timer

class TestTimer(unittest.TestCase):

    def test_init(self):
        timer = Timer(10)

        self.assertEqual(timer.start_time, 10)
        self.assertEqual(timer.current, 10)
        self.assertEqual(timer.running, False)

    
    def test_start(self):
        del_timer = Timer(10)

        del_timer.start()
        self.assertEqual(del_timer.running, True)

    
    def test_set(self):
        del_timer = Timer(10)

        del_timer.set(5)
        self.assertEqual(del_timer.start_time, 5)
        self.assertEqual(del_timer.current, 5)

    
    def test_reset(self):
        del_timer = Timer(10)

        del_timer.reset()
        self.assertEqual(del_timer.current, 10)

    
    def test_stop(self):
        del_timer = Timer(10)

        del_timer.stop()
        self.assertEqual(del_timer.running, False)

    
    def test_resume(self):
        del_timer = Timer(10)

        del_timer.resume()
        self.assertEqual(del_timer.running, True)


if __name__ == '__main__':
    unittest.main()