import os 
import sys
import time
import random
from enum import Enum
from queue import Queue
import pygame 
from consts import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PADDLE_HEIGHT, PADDLE_WIDTH, BALL_WIDTH, BALL_HEIGHT 

pygame.init()

class Controller(Enum):
    UP = 0
    DOWN = 1

class Paddle:
    VELOCITY_Y = 20
    def __init__(self,x, y, width, height, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.screen = screen
        self.q = Queue()

        self.controller = {
            Controller.UP: self.up,
            Controller.DOWN: self.down
        }

    def draw(self):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, pygame.Color("White"), rect)

    def move(self):
        if not self.q.empty():
            move = self.q.get()
            self.controller[move]()

    def up(self):
        self.y -= Paddle.VELOCITY_Y

    def down(self):
        self.y += Paddle.VELOCITY_Y

    def clear(self, x, y):
        self.x = x
        self.y = y


class Ball:
    VELOCITY_X, VELOCITY_Y = 5, 5
    def __init__(self, x, y, width, height, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.screen = screen 

    def draw(self):
        ball = pygame.Rect(self.x, self.y, self.width, self.height)
        ball.collidedict
        pygame.draw.ellipse(self.screen, pygame.Color("White"), ball)

    def move(self, x, y):
        self.x += x
        self.y += y

    def clear(self):
        self.x = SCREEN_WIDTH//2 - BALL_WIDTH//2
        self.y = SCREEN_HEIGHT//2 - BALL_HEIGHT//2
        self.VELOCITY_X = [i * 0.1 for i in range(-10, 10) if i != 0][random.randint(0, 18)] * Ball.VELOCITY_X
        self.VELOCITY_Y = [i * 0.1 for i in range(-10, 10) if i != 0][random.randint(0, 18)] * Ball.VELOCITY_Y

class Pong:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.left_paddle = Paddle(15, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, self.screen)
        self.right_paddle = Paddle(SCREEN_WIDTH - 15 - PADDLE_WIDTH, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, self.screen)
        self.ball = Ball(SCREEN_WIDTH//2 - BALL_WIDTH//2, SCREEN_HEIGHT//2 - BALL_HEIGHT//2, BALL_WIDTH, BALL_HEIGHT, self.screen)
        
    def run(self):
        done = False 
        self.update()

        while not done:
            self.update()
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True 
                    break

                keys = pygame.key.get_pressed()
                if keys[pygame.K_q] and self.left_paddle.y >= 0:
                    self.left_paddle.q.put(Controller.UP)

                if keys[pygame.K_a] and self.left_paddle. y + PADDLE_HEIGHT <= SCREEN_HEIGHT:
                    self.left_paddle.q.put(Controller.DOWN)

                if keys[pygame.K_p] and self.right_paddle.y >= 0:
                    self.right_paddle.q.put(Controller.UP)

                if keys[pygame.K_l] and self.right_paddle. y + PADDLE_HEIGHT <= SCREEN_HEIGHT:
                    self.right_paddle.q.put(Controller.DOWN)

                self.left_paddle.move()
                self.right_paddle.move()

            self.draw()
            pygame.draw.aaline(self.screen, pygame.Color("White"), (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT))
            self.ball.draw()
            self.left_paddle.draw()
            self.right_paddle.draw()
            self.update()
            

            if self.ball.x <= self.left_paddle.x + PADDLE_WIDTH and (self.ball.y <= self.left_paddle.y + PADDLE_HEIGHT and self.ball.y >= self.left_paddle.y):
                self.ball.VELOCITY_X = -1 * self.ball.VELOCITY_X

            elif self.ball.x + BALL_WIDTH >= self.right_paddle.x and (self.ball.y <= self.right_paddle.y + PADDLE_HEIGHT and self.ball.y >= self.right_paddle.y):
                self.ball.VELOCITY_X = -1 * self.ball.VELOCITY_X

            if self.ball.y <= 0 or self.ball.y + BALL_HEIGHT >= SCREEN_HEIGHT:
                self.ball.VELOCITY_Y = -1 * self.ball.VELOCITY_Y

            elif self.ball.x <= 0 or self.ball.x + BALL_WIDTH >= SCREEN_WIDTH:
                self.ball.VELOCITY_X = -1 * self.ball.VELOCITY_X
                self.ball.clear()

            

            self.ball.move(self.ball.VELOCITY_X, self.ball.VELOCITY_Y)

        pygame.quit()
        sys.exit(0)

    def draw(self):
        self.screen.fill(pygame.Color("Black"))

    def update(self):
        pygame.display.flip()


