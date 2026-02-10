import pygame
import math
import random
from collections import deque
pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GRAY = (200, 200, 200)
font = pygame.font.Font(None, 24)
def get_random_color():
    while True:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if color != WHITE:
            return color
def draw_grid(screen):
    for x in range(0, WIDTH, 50):
        color = GRAY if x != WIDTH // 2 else BLACK
        width = 1 if x != WIDTH // 2 else 2
        pygame.draw.line(screen, color, (x, 0), (x, HEIGHT), width)
    for y in range(0, HEIGHT, 50):
        color = GRAY if y != HEIGHT // 2 else BLACK
        width = 1 if y != HEIGHT // 2 else 2
        pygame.draw.line(screen, color, (0, y), (WIDTH, y), width)
def draw_info(screen, r_x, r_y, r_dir, trail, kills, font):
    info_txts = [
        f"Позиция: ({r_x:.1f}, {r_y:.1f})",
        f"Направление: {r_dir:.1f}°",
        f"Экранные: ({int(r_x + WIDTH / 2)}, {int(HEIGHT / 2 - r_y)})", 
        f"След: {len(trail)} точек",
        f"Убито: {kills}",
        "",
        "Управление:",
        "W A S D - движение",
        "Q E - поворот", 
        "Space - стрелять",
        "R - сброс в центр",
        "C - очистить след"]
    y_off = 10
    for text in info_txts:
        surface = font.render(text, True, BLACK)
        screen.blit(surface, (10, y_off))
        y_off += 25
def draw_robot(screen, r_x, r_y, r_dir, r_radius, r_color):
    s_x = int(r_x + WIDTH/2)
    s_y = int(HEIGHT/2 - r_y)
    pygame.draw.circle(screen, r_color, (s_x, s_y), r_radius)
    angle = math.radians(r_dir)
    tip_x = s_x + math.cos(angle) * r_radius * 1.5
    tip_y = s_y - math.sin(angle) * r_radius * 1.5
    lt_angle = angle + math.radians(140)
    lt_x = s_x + math.cos(lt_angle) * r_radius * 0.8
    lt_y = s_y - math.sin(lt_angle) * r_radius * 0.8
    rt_angle = angle - math.radians(140)
    rt_x = s_x + math.cos(rt_angle) * r_radius * 0.8
    rt_y = s_y - math.sin(rt_angle) * r_radius * 0.8
    pygame.draw.polygon(screen, WHITE, [
        (tip_x, tip_y),
        (lt_x, lt_y),
        (rt_x, rt_y)
    ])
    pygame.draw.circle(screen, BLACK, (s_x, s_y), r_radius, 2)

def draw_trail(screen, trail):
    if len(trail) < 2:
        return
    s_points = []
    for x, y in trail:
        s_x = int(x + WIDTH/2)
        s_y = int(HEIGHT/2 - y)
        s_points.append((s_x, s_y))
    if len(s_points) >= 2:
        pygame.draw.lines(screen, (100, 100, 255), False, s_points, 2)
r_x = 0
r_y = 0
r_dir = 0
r_color = BLACK
m_speed = 3 
r_radius = 15
t_speed = 3 
b_speed = 10
last_shot_t = 0
b_cooldown = 200
b_radius = 5
trail = deque(maxlen=150)
bullets = []
targets = []
kills = 0

