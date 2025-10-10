import pygame
import math

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))

clock = pygame.time.Clock()
clock.tick(60)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
font = pygame.font.Font(None, 24)
r_x = 0
r_y = 0
r_dir = 0
r_radius=20

def draw_robot(screen, x, y, direction, radius, color):
    s_x = int(x + WIDTH/2)
    s_y = int(HEIGHT/2 - y)
    
    pygame.draw.circle(screen, color, (s_x,s_y), radius)
    
    angle_rad = math.radians(direction)
    
    tip_x = s_x + math.cos(angle_rad) * radius * 1.5
    tip_y = s_y - math.sin(angle_rad) * radius * 1.5
    
    left_angle = angle_rad + math.radians(140)
    left_x = s_x + math.cos(left_angle) * radius * 0.8
    left_y = s_y - math.sin(left_angle) * radius * 0.8
    
    right_angle = angle_rad - math.radians(140)
    right_x = s_x + math.cos(right_angle) * radius * 0.8
    right_y = s_y - math.sin(right_angle) * radius * 0.8
    
    pygame.draw.polygon(screen, WHITE, [
        (tip_x, tip_y),
        (left_x, left_y),
        (right_x, right_y)
    ])
    
    pygame.draw.circle(screen, BLACK, (s_x, s_y), radius, 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)
    
    draw_robot(screen, r_x, r_y, r_dir, r_radius, BLACK)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

