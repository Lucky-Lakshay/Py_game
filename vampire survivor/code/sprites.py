from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

class Collisionsprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        self.player = player
        self.distance = 100
        self.player_direction = pygame.Vector2(1,0)

        super().__init__(groups)
        self.gun_surf = pygame.image.load(join("vampire survivor", "images", "gun", "gun.png")).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction*self.distance)

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.player_direction = (mouse_pos - player_pos).normalize()

    def rotate_gun(self):
        angle = math.degrees(math.atan2(self.player_direction.x, self.player_direction.y)) - 90
        if self.player_direction.x > 0:    
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)

    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction*self.distance

class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.spawn_time = pygame. time.get_ticks()
        self.lifetime = 1000

        self.direction = direction
        self.speed = 1200

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt    

        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player

        #image
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.animation_speed = 6

        #rect
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-20,-40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 350

        #timer
        self.death_time = 0
        self.death_duration = 150


    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def move(self, dt):
        #get direction
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()

        #update rect position + collision
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision("vertical")
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == "horizontal":
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom       
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def destroy(self):
        #start timer
        self.death_time = pygame.time.get_ticks()

        # Create white silhouette from enemy mask
        mask = pygame.mask.from_surface(self.frames[0])
        # to_surface() with setcolor makes visible pixels white, invisible pixels transparent
        self.image = mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0))

    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()

    def update(self,dt):
        if self.death_time == 0:
            self.move(dt)    
            self.animate(dt)
        else:
            self.death_timer()

class ClawAttack(pygame.sprite.Sprite):
    def __init__(self, pos, direction, claw_image, groups):
        super().__init__(groups)
        
        # Load and setup claw image
        self.original_image = claw_image
        self.image = self.original_image.copy()

        # Rotate claw based on direction
        angle = math.degrees(math.atan2(-direction.y, direction.x))
        self.image = pygame.transform.rotate(self.original_image, angle)
        
        # Position
        self.rect = self.image.get_frect(center=pos)
        
        # Attack properties
        self.direction = direction
        self.speed = 150  # Slightly slower for 360 attack
        self.damage = 2   # Higher damage than bullet
        self.range = 60   # Shorter range for balance
        self.distance_traveled = 0
        
        # Animation
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 300  # Attack lasts 300ms
        
    def update(self, dt):
        # Move claw attack
        self.rect.center += self.direction * self.speed * dt
        self.distance_traveled += self.speed * dt
        
        # Remove if out of range or lifetime exceeded
        current_time = pygame.time.get_ticks()
        if (self.distance_traveled >= self.range or 
            current_time - self.creation_time >= self.lifetime):
            self.kill()
        
        # Scale effect - starts big, gets smaller
        time_ratio = (current_time - self.creation_time) / self.lifetime
        scale = 1.0 - (time_ratio * 0.3)  # Shrink by 30%
        if scale > 0:
            scaled_size = (int(self.original_image.get_width() * scale),
                          int(self.original_image.get_height() * scale))
            angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))
            self.image = pygame.transform.scale(self.original_image, scaled_size)
            self.image = pygame.transform.rotate(self.image, angle)
            self.rect = self.image.get_frect(center=self.rect.center)