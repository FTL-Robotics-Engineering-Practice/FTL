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
max_linear_speed = 150
max_angular_speed = 120 
linear_speed = 0
angular_speed = 0
target_x = 0 
target_y = 0
control_mode = "mouse" 

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

def draw_grid(screen):
    for x in range(0, WIDTH, 50):
        color = GRAY if x != WIDTH // 2 else BLACK
        width = 1 if x != WIDTH // 2 else 2
        pygame.draw.line(screen, color, (x, 0), (x, HEIGHT), width)
    for y in range(0, HEIGHT, 50):
        color = GRAY if y != HEIGHT // 2 else BLACK
        width = 1 if y != HEIGHT // 2 else 2
        pygame.draw.line(screen, color, (0, y), (WIDTH, y), width)

def draw_info(screen, r_x, r_y, r_dir, linear_speed, angular_speed, target_x, target_y, control_mode):
    info_txts = [
        f"Позиция: ({r_x:.1f}, {r_y:.1f})",
        f"Направление: {r_dir:.1f}°",
        f"Экранные: ({int(r_x + WIDTH / 2)}, {int(HEIGHT / 2 - r_y)})", 
        f"Скорость: {linear_speed:.1f} пикс/с",
        f"Угловая скорость: {angular_speed:.1f}°/с",
        f"Цель: ({target_x:.1f}, {target_y:.1f})",
        f"Режим: {control_mode}",
        "",
        "Управление:",
        "W S - линейная скорость",
        "A D - угловая скорость",
        "R - сброс в центр",
        "ЛКМ - телепорт",
        "СКМ - сброс",
        "TAB - переключение режимов"
        ]
    y_off = 10
    for text in info_txts:
        surface = font.render(text, True, BLACK)
        screen.blit(surface, (10, y_off))
        y_off += 25

last_time = pygame.time.get_ticks()
running = True
while running:
    dt = (pygame.time.get_ticks() - last_time) / 1000.0
    last_time = pygame.time.get_ticks()

    linear_speed = 0
    angular_speed = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                r_x = 0
                r_y = 0
                r_dir = 0
            elif event.key == pygame.K_TAB:
                control_mode = "keyboard" if control_mode == "mouse" else "mouse"
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_screen_x, mouse_screen_y = event.pos
                r_x = mouse_screen_x - WIDTH // 2
                r_y = HEIGHT // 2 - mouse_screen_y
                print(f"Телепорт ({int(r_x)}, {int(r_y)})")
            elif event.button == 2: 
                r_x = 0
                r_y = 0
                print("в центр")
    
    if control_mode == "mouse":
        mouse_screen_x, mouse_screen_y = pygame.mouse.get_pos()
        target_x = mouse_screen_x - WIDTH // 2
        target_y = HEIGHT // 2 - mouse_screen_y

        dx = target_x - r_x
        dy = target_y - r_y
        distance = math.hypot(dx, dy)

        angle_to_target_rad = math.atan2(dy, dx)
        angle_to_target_deg = math.degrees(angle_to_target_rad)

        angle_difference = angle_to_target_deg - r_dir
        if angle_difference > 180:
            angle_difference -= 360
        elif angle_difference < -180:
            angle_difference += 360

        if abs(angle_difference) > 5: 
            angular_speed = angle_difference * 3
            angular_speed = max(-max_angular_speed, min(max_angular_speed, angular_speed))
        else:
            angular_speed = 0

        if distance > 10 and abs(angle_difference) < 30:
            linear_speed = max_linear_speed
        else:
            linear_speed = 0
    elif control_mode == "keyboard":
        keys = pygame.key.get_pressed()
       
        if keys[pygame.K_w] and keys[pygame.K_s]:
            linear_speed = 0
        elif keys[pygame.K_w]:
            linear_speed = max_linear_speed
        elif keys[pygame.K_s]:
            linear_speed = -max_linear_speed
            
        if keys[pygame.K_a]:
            angular_speed = max_angular_speed
        if keys[pygame.K_d]:
            angular_speed = -max_angular_speed
    
    r_x += linear_speed * math.cos(math.radians(r_dir)) * dt
    r_y += linear_speed * math.sin(math.radians(r_dir)) * dt
    r_dir += angular_speed * dt
    r_dir %= 360 
    
    if r_x > WIDTH // 2 + r_radius:
        r_x = -(WIDTH // 2 + r_radius)
    if r_y > HEIGHT // 2 + r_radius:
        r_y = -(HEIGHT // 2 + r_radius)
    if r_y < -(HEIGHT // 2 + r_radius):
        r_y = ((HEIGHT // 2) + r_radius)
    if r_x < -(WIDTH // 2 + r_radius):
        r_x = ((WIDTH // 2) + r_radius)
        
    screen.fill(WHITE)
    draw_grid(screen)
    draw_robot(screen, r_x, r_y, r_dir, r_radius, BLACK)

    draw_info(screen, r_x, r_y, r_dir, linear_speed, angular_speed, target_x, target_y, control_mode)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

