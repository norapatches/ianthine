from pygame.time import get_ticks

class Timer:
    def __init__(self, duration, func= None, repeat = False) -> None:
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False
        self.repeat = repeat
    
    def start(self) -> None:
        self.active = True
        self.start_time = get_ticks()
    
    def stop(self) -> None:
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.start()
    
    def update(self) -> None:
        current_time = get_ticks()
        if current_time - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.stop()