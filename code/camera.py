from settings import *
from colours import ColourPalette, change_colours

class CameraGroup(pygame.sprite.Group):
    def __init__(self, width, height, data) -> None:
        '''The CameraGroup serves as a moving zoomed-in display surface that displays all sprites on level stages'''
        super().__init__()
        
        self.ui_sprites = [sprite for sprite in data.ui.sprites]
        
        self.display = pygame.display.get_surface()
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_frect()
        self.offset = vector()
        self.width, self.height = width * TILE_SIZE, height * TILE_SIZE
        
        # minimap
        self.minimap = MiniMap(width, height)
        
        # camera boundaries
        self.borders = {
            'left': 0,
            'right': -self.width + SCREEN_WIDTH,
            'bottom': -self.height + SCREEN_HEIGHT,
            'top': 0
        }
        
        # camera box
        self.camera_bounds = {'left': 64, 'right': 64, 'top': 36, 'bottom': 36}
        self.camera_box = pygame.FRect((self.screen_rect.left + self.camera_bounds['left'],
                                        self.screen_rect.top + self.camera_bounds['top']),
                                       (self.screen_rect.width - (self.camera_bounds['left'] + self.camera_bounds['right']),
                                        self.screen_rect.height - (self.camera_bounds['top'] + self.camera_bounds['bottom'])))
        
        # adjust filters
        self.filters = [
            None,
            ColourPalette.bubblegum,
            ColourPalette.dust,
            ColourPalette.evening,
            ColourPalette.gato,
            ColourPalette.green,
            ColourPalette.evening,
            ColourPalette.ibm51,
            ColourPalette.ibm8503,
            ColourPalette.noire,
            ColourPalette.nokia,
            ColourPalette.orange,
            ColourPalette.port,
            ColourPalette.popart,
            ColourPalette.purple,
            ColourPalette.sand,
            ColourPalette.sangre,
            ColourPalette.sepia,
            ColourPalette.yellow
        ]
        self.filter = 0
        self.invert = 0
    
    def cycle_filter(self) -> None:
        keys = pygame.key.get_just_pressed()
        
        if keys[pygame.K_BACKSPACE]:
            self.filter += 1
            self.filter = 0 if self.filter > 16 else self.filter
        
        if keys[pygame.K_RSHIFT]:
            self.invert += 1
            self.invert = 0 if self.invert > 1 else self.invert
    
    def camera_constraint(self) -> None:
        '''Don't allow camera movement when reaching level stage sides'''
        self.offset.x = self.offset.x if self.offset.x < self.borders['left'] else 0
        self.offset.x = self.offset.x if self.offset.x > self.borders['right'] else self.borders['right']
    
    def target_center_camera(self, target) -> None:
        self.offset.x = -(target.centerx - SCREEN_WIDTH / 2)
        self.offset.y = -(target.centery - SCREEN_HEIGHT / 2)
    
    def box_target_camera(self, target) -> None:
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
    
    def draw(self, target, dt):
        '''The custom draw method for the CameraGroup that draws in Z layer order'''
        self.cycle_filter()
        
        #self.box_target_camera(target)
        self.target_center_camera(target)
        self.camera_constraint()
        
        self.minimap.update(self.sprites())
        
        self.screen.fill('black')
        
        for sprite in sorted(self, key= lambda sprite: sprite.z):
            offset_pos = round(sprite.rect.left + self.offset.x), round(sprite.rect.top + self.offset.y)
            #offset_pos = sprite.rect.topleft + self.offset
            self.screen.blit(sprite.image, offset_pos)
        
        #for sprite in self.ui_sprites:
        #    self.screen.blit(sprite.image, sprite.rect)
        
        # change colours of every pixel on given surface(s)
        change_colours((self.screen, ), self.filters[self.filter], self.invert)
        
        pygame.transform.scale(self.screen, (WINDOW_WIDTH, WINDOW_HEIGHT), self.display)
        
        self.toggle_minimap()


class MiniMap:
    def __init__(self, width: int, height: int) -> None:
        '''A MiniMap surface that displays terrain and player position'''
        self.surface = pygame.Surface((width, height))
        self.scaled_surface = pygame.Surface((320, 240))
    
    def update(self, sprites) -> None:
        '''Update sprite positions'''
        self.scaled_surface.fill('black')
        self.surface.fill('black')
        
        for sprite in sprites:
            if hasattr(sprite, 'map_image'):
                self.surface.blit(sprite.map_image, (sprite.map_rect))
        
        scaled = pygame.transform.scale(self.surface, self.scaled_surface.size)
        self.scaled_surface.blit(scaled, (0, 0))

