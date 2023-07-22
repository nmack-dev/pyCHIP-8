import time
import threading

class Timer:

    def __init__(self, start) -> None:
        self.start_time = start
        self.current = start
        self.running = False
        self.thread = threading.Thread(target=self.timer_task)
        # TODO remove because not needed???
        self.lock = threading.Lock()
    

    def timer_task(self) -> None:
        self.running = True

        while self.running:
            # Mutex here to protect global fields that may be accessed by other threads.
            # Yay synchronization!
            with self.lock:
                if self.current > 0:
                    self.current -= 1
                    time.sleep(0.01667)
                else:
                    self.running = False
        
    
    def start(self) -> None:
        self.thread.start()


    def set(self, val) -> None:
        self.running = False
        self.start_time = val
        self.current = val

    
    def reset(self) -> None:
        self.running = False
        self.current = self.start_time


    def stop(self) -> None:
        self.running = False

    
    def resume(self) -> None:
        self.running = True


class SoundTimer(Timer):

    def __init__(self, start) -> None:
        super().__init__(start)
    

    def start(self):
        super().start()