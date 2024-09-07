from settings import *

'''TODO: Rewrite the class to represent player and enemies with different health'''

class GameData:
    def __init__(self, ui) -> None:
        self.ui = ui
        
        self._coins = 0
        self.key = False
        
        self._health = 5
        self.ui.create_hearts(self._health)
        
        self.unlocked_level = 0
        self.current_level = 0
        
        self.paused = False
    
    @property
    def health(self) -> int:
        return self._health
    
    @health.setter
    def health(self, value) -> None:
        self._health = value
        self.ui.create_hearts(value)

    @property
    def coins(self):
        return self._coins
    
    @coins.setter
    def coins(self, value):
        self._coins = value
    