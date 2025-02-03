import pygame
import os
import sys
from settings import *
from game_objects import Ball, Paddle

class GameLogic:
  def __init__(self, ball, paddle, screen):
    self.screen = screen
    self.ball = ball
    self.paddle = paddle
    self.screen_width = SCREEN_WIDTH
    self.screen_height = SCREEN_HEIGHT
    self.score = 0
    self.speed = INITIAL_BALL_SPEED
    self.game_over = False

    self.read_high_scores()
    self.high_scores = self.read_high_scores()
    self.high_score = self.high_scores[0]

    self.title_font = pygame.font.Font(None, 50)
    self.subtitle_font = pygame.font.Font(None, 30)
    self.score_font = pygame.font.Font(None, 20)

    self.game_start_text = self.title_font.render("SAM'S PONG GAME", True, (0, 0, 0))
    self.high_score_text = self.score_font.render(f"High Score: {self.high_score}", True, (0, 0, 0))
    self.game_over_text = self.title_font.render("Game Over", True, (0, 0, 0))
    self.score_text = self.score_font.render(f"Score: {self.score}", True, (0, 0, 0))

    # Buttons
    self.play_text = self.score_font.render("P to Play", True, (0, 0, 0))
    self.quit_text = self.score_font.render("Q to Quit", True, (0, 0, 0))
    self.view_text = self.score_font.render("V to View Scores", True, (0, 0, 0))
    self.return_text = self.score_font.render("R to Return Home", True, (0, 0, 0))
    self.delete_text = self.score_font.render("D to Delete Past Scores", True, (0, 0, 0))

    # View scores
    self.high_score_title_text = self.title_font.render("High Scores", True, (0, 0, 0))
    self.table_text = self.subtitle_font.render("Rank : Score", True, (0, 0, 0))
  
  def update(self):
    if self.game_over:
      self.display_game_over()
      return
    
    # Move the ball
    self.ball.move()

    # Check collisions with wall
    if self.ball.rect.left <= 0 or self.ball.rect.right >= SCREEN_WIDTH:
      self.ball.speed_x = -self.ball.speed_x
    if self.ball.rect.top <= 0:
      self.ball.speed_y = -self.ball.speed_y
    
    # Check collisions with paddle
    if self.ball.rect.colliderect(self.paddle.rect):
      if (
        self.ball.rect.bottom + self.ball.speed_y >= self.paddle.rect.top
        and self.ball.rect.top < self.paddle.rect.top
      ):
        self.ball.rect.bottom = self.paddle.rect.top
        self.ball.speed_y *= -1
        self.score += 1
        
        self.ball.speed_y *= 1.1
        self.ball.speed_x *= 1.1
      else:
        pass
    
    # Check collisions with bottom
    if self.ball.rect.bottom >= self.screen_height:
      self.game_over = True
  
  def read_high_scores(self, file_name="high_scores.txt"):
    try:
      with open(file_name, "r") as file:
        scores = file.readlines()
      return sorted([int(score.strip()) for score in scores], reverse=True)
    except FileNotFoundError:
      with open(file_name, "x") as file:
        for i in range(5):
          file.write("0 \n")
  
  def update_high_scores(self, score, file_name="high_scores.txt"):
    scores = self.read_high_scores(file_name)
    scores.append(score)
    scores = sorted(scores, reverse=True)[:5]

    with open(file_name, "w") as file:
      for score in scores:
        file.write(f"{score}\n")


  def display_game_start(self):
    self.screen.fill(BACKGROUND_COLOR)


    self.screen.blit(self.game_start_text, (SCREEN_WIDTH // 2 - self.game_start_text.get_width() // 2, SCREEN_HEIGHT // 3))
    self.screen.blit(self.high_score_text, (SCREEN_WIDTH // 2 - self.high_score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    self.screen.blit(self.play_text, (SCREEN_WIDTH // 2 - self.play_text.get_width() // 2, SCREEN_HEIGHT // 1.5))
    self.screen.blit(self.quit_text, (SCREEN_WIDTH // 2 - self.quit_text.get_width() // 2, SCREEN_HEIGHT // 1.43))
    self.screen.blit(self.view_text, (SCREEN_WIDTH // 2 - self.view_text.get_width() // 2, SCREEN_HEIGHT // 1.36))

    pygame.display.flip()

    self.wait_for_input()
  
  def is_high_score(self, score):
    if score > self.high_score:
      return True
  
  def is_file(self, file_name='high_scores.txt'):
    if os.path.exists(file_name):
      return True
  
  def display_top_scores(self):
    self.screen.fill(BACKGROUND_COLOR)
    
    high_scores_text = [
      self.score_font.render(f"{i+1} : {score} hits", True, (0, 0, 0)) for i, score in enumerate(self.high_scores)
    ]

    self.screen.blit(self.high_score_title_text, (SCREEN_WIDTH // 2 - self.high_score_title_text.get_width() // 2, SCREEN_HEIGHT // 20))

    self.screen.blit(self.table_text, (SCREEN_WIDTH // 2 - self.table_text.get_width() // 2, SCREEN_HEIGHT // 5))
    
    for i, text in enumerate(high_scores_text):
      self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_WIDTH // 2 + i * 50))
    
    self.screen.blit(self.play_text, (SCREEN_WIDTH // 2 - self.play_text.get_width() // 2, SCREEN_HEIGHT // 1.5))
    self.screen.blit(self.quit_text, (SCREEN_WIDTH // 2 - self.quit_text.get_width() // 2, SCREEN_HEIGHT // 1.43))
    self.screen.blit(self.return_text, (SCREEN_WIDTH // 2 - self.return_text.get_width() // 2, SCREEN_HEIGHT // 1.36))
    if self.is_file('high_scores.txt'):
      self.screen.blit(self.delete_text, (SCREEN_WIDTH // 2 - self.delete_text.get_width() // 2, SCREEN_HEIGHT // 1.29))

    pygame.display.flip()

    self.wait_for_input()
  
  def display_game_over(self):
    self.update_high_scores(self.score, "high_scores.txt")
    self.update_text()

    if self.is_high_score(self.score):
      self.high_score_text = self.score_font.render("New high score!", True, (0, 0, 0))
    else:
      self.high_score_text = self.score_font.render(f"High score: {self.high_score}", True, (0, 0, 0))

    self.screen.blit(self.game_over_text, (SCREEN_WIDTH // 2 - self.game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    self.screen.blit(self.high_score_text, (SCREEN_WIDTH // 2 - self.high_score_text.get_width() // 2, SCREEN_HEIGHT // 2.5))
    self.screen.blit(self.score_text, (SCREEN_WIDTH // 2 - self.score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    self.screen.blit(self.play_text, (SCREEN_WIDTH // 2 - self.play_text.get_width() // 2, SCREEN_HEIGHT // 1.5))
    self.screen.blit(self.quit_text, (SCREEN_WIDTH // 2 - self.quit_text.get_width() // 2, SCREEN_HEIGHT // 1.43))
    self.screen.blit(self.view_text, (SCREEN_WIDTH // 2 - self.view_text.get_width() // 2, SCREEN_HEIGHT // 1.36))
    self.screen.blit(self.return_text, (SCREEN_WIDTH // 2 - self.return_text.get_width() // 2, SCREEN_HEIGHT // 1.29))

    pygame.display.flip()

    self.wait_for_input()
  
  def wait_for_input(self):
    waiting_for_input = True
    while waiting_for_input:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_p:
            self.reset()
            waiting_for_input = False
          elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
          elif event.key == pygame.K_v:
            self.display_top_scores()
            waiting_for_input = False
          elif event.key == pygame.K_r:
            self.display_game_start()
            waiting_for_input = False
          elif event.key == pygame.K_d:
            self.confirm_deletion()
            waiting_for_input = False

  def update_text(self):
    self.read_high_scores()
    self.high_scores = self.read_high_scores()
    self.high_score = self.high_scores[0]
    self.high_score_text = self.score_font.render(f"High Score: {self.high_score}", True, (0, 0, 0))
    self.score_text = self.score_font.render(f"Score: {self.score}", True, (0, 0, 0))

  def reset(self):
    self.paddle.reset()
    self.ball.reset()
    self.score = 0
    self.game_over = False
    self.update()
  
  def confirm_deletion(self):
    self.screen.fill(BACKGROUND_COLOR)

    self.confirm_deletion_text = self.score_font.render("Are you sure you want to delete your score history?", True, (0, 0, 0))
    self.confirm_deletion_text_2 = self.score_font.render("This action cannot be undone", True, (0, 0, 0))
    self.confirm_deletion_text_3 = self.score_font.render("Press 'Y' to Confirm and 'X' to Cancel", True, (0, 0, 0))

    self.screen.blit(self.confirm_deletion_text, (SCREEN_WIDTH // 2 - self.confirm_deletion_text.get_width() // 2, SCREEN_HEIGHT // 2))
    self.screen.blit(self.confirm_deletion_text_2, (SCREEN_WIDTH // 2 - self.confirm_deletion_text_2.get_width() // 2, SCREEN_HEIGHT // 1.9))
    self.screen.blit(self.confirm_deletion_text_3, (SCREEN_WIDTH // 2 - self.confirm_deletion_text_3.get_width() // 2, SCREEN_HEIGHT // 1.8))

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_y:
            self.reset_scores()
            waiting_for_input = False
          if event.key == pygame.K_x:
            self.display_top_scores()
            waiting_for_input = False
  
  def reset_scores(self):
    if os.path.exists("high_scores.txt"):
      os.remove("high_scores.txt")
      self.update_text()
      self.display_game_start()
      return
    else:
      pass