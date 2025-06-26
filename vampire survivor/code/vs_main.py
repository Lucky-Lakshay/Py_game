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

        self.setup()

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

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.running = False
            
            #update
            self.all_sprites.update(dt)

            #draw 
            self.display_surface.fill("black")
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()