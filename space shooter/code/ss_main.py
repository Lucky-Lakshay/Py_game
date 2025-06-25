import pygame
from os.path import join
from random import randint
#display
pygame.init()
window_width, window_height = 1280, 720
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Shooting space[::-1]")
running = True
clock = pygame.time.Clock()

#player
player_path = join("space shooter", "images", "player.png")
player_surf = pygame.image.load(player_path).convert_alpha()
player_rect = player_surf.get_frect(bottomleft = (100, window_height-50))
player_direction = pygame.math.Vector2()
player_speed = 550
#stars
star_path = join("space shooter", "images", "star.png")
star_surf = pygame.image.load(star_path).convert_alpha()
star_position = [(randint(0,window_width), randint(0,window_height)) for i in range(20)]
#meteor
meteor_path = join("space shooter", "images", "meteor.png")
meteor_surf = pygame.image.load(meteor_path).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (window_width/2, window_height/2))
#laser
laser_path = join("space shooter", "images", "laser.png")
laser_surf = pygame.image.load(laser_path).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, window_height-20))
while running:
    # delta time, tick(max framerate)
    dt = clock.tick() / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if event.type == pygame.MOUSEMOTION:
        #    player_rect.center = event.pos

    #input
    key = pygame.key.get_pressed()
    player_direction.x = int(key[pygame.K_RIGHT]) - int(key[pygame.K_LEFT])  
    player_direction.y = int(key[pygame.K_DOWN]) - int(key[pygame.K_UP])
    player_direction = player_direction.normalize() if player_direction else player_direction  
    player_rect.center += player_direction * player_speed * dt    
    #draw game
    display_surface.fill("darkgrey")
    for position in star_position:
        display_surface.blit(star_surf, position) 
    display_surface.blit(laser_surf, laser_rect)    
    display_surface.blit(meteor_surf, meteor_rect)  
    display_surface.blit(player_surf, player_rect) 
    pygame.display.update()

#quiting pygame to save resourses   
pygame.quit()