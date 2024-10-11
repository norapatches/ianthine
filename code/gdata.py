from settings import *

class GameData:
    def __init__(self, ui, screen: pygame.Surface) -> None:
        self.ui = ui
        self.screen = screen
        
        # PLAYER
        self._health: int = 5
        self._coins: int = 0
        self._gems: int = 0
        self.key: bool = False
        self.can_double_jump: bool = False
        self.can_walljump: bool = False
        
        self.ui.create_hearts(self.health)
        
        # GAME PROGRESS
        self.unlocked_level: int = 0
        self.current_level: int = 0
        
        # GRAPHIC SETTINGS
        self.window_ratio: str = '16:9'
        self.graphic_filter = None
        self.filter_invert: bool = False
        
        # CAMERA SETTINGS
        self.camera_type: str = 'box'
        
        # AUDIO SETTINGS
        self.bgm_volume: float = 1.0
        self.sfx_volume: float = 1.0
        
        # CONTROL SETTINGS
        self.control_scheme: int = 0
        
        # PAUSE/RESUME
        self.paused: bool = False
    
    # player health
    @property
    def health(self) -> int:
        return self._health
    
    @health.setter
    def health(self, value: int) -> None:
        self._health = value
        self.ui.create_hearts(value)

    # player coins
    @property
    def coins(self):
        return self._coins
    
    @coins.setter
    def coins(self, value: int):
        self._coins = value
    
    # player gems
    @property
    def gems(self) -> int:
        return self._gems
    
    @gems.setter
    def gems(self, value: int) -> None:
        self._gems = value