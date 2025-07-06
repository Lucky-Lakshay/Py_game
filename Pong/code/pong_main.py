from settings import * 
from sprites import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.running = True

        #sprites
        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()
        self.player = Player((self.all_sprites, self.paddle_sprites))
        self.ball = Ball(self.all_sprites, self.paddle_sprites)

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
            self.display_surface.fill(COLORS["bg"])
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()

        pygame.quit()
        
if __name__ == "__main__":
    game = Game()
    game.run()        