from pygame.time import get_ticks

class Timer:
    def __init__(self, duration, func= None, repeat = False) -> None:
        '''An instance of a timer that can also be used to execute a function'''
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False
        self.repeat = repeat
    
    def start(self) -> None:
        '''Start the timer'''
        self.active = True
        self.start_time = get_ticks()
    
    def stop(self) -> None:
        '''Stop the timer. If repeat is enabled, the timer starts again'''
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.start()
    
    def update(self) -> None:
        '''The update method'''
        current_time = get_ticks()
        if current_time - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.stop()