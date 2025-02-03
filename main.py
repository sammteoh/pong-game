import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, BACKGROUND_COLOR
from game_logic import GameLogic
from game_objects import Ball, Paddle

def main():
  pygame.init()

  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

  paddle = Paddle(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)
  ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

  game_logic = GameLogic(ball, paddle, screen)
  game_logic.display_game_start()

  clock = pygame.time.Clock()

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False
    
    game_logic.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
       paddle.move_left()
    if keys[pygame.K_RIGHT]:
       paddle.move_right()

    screen.fill(BACKGROUND_COLOR)
    paddle.draw(screen)
    ball.draw(screen)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {game_logic.score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    clock.tick(60)

  pygame.quit()

if __name__ == "__main__":
   main()