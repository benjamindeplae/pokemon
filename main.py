import pygame
from settings import *
from map import *
from player import *


class Game:
    def __init__(self):
        pg.init()
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.screen = pg.display.set_mode(RES)
        self.player = Player(self)
        self.map = Map(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in PLAYER_MOVEMENT_KEYS:
                    self.player.timer = self.player.timer
                    self.player.last_key.insert(0, event.key)
                elif event.key == PLAYER_TOGGLE_SPRINT:
                    self.player.sprint = not self.player.sprint
            elif event.type == pygame.KEYUP:
                if event.key in self.player.last_key:
                    self.player.last_key.remove(event.key)

    def update(self):
        self.player.update()
        self.delta_time = self.clock.tick()
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')
        pg.display.flip()

    def draw(self):
        # Calculate the offset to scroll the map with the players
        map_offset_x = WIDTH // 2 - self.player.x * self.player.player_width - self.player.player_width // 2
        map_offset_y = HEIGHT // 2 - self.player.y * self.player.player_height - self.player.player_height // 2 + TILE_HEIGHT // 1.2
        # Clear the screen
        self.screen.fill('black')
        # Draw the map with the calculated offset
        self.map.draw_map(map_offset_x, map_offset_y)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
