from settings import *
from gtimer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, collision_sprites, semi_collision_sprites, snail_sprites, frames):
        # general setup
        super().__init__(groups)
        self.z = Z_LAYERS['main']
                
        # abilities
        self.abilities = {'double_jump': False, 'walljump': False}
        
        # image
        self.frames, self.frame_index = frames, 0
        self.state, self.facing_right = 'idle', True
        self.image = self.frames[self.state][self.frame_index]
        
        # minimap
        self.map_image = pygame.Surface((1, 1))
        self.map_image.fill('gray')
        self.map_rect = self.map_image.get_frect(topleft = (position[0] / TILE_SIZE, position[1] / TILE_SIZE))
        
        # rects
        self.rect = self.image.get_frect(topleft = position)
        self.hitbox_rect = self.rect.inflate(-8, 0)
        self.old_rect = self.hitbox_rect.copy()
        
        self.floor_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2))  # rect UNDER player
        self.right_rect = pygame.Rect((self.hitbox_rect.topright + vector(0, self.hitbox_rect.height / 4)), (2, self.rect.height / 2))    # rect on RIGHT side of player
        self.left_rect = pygame.Rect((self.hitbox_rect.topleft + vector(-2, self.hitbox_rect.height / 4)), (2, self.rect.height / 2))    # rect on LEFT side of player
        
        # movement
        self.direction = vector()
        self.speed = 128
        self.fallspeed_max = 256
        self.gravity = 1024
        self.crouch = False
        self.jump = False
        self.jump_height = 256
        self.dash = False
              
        # collision
        self.collision_sprites = collision_sprites
        self.semi_collision_sprites = semi_collision_sprites
        self.snail_sprites = snail_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        self.platform = None
        
        # timers
        self.timers = {
            'platform_skip': Timer(200),
            'walljump': Timer(100),
            'wallslide_block': Timer(200),
            'dash': Timer(200)
        }
    
    def input(self) -> None:
        pressed = pygame.key.get_pressed()
        jpressed = pygame.key.get_just_pressed()
        released = pygame.key.get_just_released()
        input_vector = vector(0, 0)
        
        # we ignore input for a short time while on the wall
        if not self.timers['walljump'].active:
            # movement
            if pressed[pygame.K_RIGHT]:
                input_vector.x += 1
                self.facing_right = True
            
            if pressed[pygame.K_LEFT]:
                input_vector.x -= 1
                self.facing_right = False
            
            # platform skip / crouch
            if pressed[pygame.K_DOWN]:
                self.timers['platform_skip'].start()
                self.crouch = True if self.on_surface['floor'] else False
            
            if released[pygame.K_DOWN]:
                self.crouch = False
                self.frame_index = 0
            
            # interaction
            if pressed[pygame.K_UP]:
                self.does_interact = True
            if released[pygame.K_UP]:
                self.does_interact = False
            
            # dash
            if jpressed[pygame.K_x]:
                self.dash = True
                self.timers['dash'].start()
            
            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x
        # jumping
        if pressed[pygame.K_SPACE]:
            self.jump = True
        if released[pygame.K_SPACE] and self.direction.y <= 0:
            self.direction.y = 1
    
    def move(self, dt) -> None:
        if self.crouch:
            self.speed = 100
        elif not self.crouch:
            self.speed = 200
        
        # horizontal movement
        if self.timers['dash'].active:
            self.direction.y = 0
            self.direction.x = 1 if self.facing_right else -1
            self.hitbox_rect.x += self.direction.x * self.speed * dt
            self.dash = False
        else:
            self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        
        # vertical movement
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wallslide_block'].active:
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
        self.floor_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 1))  # rect UNDER player
        self.right_rect = pygame.Rect((self.hitbox_rect.topright + vector(0, self.hitbox_rect.height / 4)), (1, self.rect.height / 2))    # rect on RIGHT side of player
        self.left_rect = pygame.Rect((self.hitbox_rect.topleft + vector(-2, self.hitbox_rect.height / 4)), (1, self.rect.height / 2))    # rect on LEFT side of player
        
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        semi_collide_rects = [sprite.rect for sprite in self.semi_collision_sprites]
        snail_rects = [sprite.hitbox_rect for sprite in self.snail_sprites]
        
        # collisions
        self.on_surface['floor'] = True if (self.floor_rect.collidelist(collide_rects) >= 0 or self.floor_rect.collidelist(semi_collide_rects) >= 0 or self.floor_rect.collidelist(snail_rects) >= 0) and self.direction.y >= 0 else False
        self.on_surface['right'] = True if self.right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left'] = True if self.left_rect.collidelist(collide_rects) >= 0 else False
        
        self.platform = None
        sprites = self.collision_sprites.sprites() + self.semi_collision_sprites.sprites() + self.snail_sprites.sprites()
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(self.floor_rect):
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
        self.frame_index += ANIMATION_SPEED * dt
                
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
    
    def get_state(self) -> None:
        if self.on_surface['floor']:
            self.state = 'idle' if self.direction.x == 0 else 'walk'
            self.state = 'crouch' if self.crouch else self.state
        else:
            if any((self.on_surface['left'], self.on_surface['right'])):
                    self.state = 'wallslide'
            else:
                self.state = 'jump' if self.direction.y < 0 else 'fall'
        if self.timers['dash'].active:
            self.state = 'dash'
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
        
        # hitbox and side rects
        #self.show_hitbox()
        #self.show_collision_detect()
        

