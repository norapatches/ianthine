from settings import *
from camera import CameraGroup
from gtimer import Timer
from pause import PauseScreen
from sprites import Sprite, MovingSprite, Door, Item, Floor, Platform, VFX

from npc import Creature, Snail
from enemies import Chaser, Crawler, Floater, Shooter, Skipper, Walker, Thorn
from enemy_boss import Golem, Boulder, Spike
from player import Player, Arrow

class Level:
    def __init__(self, tmx_map, level_frames: dict, data, fonts: dict, switch_stage: callable) -> None:
        self.display = pygame.display.get_surface()
        self.data = data
        self.switch_stage = switch_stage
        
        # level data
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_height = tmx_map.height * TILE_SIZE
        tmx_level_properties = tmx_map.get_layer_by_name('data')[0].properties
        self.level_unlock = tmx_level_properties['level_unlock']
        
        # pause screen
        self.pause_menu = PauseScreen(level_frames['items'], fonts, self.data)
        
        # all sprites
        self.all_sprites = CameraGroup(
            width= tmx_map.width,
            height= tmx_map.height,
            data= data
        )
        
        self.collision_sprites = pygame.sprite.Group()          # floor
        self.semi_collision_sprites = pygame.sprite.Group()     # platforms, moving platforms
        self.damage_sprites = pygame.sprite.Group()             # anything that damages player
        self.snail_collision_sprites = pygame.sprite.Group()    # snails
        self.enemy_sprites = pygame.sprite.Group()              # enemies
        self.projectile_sprites = pygame.sprite.Group()         # player projectiles
        self.enemy_projectile_sprites = pygame.sprite.Group()   # enemy projectiles
        self.item_sprites = pygame.sprite.Group()               # items
        
        self.interaction_sprites = pygame.sprite.Group()        # interactibles
        
        self.setup(tmx_map, level_frames)
        
        # frames
        self.vfx_frames = level_frames['vfx']
        self.interact_frames = level_frames['interact']
        self.arrow_frames = level_frames['arrow']
        
        # boss projectiles
        self.boss_boulder = level_frames['boulder']
        
        # timers
        self.timers = {
            'interaction_wait': Timer(1000)
        }
    
    def setup(self, tmx_map, level_frames: dict) -> None:
        '''Read tile and object layers from tmx map file'''
        
        # tiles
        for layer in ['bg', 'terrain', 'terrain_hidden', 'platform', 'spike']:
            for x, y, surface in tmx_map.get_layer_by_name(layer).tiles():
                if layer == 'terrain':
                    Floor((x * TILE_SIZE, y * TILE_SIZE), surface, (self.all_sprites, self.collision_sprites))
                if layer == 'terrain_hidden':
                    Floor((x * TILE_SIZE, y * TILE_SIZE), surface, (self.all_sprites, self.collision_sprites), hidden=True)
                if layer == 'platform':
                    Platform((x * TILE_SIZE, y * TILE_SIZE), surface, (self.all_sprites, self.semi_collision_sprites))
                if layer == 'spike':
                    Sprite((x * TILE_SIZE, y * TILE_SIZE), surface, (self.all_sprites, self.collision_sprites, self.damage_sprites))
                else:
                    # bg
                    Sprite((x * TILE_SIZE, y * TILE_SIZE), surface, self.all_sprites, Z_LAYERS['bg_tiles'])
        
        # NPC
        for obj in tmx_map.get_layer_by_name('npc'):
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
            if obj.name == 'door':
                self.door  = Door((obj.x, obj.y), level_frames['door'], (self.all_sprites, self.interaction_sprites))
            if obj.name == 'chest':
                self.chest = Sprite((obj.x, obj.y), level_frames['chest'][0], self.all_sprites, Z_LAYERS['bg_tiles'])
        
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
            if obj.name in ['skeleton', 'zombie']:
                Walker((obj.x, obj.y), level_frames[obj.name], (self.all_sprites, self.enemy_sprites), self.collision_sprites)
            if obj.name == 'crawler':
                Crawler((obj.x, obj.y), level_frames['crawler'], (self.all_sprites, self.enemy_sprites), self.collision_sprites)
            if obj.name in ['shadowman', 'horn']:
                Chaser((obj.x, obj.y), level_frames[obj.name], (self.all_sprites, self.enemy_sprites), self.collision_sprites, self.player)
            if obj.name == 'ghost':
                Floater((obj.x, obj.y), level_frames['ghost'], (self.all_sprites, self.enemy_sprites), self.player)
            if obj.name == 'golem':
                Golem((obj.x, obj.y), level_frames['golem'], (self.all_sprites, self.enemy_sprites), self.create_boss_boulder, self.create_boss_spike, self.player)
            if obj.name == 'plant':
                Shooter((obj.x, obj.y), level_frames['plant'], (self.all_sprites, self.enemy_sprites), self.player, self.create_enemy_projectile)
        
        # items
        for obj in tmx_map.get_layer_by_name('items'):
            Item(obj.name, (obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), level_frames['items'][obj.name], (self.all_sprites, self.item_sprites), self.data)
    
    def check_exit(self) -> None:
        # door
        if self.player.hitbox_rect.colliderect(self.door.rect) and self.player.interaction['do']:
            if self.data.key:
                self.data.key = False
                self.switch_stage('overworld', self.level_unlock)
            else:
                pass
    
    def melee_collision(self) -> None:
        for target in self.enemy_sprites:
            facing_target = self.player.rect.centerx < target.rect.centerx and self.player.facing_right or\
                            self.player.rect.centerx > target.rect.centerx and not self.player.facing_right
            if target.hitbox_rect.colliderect(self.player.rect) and self.player.melee_atk and facing_target:
                target.take_hit()
                VFX(target.rect.center, self.vfx_frames['punch'], self.all_sprites)
    
    def ranged_collision(self) -> None:
        groups = self.collision_sprites.sprites() + self.enemy_sprites.sprites()
        for sprite in groups:
            collision = pygame.sprite.spritecollide(sprite, self.projectile_sprites, pygame.sprite.collide_mask)
            if collision:
                if hasattr(sprite, 'enemy') and sprite.state != 'death':
                    sprite.take_hit()
                VFX((collision[0].rect.center), self.vfx_frames['particle'], self.all_sprites)
                collision[0].kill()
    
    def create_projectile(self, position, direction) -> None:
        Arrow(position, self.arrow_frames, (self.all_sprites, self.projectile_sprites), direction, 128)
    
    def create_enemy_projectile(self, position, direction) -> None:
        Thorn(position, (self.all_sprites, self.damage_sprites, self.enemy_projectile_sprites), direction, 56)
    
    def create_boss_boulder(self, position, direction) -> None:
        Boulder(position, self.boss_boulder, (self.all_sprites, self.damage_sprites), direction, 64)
    
    def create_boss_spike(self, position, direction) -> None:
        Spike(position, self.boss_boulder, (self.all_sprites, self.damage_sprites), direction, 64)
    
    def item_collision(self) -> None:
        if self.item_sprites:
            for sprite in self.item_sprites:
                if sprite.rect.colliderect(self.player.hitbox_rect):
                    sprite.activate()
                    VFX((sprite.rect.center), self.vfx_frames['sparkle'] if sprite.item_type == 'key' else self.vfx_frames['particle'], self.all_sprites)
    
    def pause_game(self) -> None:
        keys = pygame.key.get_just_pressed()
        '''Pause the game with ESC'''
        if keys[pygame.K_ESCAPE]:
            self.pause_menu.selected = 0
            self.data.paused = not self.data.paused
    
    def update_timers(self) -> None:
        for timer in self.timers.values():
            timer.update()
    
    def run(self, dt):
        '''Run the given level, update all sprites, center camera around player'''
        
        self.pause_game()
        if not self.data.paused:
            self.update_timers()
            self.all_sprites.update(dt)
            #self.data.ui.sprites.update(dt)
            
            self.melee_collision()
            self.ranged_collision()
            self.item_collision()
            
            self.check_exit()
            
            self.all_sprites.draw(self.player.hitbox_rect, dt)
        else:
            self.pause_menu.run(dt)