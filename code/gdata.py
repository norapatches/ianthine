from settings import *

class GameData:
    def __init__(self, ui) -> None:
        self.ui = ui
        
        self._health = 5
        self.ui.create_hearts(self._health)
        
        self.unlocked_level = 0
        self.current_level = 0
    
    @property
    def health(self) -> int:
        return self._health
    
    @health.setter
    def health(self, value) -> None:
        self._health = value
        self.ui.create_hearts(value)
    