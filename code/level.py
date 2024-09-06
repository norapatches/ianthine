from settings import *
from sprites import Sprite, AnimatedSprite, MovingSprite, Floor, CollapseFloor, ParticleEffect
from camera import CameraGroup

from npc import Creature, Ghost, Snail
from enemies import Crawler, Soldier
from player import Player, Projectile

class Level:
    def __init__(self, tmx_map, level_frames, data) -> None:
        self.display = pygame.display.get_surface()
        self.data = data
        
        # level data
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_height = tmx_map.height * TILE_SIZE
        
        # groups
        self.all_sprites = CameraGroup(
            width= tmx_map.width,
            height= tmx_map.height
        )
        
        self.collision_sprites = pygame.sprite.Group()          # floor
        self.collapse_sprites = pygame.sprite.Group()           # collapsing floor
        self.semi_collision_sprites = pygame.sprite.Group()     # platforms
        self.damage_sprites = pygame.sprite.Group()             # anything that damages player
        self.snail_collision_sprites = pygame.sprite.Group()    # snails
        self.enemy_sprites = pygame.sprite.Group()              # enemies
        self.projectile_sprites = pygame.sprite.Group()         # projectiles
        
        self.setup(tmx_map, level_frames)
        
        # frames
        self.particle_frames = level_frames['particle']
    
    def setup(self, tmx_map, level_frames) -> None:
        '''Read tile and object layers from tmx map file'''
        
        # tiles
        for layer in ['bg', 'terrain', 'terrain_hidden', 'terrain_collapse', 'platform']:
            for x, y, surface in tmx_map.get_layer_by_name(layer).tiles():
                if layer == 'terrain':
                    Floor((x * TILE_SIZE, y * TILE_SIZE), surface, (self.all_sprites, self.collision_sprites))
                if layer == 'terrain_hidden':
                    Floor((x * TILE_SIZE, y * TILE_SIZE), surface, (self.all_sprites, self.collision_sprites), hidden=True)
                if layer == 'terrain_collapse':
                    CollapseFloor((x * TILE_SIZE, y * TILE_SIZE), surface, (self.all_sprites, self.collision_sprites, self.collapse_sprites))
                if layer == 'platform':
                    Floor((x * TILE_SIZE, y * TILE_SIZE), surface, (self.all_sprites, self.semi_collision_sprites))
                else:
                    Sprite((x * TILE_SIZE, y * TILE_SIZE), surface, self.all_sprites, Z_LAYERS['bg_tiles'])
        
        # spikes
        for x, y, surface in tmx_map.get_layer_by_name('spike').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surface, (self.all_sprites, self.collision_sprites, self.damage_sprites))
        
        # NPC
        for obj in tmx_map.get_layer_by_name('npc'):
            if obj.name == 'ghost':
                Ghost((obj.x, obj.y), level_frames['ghost'], self.all_sprites)
            if obj.name == 'snail':
                Snail((obj.x, obj.y), level_frames['snail'], (self.all_sprites, self.snail_collision_sprites), self.collision_sprites)
        
        # objects
        for obj in tmx_map.get_layer_by_name('objects'):
            if obj.name == 'player':
                self.player = Player(
                    position= (obj.x, obj.y),
                    groups= self.all_sprites,
                    collision_sprites= self.collision_sprites,
                    semi_collision_sprites= self.semi_collision_sprites,
                    snail_sprites= self.snail_collision_sprites,
                    frames= level_frames['player'],
                    projectile=self.create_projectile,
                    data= self.data
                )
        
        # moving objects
        for obj in tmx_map.get_layer_by_name('moving_objects'):
            frames = level_frames[obj.name]
            groups = (self.all_sprites, self.semi_collision_sprites) if obj.properties['platform'] else (self.all_sprites, self.damage_sprites)
            if obj.width > obj.height:
                move_direction = 'x'
                start_pos = (obj.x, obj.y + obj.height / 2)
                end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
            else:
                move_direction = 'y'
                start_pos = (obj.x + obj.width / 2, obj.y)
                end_pos = (obj.x + obj.width / 2, obj.y + obj.height)
            speed = obj.properties['speed']
            MovingSprite(frames, groups, start_pos, end_pos, move_direction, speed)
        
        # enemies
        for obj in tmx_map.get_layer_by_name('enemies'):
            if obj.name == 'soldier':
                Soldier((obj.x, obj.y), level_frames['soldier'], (self.all_sprites, self.enemy_sprites), self.collision_sprites)
            if obj.name == 'crawler':
                Crawler((obj.x, obj.y), level_frames['crawler'], (self.all_sprites, self.damage_sprites), self.collision_sprites)
    
    def melee_collision(self) -> None:
        for target in self.enemy_sprites.sprites():
            facing_target = self.player.rect.centerx < target.rect.centerx and self.player.facing_right or\
                            self.player.rect.centerx > target.rect.centerx and not self.player.facing_right
            if target.rect.colliderect(self.player.rect) and self.player.melee_atk and facing_target:
                target.reverse()
    
    def ranged_collision(self) -> None:
        groups = self.collision_sprites.sprites() + self.enemy_sprites.sprites()
        for sprite in groups:
            sprite = pygame.sprite.spritecollide(sprite, self.projectile_sprites, True)
            if sprite:
                ParticleEffect((sprite[0].rect.center), self.particle_frames, self.all_sprites)
    
    def create_projectile(self, position, direction) -> None:
        Projectile(position, (self.all_sprites, self.projectile_sprites), direction, 128)
    
    def run(self, dt):
        '''Run the given level, update all sprites, center camera around player'''
        
        self.all_sprites.update(dt)
        self.data.ui.sprites.update(dt)
        
        self.melee_collision()
        self.ranged_collision()
        
        self.all_sprites.draw(self.player.hitbox_rect.center, dt)
        
        self.data.ui.sprites.draw(self.display)