import pygame
from settings import *
from collections import deque


class Player:
    def __init__(self, game, pos=(30, 10)):
        self.game = game
        self.tile_x, self.tile_y = pos
        self.x, self.y = pos
        self.player_width, self.player_height = TILE_WIDTH * FACTOR, TILE_HEIGHT * FACTOR
        self.last_key = []

        self.img = pygame.image.load('graphics/player.png')
        self.images_down = deque()
        for i in range(0, 2):
            img = self.img.subsurface(pygame.Rect(0, i * 32, 23, 25))
            self.images_down.append(pygame.transform.scale(img, (TILE_WIDTH * FACTOR, TILE_HEIGHT * FACTOR)))

        self.images_right = deque()
        for i in range(0, 3):
            img = self.img.subsurface(pygame.Rect(35, 32 + i * 32, 23, 25))
            self.images_right.append(pygame.transform.scale(img, (TILE_WIDTH * FACTOR, TILE_HEIGHT * FACTOR)))
        first_element = self.images_right.popleft()
        self.images_right.insert(1, first_element)

        self.images_left = deque()
        for i in range(0, 2):
            img = self.img.subsurface(pygame.Rect(0, 32 * 2 + i * 32, 23, 25))
            self.images_left.append(pygame.transform.scale(img, (TILE_WIDTH * FACTOR, TILE_HEIGHT * FACTOR)))
        img = self.img.subsurface(pygame.Rect(32, 0, 23, 25))
        self.images_left.append(pygame.transform.scale(img, (TILE_WIDTH * FACTOR, TILE_HEIGHT * FACTOR)))
        first_element = self.images_left.popleft()
        self.images_left.insert(1, first_element)

        self.images_up = deque()
        for i in range(0, 2):
            img = self.img.subsurface(pygame.Rect(354, 125 + i * 64, 23, 25))
            self.images_up.append(pygame.transform.scale(img, (TILE_WIDTH * FACTOR, TILE_HEIGHT * FACTOR)))
        first_element = self.images_up.popleft()
        self.images_up.insert(1, first_element)

        self.timer = 0
        self.drempel = 200
        self.current_img = self.images_down[0]
        self.speed = PLAYER_WALK_SPEED
        self.sprint = False
        self.current_direction = None

    def update(self):
        if self.x == self.tile_x and self.y == self.tile_y:
            if len(self.last_key):
                if self.last_key[0] == PLAYER_MOVEMENT_KEYS[0]:
                    self.current_direction = self.images_up
                    if self.game.map.hit_boxes[self.tile_y - 1][self.tile_x] == '_':
                        self.tile_y -= 1
                if self.last_key[0] == PLAYER_MOVEMENT_KEYS[1]:
                    self.current_direction = self.images_right
                    if self.game.map.hit_boxes[self.tile_y][self.tile_x + 1] == '_':
                        self.tile_x += 1
                if self.last_key[0] == PLAYER_MOVEMENT_KEYS[2]:
                    self.current_direction = self.images_down
                    if self.game.map.hit_boxes[self.tile_y + 1][self.tile_x] == '_':
                        self.tile_y += 1
                if self.last_key[0] == PLAYER_MOVEMENT_KEYS[3]:
                    self.current_direction = self.images_left
                    if self.game.map.hit_boxes[self.tile_y][self.tile_x - 1] == '_':
                        self.tile_x -= 1
            else:
                self.current_direction = None
        else:
            if self.x < self.tile_x:
                self.x += self.speed * self.game.delta_time
                if self.x > self.tile_x:
                    self.x = self.tile_x
            elif self.x > self.tile_x:
                self.x -= self.speed * self.game.delta_time
                if self.x < self.tile_x:
                    self.x = self.tile_x
            elif self.y < self.tile_y:
                self.y += self.speed * self.game.delta_time
                if self.y > self.tile_y:
                    self.y = self.tile_y
            elif self.y > self.tile_y:
                self.y -= self.speed * self.game.delta_time
                if self.y < self.tile_y:
                    self.y = self.tile_y

        self.timer += self.game.delta_time
        if self.timer >= self.drempel and self.current_direction:
            self.timer = 0
            self.current_img = self.current_direction[0]
            self.current_direction.rotate(-1)

        if self.sprint:
            self.speed = PLAYER_RUN_SPEED
        else:
            self.speed = PLAYER_WALK_SPEED

    def draw(self):
        # pygame.draw.rect(self.game.screen, (255, 255, 255), pygame.Rect(WIDTH // 2 - self.player_width // 2, HEIGHT // 2 - self.player_height // 2, self.player_width, self.player_height))
        self.game.screen.blit(self.current_img, (WIDTH // 2 - self.player_width // 2, HEIGHT // 2 - self.player_height // 2))
