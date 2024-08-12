from settings import *
from sprites import Sprite, Floor, Door
from camera import CameraGroup
from enemies import Snail
from npc import Ghost
from player import Player

class Level:
    def __init__(self, tmx_map, level_frames) -> None:
        self.display = pygame.display.get_surface()
        
        # level data
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_height = tmx_map.height * TILE_SIZE
        
        # groups
        self.all_sprites = CameraGroup(
            width= tmx_map.width,
            height= tmx_map.height
        )
        
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map, level_frames)
    
    def setup(self, tmx_map, level_frames):
        
        # tiles
        for layer in ['bg', 'bg_details', 'terrain', 'platform']:
            for x, y, surface in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'terrain':
                    Floor((x * TILE_SIZE, y * TILE_SIZE), surface, (self.all_sprites, self.collision_sprites))
                if layer == 'platform': groups.append(self.semi_collision_sprites)
                
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surface, groups, Z_LAYERS['bg_tiles'])
        
        # spikes
        for x, y, surface in tmx_map.get_layer_by_name('spike').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surface, (self.all_sprites, self.collision_sprites))
        
        # NPC
        for obj in tmx_map.get_layer_by_name('npc'):
            if obj.name == 'ghost':
                Ghost((obj.x, obj.y), level_frames['ghost'], self.all_sprites)
        
        for obj in tmx_map.get_layer_by_name('snail'):
            if obj.name == 'snail':
                Snail((obj.x, obj.y), level_frames['snail'], (self.all_sprites, self.semi_collision_sprites), self.collision_sprites)
        
        # door
        for obj in tmx_map.get_layer_by_name('doors'):
            if obj.name == 'door':
                Door((obj.x, obj.y), surface, self.all_sprites)
        
        # player
        for obj in tmx_map.get_layer_by_name('player'):
            if obj.name == 'player':
                self.player = Player(
                    position= (obj.x, obj.y),
                    groups= self.all_sprites,
                    collision_sprites= self.collision_sprites,
                    semi_collision_sprites= self.semi_collision_sprites,
                    frames= level_frames['player']
                )
    
    def run(self, dt):
        self.display.fill('black')
        
        self.all_sprites.update(dt)
        
        self.all_sprites.draw(self.player.rect.center, dt)