import pygame
import sys
import random

pygame.init()

width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Aim Trainer")

target_radius = 20
target_color = (255, 0, 0)  # Red
background_color = (255, 255, 255)  # White

clock = pygame.time.Clock()

def spawn_target():
    while True:
        x = random.randint(target_radius, width - target_radius)
        y = random.randint(target_radius, height - target_radius)
        # Check if the target is too close to the score and timer text
        if (10 <= x <= 150 and 10 <= y <= 50) or (width - 150 <= x <= width - 10 and 10 <= y <= 50):
            continue
        return [x, y]

def draw_targets():
    for target in targets:
        pygame.draw.circle(screen, target_color, (target[0], target[1]), target_radius)

def show_game_over_screen():
    screen.fill(background_color)
    game_over_text = font.render(f"The number of targets hit: {score}", True, (0, 0, 0))
    retry_text = font.render("Right-Click to Retry", True, (0, 0, 0))

    screen.blit(game_over_text, (width // 2 - 150, height // 2 - 30))
    screen.blit(retry_text, (width // 2 - 120, height // 2 + 20))

    pygame.display.flip()

    waiting_for_retry = True
    while waiting_for_retry:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right-click
                waiting_for_retry = False

# Initialize targets
num_targets = 5
targets = [spawn_target() for _ in range(num_targets)]
score = 0
font = pygame.font.Font(None, 36)

# Timer setup
timer_duration = 30  # 30 seconds
timer_start = pygame.time.get_ticks()

while True:
    elapsed_time = (pygame.time.get_ticks() - timer_start) / 1000  # in seconds

    if elapsed_time >= timer_duration:
        show_game_over_screen()
        # Reset game state
        targets = [spawn_target() for _ in range(num_targets)]
        score = 0
        timer_start = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for target in targets:
                distance = ((mouse_x - target[0])**2 + (mouse_y - target[1])**2)**0.5
                if distance < target_radius:
                    targets.remove(target)
                    targets.append(spawn_target())
                    score += 1

    screen.fill(background_color)

    # Draw targets
    draw_targets()

    # Display the score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Display the timer
    timer_text = font.render(f"Time: {timer_duration - elapsed_time:.1f}s", True, (0, 0, 0))
    screen.blit(timer_text, (width - 150, 10))

    pygame.display.flip()
    clock.tick(60)