def create_random_target():
    t_size = 20
    t_x = random.randint(-WIDTH // 2 + t_size, WIDTH // 2 - t_size)
    t_y = random.randint(-HEIGHT // 2 + t_size, HEIGHT // 2 - t_size)
    return {"x": t_x, "y": t_y, "size": t_size, "color": get_random_color()}
def draw_target(screen, target):
    s_x = int(target["x"] + WIDTH / 2)
    s_y = int(HEIGHT / 2 - target["y"])
    pygame.draw.rect(screen, target["color"], (s_x - target["size"] / 2, s_y - target["size"] / 2, target["size"], target["size"])) 
for _ in range(5):
    targets.append(create_random_target())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                r_x = 0
                r_y = 0
                r_dir = 0 
                r_color = BLACK
                trail.clear()
                targets.clear()
                for _ in range(5):
                    targets.append(create_random_target())
                kills = 0
            if event.key == pygame.K_c:
                trail.clear()
            if event.key == pygame.K_SPACE:
                c_time = pygame.time.get_ticks()
                if c_time - last_shot_t > b_cooldown:
                    b_x = r_x + math.cos(math.radians(r_dir)) * r_radius
                    b_y = r_y + math.sin(math.radians(r_dir)) * r_radius
                    bullets.append({"x": b_x, "y": b_y, "direction": r_dir, "color": get_random_color()})
                    last_shot_t = c_time
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        r_dir += t_speed
        r_dir %= 360
    if keys[pygame.K_e]:
        r_dir -= t_speed
        r_dir %= 360
    if keys[pygame.K_w]:
        angle = math.radians(r_dir)
        r_x += math.cos(angle) * m_speed
        r_y += math.sin(angle) * m_speed
    if keys[pygame.K_s]:
        angle = math.radians(r_dir + 180)
        r_x += math.cos(angle) * m_speed
        r_y += math.sin(angle) * m_speed
    if keys[pygame.K_a]:
        angle = math.radians(r_dir + 90)
        r_x += math.cos(angle) * m_speed
        r_y += math.sin(angle) * m_speed
    if keys[pygame.K_d]:
        angle = math.radians(r_dir - 90)
        r_x += math.cos(angle) * m_speed
        r_y += math.sin(angle) * m_speed
    trail.append((r_x, r_y))
    if r_x > WIDTH // 2 + r_radius:
        r_x = -(WIDTH // 2 + r_radius)
        r_color = get_random_color()
        trail.clear()
    elif r_x < -(WIDTH // 2 + r_radius):
        r_x = WIDTH // 2 + r_radius
        r_color = get_random_color()
        trail.clear()
    if r_y > HEIGHT // 2 + r_radius:
        r_y = -(HEIGHT // 2 + r_radius)
        r_color = get_random_color()
        trail.clear()
    elif r_y < -(HEIGHT // 2 + r_radius):
        r_y = HEIGHT // 2 + r_radius
        r_color = get_random_color()
        trail.clear()
    n_bullets = []
    for bullet in bullets:
        bullet["x"] += math.cos(math.radians(bullet["direction"])) * b_speed
        bullet["y"] += math.sin(math.radians(bullet["direction"])) * b_speed
        if -WIDTH // 2 - b_radius < bullet["x"] < WIDTH // 2 + b_radius and -HEIGHT // 2 - b_radius < bullet["y"] < HEIGHT // 2 + b_radius:
            n_bullets.append(bullet)
    bullets = n_bullets
    b_to_rem = []
    t_to_rem = []
    for bullet in bullets:
        for target in targets:
            d_x = bullet["x"] - target["x"]
            d_y = bullet["y"] - target["y"]
            distance = math.sqrt(d_x**2 + d_y**2)
            if distance < target["size"] / 2 + b_radius:
                b_to_rem.append(bullet)
                t_to_rem.append(target)
                kills += 1
                targets.append(create_random_target())
                break
    bullets = [b for b in bullets if b not in b_to_rem]
    targets = [t for t in targets if t not in t_to_rem]

    screen.fill(WHITE)
    draw_grid(screen)
    draw_trail(screen, trail)
    
    for bullet in bullets:
        sb_x = int(bullet["x"] + WIDTH / 2)
        sb_y = int(HEIGHT / 2 - bullet["y"])
        pygame.draw.circle(screen, bullet["color"], (sb_x, sb_y), b_radius)

    for target in targets:
        draw_target(screen, target)
    draw_robot(screen, r_x, r_y, r_dir, r_radius, r_color)
    draw_info(screen, r_x, r_y, r_dir, trail, kills, font)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()