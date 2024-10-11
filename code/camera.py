from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gdata import GameData

from settings import *


class CameraGroup(pygame.sprite.Group):
    def __init__(self, width: int, height: int, data: GameData) -> None:
        '''The CameraGroup serves as a moving zoomed-in display surface that displays all sprites on level stages'''
        super().__init__()
        self.data: GameData = data
        #self.ui_sprites = [sprite for sprite in data.ui.sprites]
        
        self.display: pygame.Surface = pygame.display.get_surface()
        self.screen: pygame.Surface = data.screen
        self.screen_rect: pygame.FRect = self.screen.get_frect()
        self.offset: vector = vector()
        self.width: int = width * TILE_SIZE
        self.height: int = height * TILE_SIZE
        
        # minimap
        self.minimap = MiniMap(width, height)
        
        # camera boundaries
        self.borders: dict[str, int] = {
            'left': 0,
            'right': -self.width + SCREEN_WIDTH,
            'bottom': -self.height + SCREEN_HEIGHT,
            'top': 0
        }
        
        # camera box
        self.camera_bounds: dict[str, int] = {'left': 80, 'right': 80, 'top': 48, 'bottom': 48}
        self.camera_box = pygame.FRect((self.screen_rect.left + self.camera_bounds['left'],
                                        self.screen_rect.top + self.camera_bounds['top']),
                                       (self.screen_rect.width - (self.camera_bounds['left'] + self.camera_bounds['right']),
                                        self.screen_rect.height - (self.camera_bounds['top'] + self.camera_bounds['bottom'])))
    
    def camera_constraint(self) -> None:
        '''Don't allow camera movement when reaching level stage sides'''
        self.offset.x = self.offset.x if self.offset.x < self.borders['left'] else 0
        self.offset.x = self.offset.x if self.offset.x > self.borders['right'] else self.borders['right']
    
    def target_center_camera(self, target: pygame.FRect) -> None:
        self.offset.x = -(target.centerx - SCREEN_WIDTH / 2)
        self.offset.y = -(target.centery - SCREEN_HEIGHT / 2)
    
    def box_target_camera(self, target: pygame.FRect) -> None:
        if target.left < self.camera_box.left:
            self.camera_box.left = target.left
        if target.right > self.camera_box.right:
            self.camera_box.right = target.right
        if target.top < self.camera_box.top:
            self.camera_box.top = target.top
        if target.bottom > self.camera_box.bottom:
            self.camera_box.bottom = target.bottom
        
        self.offset.x = -self.camera_box.left + self.camera_bounds['left']
        self.offset.y = -self.camera_box.top + self.camera_bounds['top']
    
    def toggle_minimap(self) -> None:
        '''Show minimap while holding M key'''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            self.display.blit(self.minimap.scaled_surface, (10, WINDOW_HEIGHT - self.minimap.scaled_surface.height - 10))
    
    def draw(self, target: pygame.FRect, dt: float):
        '''The custom draw method for the CameraGroup that draws in Z layer order'''
        
        self.box_target_camera(target)
        #self.target_center_camera(target)
        self.camera_constraint()
        
        self.minimap.update(self.sprites())
        
        self.screen.fill('black')
        
        for sprite in sorted(self, key= lambda sprite: sprite.z):
            offset_pos = round(sprite.rect.left + self.offset.x), round(sprite.rect.top + self.offset.y)
            #offset_pos = sprite.rect.topleft + self.offset
            self.screen.blit(sprite.image, offset_pos)
        
        #for sprite in self.ui_sprites:
        #    self.screen.blit(sprite.image, sprite.rect)
        
        #pygame.transform.scale(self.screen, (WINDOW_WIDTH, WINDOW_HEIGHT), self.display)
        #self.display.blit(pygame.transform.scale(self.screen, (1280, 720)), (43, 24))
        
        self.toggle_minimap()


class MiniMap:
    def __init__(self, width: int, height: int) -> None:
        '''A MiniMap surface that displays terrain and player position'''
        self.surface = pygame.Surface((width, height))
        self.scaled_surface = pygame.Surface((320, 240))
    
    def update(self, sprites: list) -> None:
        '''Update sprite positions'''
        self.scaled_surface.fill('black')
        self.surface.fill('black')
        
        for sprite in sprites:
            if hasattr(sprite, 'map_image'):
                self.surface.blit(sprite.map_image, (sprite.map_rect))
        
        scaled = pygame.transform.scale(self.surface, self.scaled_surface.size)
        self.scaled_surface.blit(scaled, (0, 0))


class OverworldCamera(pygame.sprite.Group):
    def __init__(self, width: int, height: int, data: GameData) -> None:
        super().__init__()
        self.display = pygame.display.get_surface()
        #self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen = data.screen
        self.data = data
        self.offset = vector()
        
        self.width, self.height = width * TILE_SIZE, height * TILE_SIZE
        
        # camera boundaries
        self.borders = {
            'left': 0,
            'right': -self.width + SCREEN_WIDTH,
            'bottom': -self.height + SCREEN_HEIGHT,
            'top': 0
        }
    
    def camera_constraint(self) -> None:
        '''Don't allow camera movement when reaching level stage sides'''
        self.offset.x = self.offset.x if self.offset.x < self.borders['left'] else 0
        self.offset.x = self.offset.x if self.offset.x > self.borders['right'] else self.borders['right']
        
        self.offset.y = self.offset.y if self.offset.y < self.borders['top'] else 0
        self.offset.y = self.offset.y if self.offset.y > self.borders['bottom'] else self.borders['bottom']
    
    def draw(self, target: pygame.FRect) -> None:
        self.screen.fill('black')
        
        self.offset.x = -(target.centerx - SCREEN_WIDTH / 2)
        self.offset.y = -(target.centery - SCREEN_HEIGHT / 2)
        
        self.camera_constraint()
        
        # background
        for sprite in sorted(self, key= lambda sprite: sprite.z):
            if sprite.z < Z_LAYERS['main']:
                if sprite.z == Z_LAYERS['path']:
                    if sprite.level <= self.data.unlocked_level:
                        self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)
                else:
                    self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)
        
        # main
        for sprite in sorted(self, key= lambda sprite: sprite.rect.centery):
            if sprite.z == Z_LAYERS['main']:
                if hasattr(sprite, 'icon'):
                    self.screen.blit(sprite.image, sprite.rect.topleft + self.offset + vector(0, -8))
                else:
                    self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)
        
        pygame.transform.scale(self.screen, (WINDOW_WIDTH, WINDOW_HEIGHT), self.display)
        