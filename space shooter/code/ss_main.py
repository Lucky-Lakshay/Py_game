import pygame
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("space shooter", "images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center = (window_width/2, window_height-50))
        self.direction = pygame.math.Vector2()
        self.speed = 850

        #cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 500

    def update(self, dt):
        #player control
        key = pygame.key.get_pressed()       
        self.direction.x = int(key[pygame.K_RIGHT]) - int(key[pygame.K_LEFT])  
        self.direction.y = int(key[pygame.K_DOWN]) - int(key[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction  
        self.rect.center += self.direction * self.speed * dt
        
        #Screen Boundary Check
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > window_width:
            self.rect.right = window_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > window_height:
            self.rect.bottom = window_height

        #laser controls
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            laser_sound.play()
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        #laser timer
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True        

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0,window_width), randint(0,window_height)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
    def update(self, dt):
        self.rect.centery -= 500 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(100, 1100), 0))
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(500,800)
        self.rotation_speed = randint(-70,70)
        self.rotation = 0
    def update(self,dt):
        self.rect.center += self.speed * self.direction *  dt
        if self.rect.top > window_height:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class Animated_explosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)
    def update(self, dt):
        self.frame_index += 60 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index) % len(self.frames)]
        else:
            self.kill()

def collision():
    global running
    collision_sprite = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprite:
        damage_sound.play()
        running = False 
    for laser in laser_sprites:
        collision_sprite = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collision_sprite:
            laser.kill()
            Animated_explosion(explosion_frame, laser.rect.midtop, all_sprites)
            explosion_sound.play()

def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True, (240,240,240))
    text_rect = text_surf.get_frect(topleft = (25 , 20))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, "white", text_rect.inflate(30, 10).move(0, -5), 3, 10)


#general setup
pygame.init()
window_width, window_height = 1280, 720
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Shooter Space[::-1]")
running = True
clock = pygame.time.Clock()

#import
star_surf = pygame.image.load(join("space shooter", "images", "star.png")).convert_alpha()
laser_surf = pygame.image.load(join("space shooter", "images", "laser.png")).convert_alpha()
meteor_surf = pygame.image.load(join("space shooter", "images", "meteor.png")).convert_alpha()
font = pygame.font.Font(join("space shooter", "images", "font.ttf"), 30)
explosion_frame = [pygame.image.load(join("space shooter", "images", "explosion", f"{i}.png")).convert_alpha() for i in range(21)]
laser_sound = pygame.mixer.Sound(join("space shooter", "audio", "laser.wav"))
explosion_sound = pygame.mixer.Sound(join("space shooter", "audio", "explosion.wav"))
damage_sound = pygame.mixer.Sound(join("space shooter", "audio", "damage.ogg"))
game_music = pygame.mixer.Sound(join("space shooter", "audio", "game_music.wav"))
game_music.set_volume(0.5)
game_music.play(loops = -1)
#sprites 
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(35):
    star = Star(all_sprites, star_surf)    
player = Player(all_sprites)

#meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 300)

while running:
    # delta time, tick(max framerate)
    dt = clock.tick() / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surf, (all_sprites, meteor_sprites))
    #update
    all_sprites.update(dt)
    collision()
    #draw the game
    display_surface.fill((24, 25, 26))
    display_score()
    all_sprites.draw(display_surface) 

    pygame.display.update()

#quiting pygame to save resourses   
pygame.quit()