from settings import *

'''TODO: Rewrite the class to represent player and enemies with different health'''

class GameData:
    def __init__(self, ui) -> None:
        self.ui = ui
        
        # PLAYER
        self._health: int = 5
        self._coins: int = 0
        self._gems: int = 0
        self.key: bool = False
        
        # GAME PROGRESS
        self.unlocked_level: int = 0
        self.current_level: int = 0
        
        # GRAPHIC SETTINGS
        self.graphic_filter = None
        self.filter_invert: bool = False
        
        # AUDIO SETTINGS
        self.bgm_volume: float = 1.0
        self.sfx_volume: float = 1.0
        
        # CONTROL SETTINGS
        self.control_scheme: int = 0
        
        # PAUSE/RESUME
        self.paused: bool = False
    
    @property
    def health(self) -> int:
        return self._health
    
    @health.setter
    def health(self, value: int) -> None:
        self._health = value

    @property
    def coins(self):
        return self._coins
    
    @coins.setter
    def coins(self, value: int):
        self._coins = value
    
    @property
    def gems(self) -> int:
        return self._gems
    
    @gems.setter
    def gems(self, value: int) -> None:
        self._gems = value