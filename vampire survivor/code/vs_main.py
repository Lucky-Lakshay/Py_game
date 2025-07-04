from settings import *
from player import Player
from sprites import *
from groups import allsprites

class Game:
    def __init__(self):
        #setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survivor")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_active = True

        #groups
        self.all_sprites = allsprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # Gun Timer 
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 150

        # Enemy timer 
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_position = []

         # Melee attack system
        self.claw_sprites = pygame.sprite.Group()
        self.can_melee = True
        self.melee_time = 0
        self.melee_cooldown = 800

        # Player HP system
        self.max_hp = 10  # Maximum player health
        self.current_hp = self.max_hp

        # Damage cooldown system
        self.damage_cooldown = 1500  # 1 second in milliseconds
        self.last_damage_time = 0
        self.can_take_damage = True
        
        # Load heart image (you'll need to add this to your images folder)
        self.heart_surf = self.create_heart_surface(30)

        # audio and font
        self.font = pygame.font.Font(join("space shooter", "images", "font.ttf"), 30)
        self.shoot_sound = pygame.mixer.Sound(join("vampire survivor", "audio", "shoot.wav"))
        self.shoot_sound.set_volume(0.4)
        self.impact_sound = pygame.mixer.Sound(join("vampire survivor", "audio", "impact.ogg"))
        self.music = pygame.mixer.Sound(join("vampire survivor", "audio", "music.wav"))
        self.music.set_volume(0.5)
        self.music.play(loops = -1)

        #setup
        self.setup()
        self.load_images()
        
    def load_images(self):
        # bullet
        self.bullet_surf = pygame.image.load(join("vampire survivor", "images", "gun", "bullet.png")).convert_alpha()

        # Load claw attack image
        self.claw_surf = pygame.image.load(join("vampire survivor", "images", "claw.png")).convert_alpha()
        # Scale claw if needed
        self.claw_surf = pygame.transform.scale(self.claw_surf, (70, 70))

        # enemies
        # Get all enemy type folders
        folders = list(walk(join("vampire survivor", "images", "enemies")))[0][1]
        self.enemy_frames = {}

        for folder in folders:
            enemy_path = join("vampire survivor", "images", "enemies", folder)
            
            # Get all files in this enemy folder
            try:
                file_names = list(walk(enemy_path))[0][2]  # [2] gets files, not directories
                self.enemy_frames[folder] = []
                
                # Sort files numerically (assuming they're named like 1.png, 2.png, etc.)
                sorted_files = sorted(file_names, key=lambda name: int(name.split(".")[0]))
                
                for file_name in sorted_files:
                    full_path = join(enemy_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)
                    
            except (IndexError, ValueError) as e:
                print(f"Error loading frames for {folder}: {e}")

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.shoot_sound.play()
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

        # 360-degree melee attack (right click)
        if pygame.mouse.get_pressed()[2] and self.can_melee:  # Right mouse button
            # Create 8 claw attacks in all directions (360 degrees)
            num_claws = 8
            angle_step = 360 / num_claws
            
            for i in range(num_claws):
                # Calculate direction for each claw
                angle = math.radians(i * angle_step)
                direction = pygame.Vector2(math.cos(angle), math.sin(angle))
                
                # Create claw attack in this direction
                attack_pos = self.player.rect.center + direction * 25  # Start close to player
                ClawAttack(attack_pos, direction, self.claw_surf, (self.all_sprites, self.claw_sprites))
            
            self.can_melee = False
            self.melee_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    def melee_timer(self):
        if not self.can_melee:
            current_time = pygame.time.get_ticks()
            if current_time - self.melee_time >= self.melee_cooldown:
                self.can_melee = True

    def melee_collision(self):
        if self.claw_sprites:
            for claw in self.claw_sprites:
                hit_enemies = pygame.sprite.spritecollide(claw, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if hit_enemies:
                    for enemy in hit_enemies:
                        enemy.destroy()
                    claw.kill()

    def setup(self):
        map = load_pygame(join("vampire survivor", "data", "maps", "world.tmx"))
        for x, y, image in map.get_layer_by_name("Ground").tiles():
            Sprite((x* TILE_SIZE, y* TILE_SIZE), image, self.all_sprites)
        for obj in map.get_layer_by_name("Objects"):
            Collisionsprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        for obj in map.get_layer_by_name("Collisions"):
            Collisionsprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_position.append((obj.x, obj.y))    

    def bullet_collision(self):
        if self.bullet_sprites:
            for Bullet in self.bullet_sprites:
                Collisionsprite = pygame.sprite.spritecollide(Bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if Collisionsprite:
                    for sprite in Collisionsprite:
                        sprite.destroy()    
                    Bullet.kill()

    def create_heart_surface(self, size=30):
        #Create a heart shape surface programmatically
        heart_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Simple heart shape using circles and a triangle
        red = (255, 0, 0)
        
        # Two circles for the top of the heart
        circle_radius = size // 4
        pygame.draw.circle(heart_surf, red, (size//3, size//3), circle_radius)
        pygame.draw.circle(heart_surf, red, (2*size//3, size//3), circle_radius)
        
        # Triangle for the bottom of the heart
        points = [
            (size//6, size//2),
            (5*size//6, size//2),
            (size//2, 5*size//6)
        ]
        pygame.draw.polygon(heart_surf, red, points)
        
        return heart_surf

    def draw_hp(self):
        #Draw HP hearts in top-right corner
        heart_size = 30
        heart_spacing = 35
        start_x = WINDOW_WIDTH - (self.max_hp * heart_spacing) - 10
        start_y = 10
    
        for i in range(self.max_hp):
            x = start_x + (i * heart_spacing)
            y = start_y
            
            if i < self.current_hp:
                # Draw full heart for current HP
                self.display_surface.blit(self.heart_surf, (x, y))
            else:
                # Draw empty heart outline for lost HP
                empty_heart = self.heart_surf.copy()
                empty_heart.fill((100, 100, 100, 128), special_flags=pygame.BLEND_RGBA_MULT)
                self.display_surface.blit(empty_heart, (x, y))

    def damage_timer(self):
        # """Handle damage cooldown timer"""
        if not self.can_take_damage:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_damage_time >= self.damage_cooldown:
                self.can_take_damage = True

    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            
            if self.can_take_damage:
                self.impact_sound.play()
                self.current_hp -= 1
                self.can_take_damage = False
                self.last_damage_time = pygame.time.get_ticks()
                
                # Check if player is dead
                if self.current_hp <= 0:
                    self.current_hp = 0
                    self.game_active = False

    def restart_game(self):
        # """Reset all game state to start fresh"""
        # Clear all sprite groups
        self.all_sprites.empty()
        self.bullet_sprites.empty()
        self.enemy_sprites.empty()
        self.collision_sprites.empty()
        self.claw_sprites.empty()
        
        # Reset shooting timer
        self.can_shoot = True
        self.shoot_time = 0

        # Reset melee timer
        self.can_melee = True
        self.melee_time = 0
        
         # Reset HP
        self.current_hp = self.max_hp
        self.can_take_damage = True
        self.last_damage_time = 0

        # Reset game state
        self.game_active = True
        
        # Reload the map and recreate all sprites
        self.setup()

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.running = False

                if not self.game_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:  # Restart
                            self.restart_game()
                            
                        elif event.key == pygame.K_q:  # Quit
                            self.running = False

                if event.type == self.enemy_event:
                    Enemy(choice(self.spawn_position), choice(list(self.enemy_frames.values())), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)

            if self.game_active:
                #update
                self.gun_timer()
                self.melee_timer()
                self.damage_timer()
                self.input()
                self.all_sprites.update(dt)
                self.bullet_collision()
                self.melee_collision()
                self.player_collision()

                #draw 
                self.display_surface.fill("black")
                self.all_sprites.draw(self.player.rect.center)
                self.draw_hp()
            else:
                # Game Over Screen
                self.display_surface.fill((0, 0, 0))
                game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
                restart_text = self.font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
                self.display_surface.blit(game_over_text, game_over_text.get_frect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50)))
                self.display_surface.blit(restart_text, restart_text.get_frect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 60)))


            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()