import pygame
from os.path import join
from random import randint
#display
pygame.init()
window_width, window_height = 1280, 720
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Shooting space[::-1]")
running = True

#player
player_path = join("space shooter", "images", "player.png")
player_surf = pygame.image.load(player_path).convert_alpha()
player_rect = player_surf.get_frect(bottomleft = (100, window_height-50))
direction = 1
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
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #draw game
    display_surface.fill("darkgrey")

    for position in star_position:
        display_surface.blit(star_surf, position) 

    display_surface.blit(laser_surf, laser_rect)    

    display_surface.blit(meteor_surf, meteor_rect)

    #player movement
    player_rect.right += direction*0.3
    if player_rect.right > window_width or player_rect.left < 0:
        direction *= (-1)
    display_surface.blit(player_surf, player_rect) 

    pygame.display.update()

#quiting pygame to save resourses   
pygame.quit()