from settings import*

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = "down", 0
        self.image = pygame.image.load(join("vampire survivor", "images", "player", "down", "0.png")).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -60)

        #movement
        self.direction = pygame.math.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

    def load_images(self):
        self.frames = {"left":[],"right":[],"up":[],"down":[] }
        for state in self.frames.keys():
            for folderpath, subfolders, filenames in walk(join("vampire survivor","images", "player", state)):
                if filenames:
                    for filename in sorted(filenames, key= lambda name:int(name.split(".")[0])):
                        fullpath = join(folderpath, filename)
                        surf = pygame.image.load(fullpath).convert_alpha()
                        self.frames[state].append(surf)

    def input(self):
        key = pygame.key.get_pressed()       
        self.direction.x = int(key[pygame.K_RIGHT]) - int(key[pygame.K_LEFT])  
        self.direction.y = int(key[pygame.K_DOWN]) - int(key[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
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

    def animate(self, dt):
        if self.direction.x != 0:
            self.state = "right" if self.direction.x > 0 else "left"
        if self.direction.y != 0:
            self.state = "down" if self.direction.y > 0 else "up"

        self.frame_index = self.frame_index + 5 * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)