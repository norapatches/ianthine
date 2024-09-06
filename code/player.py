from settings import *
from controls import LevelControls
from gtimer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, collision_sprites, semi_collision_sprites, snail_sprites, frames, data, projectile):
        # general setup
        super().__init__(groups)
        self.data = data
        self.z = Z_LAYERS['main']
                
        # abilities
        self.abilities = {'double_jump': False, 'walljump': False}
        
        # controls
        self.controls = LevelControls()
        
        # image
        self.frames, self.frame_index = frames, 0
        self.state, self.facing_right = 'idle', True
        self.image = self.frames[self.state][self.frame_index]
                
        # minimap
        self.map_image = pygame.Surface((1, 1))
        self.map_image.fill('red')
        self.map_rect = self.map_image.get_frect(topleft = (position[0] / TILE_SIZE, position[1] / TILE_SIZE))
        
        # rects
        self.rect = self.image.get_frect(topleft = position)
        self.hitbox_rect = self.rect.inflate(-8, 0)
        self.old_rect = self.hitbox_rect.copy()
               
        # movement
        self.direction = vector()
        
        self.fallspeed_max = 256
        self.gravity = 960
        self.crouch = False
        self.jump = False
        self.jump_height = 320 
        self.melee_atk = False
        self.ranged_atk = False
        self.has_fired = False
        self.create_projectile = projectile
              
        # collision
        self.collision_sprites = collision_sprites
        self.semi_collision_sprites = semi_collision_sprites
        self.snail_sprites = snail_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        self.platform = None
        
        # timers
        self.timers = {
            'platform_skip': Timer(100),
            'walljump': Timer(150),
            'wallslide_block': Timer(400),
            'attack_lock': Timer(600)
        }
    
    def input(self) -> None:
        pressed = pygame.key.get_pressed()
        jpressed = pygame.key.get_just_pressed()
        released = pygame.key.get_just_released()
        input_vector = vector(0, 0)
        
        # we ignore input for a short time while jumping off the wall
        if not self.timers['walljump'].active:
            # movement
            if pressed[self.controls.right]:
                input_vector.x += 1
                self.facing_right = True
            
            if pressed[self.controls.left]:
                input_vector.x -= 1
                self.facing_right = False
            
            # platform skip / crouch
            if pressed[self.controls.down]:
                if self.on_surface['floor']:
                    self.timers['platform_skip'].start()
                self.crouch = True if self.on_surface['floor'] else False
            
            if released[self.controls.down]:
                self.crouch = False
                self.frame_index = 0
            
            # interaction
            if pressed[self.controls.up]:
                self.does_interact = True
            if released[self.controls.up]:
                self.does_interact = False
            
            # melee
            if jpressed[self.controls.melee]:
                self.attack('melee')
            # ranged
            if jpressed[self.controls.ranged]:
                self.attack('ranged')
            
            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x
        
        # jumping
        if not self.abilities['walljump']:
            if jpressed[self.controls.jump]:
                self.jump = True
        else:
            if not any((self.on_surface['left'], self.on_surface['right'])):
                if jpressed[self.controls.jump]:
                    self.jump = True
            else:
                if pressed[self.controls.jump]:
                    self.jump = True
        
        if released[self.controls.jump] and self.direction.y <= 0:
            self.direction.y = 1
    
    def attack(self, type) -> None:
        if type == 'melee':
            if not self.timers['attack_lock'].active:
                self.melee_atk = True
                self.frame_index = 0
                self.timers['attack_lock'].start()
        if type == 'ranged':
            if not self.timers['attack_lock'].active:
                self.ranged_atk = True
                self.frame_index = 0
                self.timers['attack_lock'].start()
    
    def move(self, dt) -> None:
        self.speed = 64
        self.speed = self.speed if not self.crouch else self.speed / 2
        
        # horizontal movement
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        
        self.collision('horizontal')
        
        # vertical movement
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wallslide_block'].active and self.abilities['walljump']:
            self.direction.y = 0
            self.hitbox_rect.y += self.gravity / 14 * dt
        else:
            self.direction.y += self.gravity / 2 * dt
            self.hitbox_rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt
        # cap max velocity
        self.direction.y = self.direction.y if self.direction.y < self.fallspeed_max else self.fallspeed_max
        
        if self.jump:
            # jump
            if not self.timers['platform_skip'].active:
                if self.on_surface['floor']:
                    self.direction.y = -self.jump_height
                    self.timers['wallslide_block'].start()
                    self.hitbox_rect.bottom -= 1
                # walljump
                elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wallslide_block'].active and self.abilities['walljump']:
                    self.timers['walljump'].start()
                    self.direction.y = -self.jump_height
                    self.direction.x = 1 if self.on_surface['left'] else -1
            self.jump = False
        
        self.collision('vertical')
        self.semi_collision()
        
        self.rect.center = self.hitbox_rect.center
        self.map_rect.x, self.map_rect.y = (self.hitbox_rect.x / TILE_SIZE), self.hitbox_rect.y / TILE_SIZE
    
    def platform_move(self, dt) -> None:
        if self.platform:
            self.hitbox_rect.topleft += self.platform.direction * self.platform.speed * dt
    
    def check_contact(self) -> None:
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2))  # rect UNDER player
        right_rect = pygame.Rect((self.hitbox_rect.topright + vector(0, self.hitbox_rect.height / 4)), (2, self.rect.height / 2))    # rect on RIGHT side of player
        left_rect = pygame.Rect((self.hitbox_rect.topleft + vector(-2, self.hitbox_rect.height / 4)), (2, self.rect.height / 2))    # rect on LEFT side of player
        
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        semi_collide_rects = [sprite.rect for sprite in self.semi_collision_sprites]
        snail_rects = [sprite.hitbox_rect for sprite in self.snail_sprites]
        
        # collisions
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 or\
                                        floor_rect.collidelist(semi_collide_rects) >= 0 or\
                                        floor_rect.collidelist(snail_rects) >= 0 and\
                                        self.direction.y >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left'] = True if left_rect.collidelist(collide_rects) >= 0 else False
        
        self.platform = None
        sprites = self.collision_sprites.sprites() + self.semi_collision_sprites.sprites() + self.snail_sprites.sprites()
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite
    
    def collision(self, axis) -> None:
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis == 'horizontal':
                    if self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right):
                        self.hitbox_rect.left = sprite.rect.right
                    if self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.old_rect.left):
                        self.hitbox_rect.right = sprite.rect.left
                if axis == 'vertical':
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom):
                        self.hitbox_rect.top = sprite.rect.bottom
                        if hasattr(sprite, 'moving'):
                            self.hitbox_rect.top += 1
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top
                    self.direction.y = 0
    
    def semi_collision(self) -> None:
        if not self.timers['platform_skip'].active:
            for sprite in self.semi_collision_sprites:
                if sprite.rect.colliderect(self.hitbox_rect):
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top
                        if self.direction.y > 0:
                            self.direction.y = 0
            for sprite in self.snail_sprites:
                if sprite.hitbox_rect.colliderect(self.hitbox_rect):
                    if self.hitbox_rect.bottom >= sprite.hitbox_rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
                        self.hitbox_rect.bottom = sprite.hitbox_rect.top
                        if self.direction.y > 0:
                            self.direction.y = 0
    
    def update_timers(self) -> None:
        for timer in self.timers.values():
            timer.update()
    
    def animate(self, dt) -> None:
        if self.state in ['melee', 'air_melee', 'ranged', 'air_ranged']:
            self.frame_index += ANIMATION_SPEED * 2.5 * dt
        else:
            self.frame_index += ANIMATION_SPEED * dt
        
        if self.state in ['ranged', 'air_ranged'] and int(self.frame_index) == 1 and not self.has_fired:
            self.create_projectile(self.hitbox_rect.center, 1 if self.facing_right else -1)
            self.has_fired = True
        
        if self.state in ['melee', 'air_melee', 'ranged', 'air_ranged'] and self.frame_index >= len(self.frames[self.state]):
            self.state = 'idle'
            self.has_fired = False
        
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
        
        if self.melee_atk and self.frame_index > len(self.frames[self.state]):
            self.melee_atk = False
        if self.ranged_atk and self.frame_index > len(self.frames[self.state]):
            self.ranged_atk = False
    
    def get_state(self) -> None:
        if self.on_surface['floor']:
            if self.melee_atk:
                self.state = 'melee'
            elif self.ranged_atk:
                self.state = 'ranged'
            else:
                self.state = 'idle' if self.direction.x == 0 else 'walk'
                self.state = 'crouch' if self.crouch else self.state
        else:
            if self.melee_atk:
                self.state = 'air_melee'
            elif self.ranged_atk:
                self.state = 'air_ranged'
            else:
                if any((self.on_surface['left'], self.on_surface['right'])):
                        self.state = 'wallslide'
                else:
                    self.state = 'jump' if self.direction.y < 0 else 'fall'
        if self.crouch and self.direction.x != 0 and self.direction.y == 0:
            self.state = 'crouch_walk'
    
    def show_hitbox(self) -> None:
        surf = pygame.Surface(self.hitbox_rect.size)
        surf.fill('yellow')
        self.image.blit(surf, (4, 0))
    
    def show_collision_detect(self) -> None:
        floor_surf = pygame.Surface((self.hitbox_rect.width, 1))
        left_surf = pygame.Surface((1, self.hitbox_rect.height / 2))
        right_surf = pygame.Surface((1, self.hitbox_rect.height / 2))
        
        floor_surf.fill('green')
        left_surf.fill('green')
        right_surf.fill('green')
        
        self.image.blit(left_surf, (3, 4))
        self.image.blit(right_surf, (12, 4))
    
    def update(self, dt) -> None:
        # update rect and timer
        self.old_rect = self.hitbox_rect.copy()
        self.update_timers()
        
        # input and movement
        self.input()
        self.move(dt)
        self.platform_move(dt)
        self.check_contact()
        
        
        # animation
        self.get_state()
        self.animate(dt)
        
        '''hitbox and side rects'''
        #self.show_hitbox()
        #self.show_collision_detect()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, position, groups, direction, speed) -> None:
        self.projectile = True
        super().__init__(groups)
        self.image = pygame.Surface((2, 2))
        self.image.fill('white')
        self.rect = self.image.get_frect(center= position + vector(4 * direction, -4))
        self.direction = direction
        self.speed = speed
        self.z = Z_LAYERS['main']
        
        self.timers = {
            'lifetime': Timer(3000)
        }
        self.timers['lifetime'].start()
    
    def update(self, dt) -> None:
        for timer in self.timers.values():
            timer.update()
        self.rect.x += self.direction * self.speed * dt
        
        if not self.timers['lifetime'].active:
            self.kill()