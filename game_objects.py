import pygame
from settings import *

class Paddle:
  def __init__(self, x, y):
    self.rect = pygame.Rect(x - PADDLE_WIDTH // 2, y, PADDLE_WIDTH, PADDLE_HEIGHT)
    self.color = PADDLE_COLOR
    self.speed = PADDLE_SPEED

  def move_left(self):
    if self.rect.left > 0:
      self.rect.x -= self.speed
  
  def move_right(self):
    if self.rect.right < SCREEN_WIDTH:
      self.rect.x += self.speed

  def draw(self, screen):
    pygame.draw.rect(screen, self.color, self.rect)
  
  def reset(self):
    self.rect.centerx = SCREEN_WIDTH // 2


class Ball:
  def __init__(self, x, y):
    self.rect = pygame.Rect(x - BALL_RADIUS, y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
    self.color = BALL_COLOR
    self.speed_x = INITIAL_BALL_SPEED
    self.speed_y = INITIAL_BALL_SPEED
  
  def move(self):
    self.rect.x += self.speed_x
    self.rect.y += self.speed_y

  def draw(self, screen):
    pygame.draw.ellipse(screen, self.color, self.rect)
  
  def reset(self):
    self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    self.speed_x = INITIAL_BALL_SPEED
    self.speed_y = INITIAL_BALL_SPEED