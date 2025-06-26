import pygame
from os.path import join
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("space shooter", "images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(bottomleft = (100, window_height-50))
        self.direction = pygame.math.Vector2()
        self.speed = 850

        #cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 200

    def update(self, dt):
        #player control
        key = pygame.key.get_pressed()       
        self.direction.x = int(key[pygame.K_RIGHT]) - int(key[pygame.K_LEFT])  
        self.direction.y = int(key[pygame.K_DOWN]) - int(key[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction  
        self.rect.center += self.direction * self.speed * dt
        #laser controls
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, all_sprites)
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
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(100, 1100), 0))
    def update(self,dt):
        self.rect.centery += 400 * dt
        if self.rect.top > window_height:
            self.kill()

#general setup
pygame.init()
window_width, window_height = 1280, 720
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Shooting space[::-1]")
running = True
clock = pygame.time.Clock()

#import
star_surf = pygame.image.load(join("space shooter", "images", "star.png")).convert_alpha()
laser_surf = pygame.image.load(join("space shooter", "images", "laser.png")).convert_alpha()
meteor_surf = pygame.image.load(join("space shooter", "images", "meteor.png")).convert_alpha()

#sprites 
all_sprites = pygame.sprite.Group()
for i in range(20):
    star = Star(all_sprites, star_surf)
player = Player(all_sprites)

#meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 1000)

while running:
    # delta time, tick(max framerate)
    dt = clock.tick() / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surf, all_sprites)

    all_sprites.update(dt)
    display_surface.fill("darkgrey")
    all_sprites.draw(display_surface) 
    pygame.display.update()

#quiting pygame to save resourses   
pygame.quit()