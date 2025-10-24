# task 3.3
import pygame
import math
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

font = pygame.font.Font(None, 24)

robot_x = 0
robot_y = 0
robot_direction = 0

linear_speed = 0
angular_speed = 0

control_mode = "keyboard"

speed_multiplier = 1.0

MAX_X = WIDTH // 2 - 20
MAX_Y = HEIGHT // 2 - 20

trail = []

MAX_TRAIL_LENGTH = 100

coins = []

score = 0
high_score = 0

COIN_COLORS = [
    (255, 200, 0),
    (0, 200, 255),
    (255, 100, 200),
    (150, 255, 100)
]

COIN_RADIUS = 8
ROBOT_RADIUS = 15

obstacles = [
    {'x': 100, 'y': 0, 'radius': 30},
    {'x': -100, 'y': 100, 'radius': 25},
    {'x': 50, 'y': -80, 'radius': 20},
]

game_start_time = pygame.time.get_ticks()
GAME_DURATION = 60

def spawn_coin():
    x = random.randint(-MAX_X, MAX_X)
    y = random.randint(-MAX_Y, MAX_Y)
    
    color = random.choice(COIN_COLORS)
    
    if color == (255, 200, 0):
        value = 3
    else:
        value = 1
    
    coin = {
        'x': x,
        'y': y,
        'color': color,
        'radius': COIN_RADIUS,
        'value': value,
        'pulse': random.random() * 3.14
    }
    
    return coin

def draw_coins(screen, coins):
    for coin in coins:
        screen_x = coin['x'] + WIDTH // 2
        screen_y = HEIGHT // 2 - coin['y']
        
        coin['pulse'] += 0.1
        pulse_radius = coin['radius'] + math.sin(coin['pulse']) * 2
        
        pygame.draw.circle(
            surface=screen,
            color=coin['color'],
            center=(screen_x, screen_y),
            radius=int(pulse_radius)
        )

def draw_obstacles(screen, obstacles):
    for obs in obstacles:
        screen_x = obs['x'] + WIDTH // 2
        screen_y = HEIGHT // 2 - obs['y']
        pygame.draw.circle(
            surface=screen,
            color=(100, 100, 100),
            center=(screen_x, screen_y),
            radius=obs['radius']
        )

def restart_game():
    global score, coins, game_start_time, robot_x, robot_y, robot_direction, trail
    
    score = 0
    coins.clear()
    min_coins = 5
    for i in range(min_coins):
        coins.append(spawn_coin())
    robot_x = 0
    robot_y = 0
    robot_direction = 0
    trail.clear()
    game_start_time = pygame.time.get_ticks()
    print("Игра перезапущена!")

def draw_robot(screen, x, y, direction, radius):
    screen_x = x + WIDTH // 2
    screen_y = HEIGHT // 2 - y
    
    pygame.draw.circle(screen, BLUE, (screen_x, screen_y), radius)
    
    angle_rad = math.radians(direction)
    
    tip_x = screen_x + radius * math.cos(angle_rad)
    tip_y = screen_y - radius * math.sin(angle_rad)
    
    left_x = screen_x + (radius * 0.5) * math.cos(angle_rad + 2.5)
    left_y = screen_y - (radius * 0.5) * math.sin(angle_rad + 2.5)
    
    right_x = screen_x + (radius * 0.5) * math.cos(angle_rad - 2.5)
    right_y = screen_y - (radius * 0.5) * math.sin(angle_rad - 2.5)
    
    pygame.draw.polygon(screen, BLACK, [(tip_x, tip_y), (left_x, left_y), (right_x, right_y)])
    
    pygame.draw.circle(screen, BLACK, (screen_x, screen_y), radius, 2)

def draw_trail(screen, trail):
    if len(trail) < 2:
        return
    
    for i in range(len(trail) - 1):
        point1 = trail[i]
        point2 = trail[i + 1]
        
        screen_x1 = point1[0] + WIDTH // 2
        screen_y1 = HEIGHT // 2 - point1[1]
        screen_x2 = point2[0] + WIDTH // 2
        screen_y2 = HEIGHT // 2 - point2[1]
        
        pygame.draw.line(
            surface=screen,
            color=(150, 150, 255),
            start_pos=(screen_x1, screen_y1),
            end_pos=(screen_x2, screen_y2),
            width=2
        )

def draw_info(screen, x, y, direction, linear_speed, angular_speed, mode, multiplier, score, time_left, high_score):
    lines = [
        f"Счёт: {score}",
        f"Рекорд: {high_score}",
        f"Время: {int(time_left)}с",
        f"Позиция: ({int(x)}, {int(y)})",
        f"Направление: {int(direction % 360)}°",
        f"Линейная скорость: {int(linear_speed)} пикс/с",
        f"Угловая скорость: {int(angular_speed)} град/с",
        f"Режим: {mode}",
        f"Скорость: {int(multiplier * 100)}%",
        "Tab - режим, +/- скорость, R - перезапуск"
    ]
    
    y_offset = 10
    for line in lines:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (10, y_offset))
        y_offset += 25

for i in range(5):
    coins.append(spawn_coin())

running = True
while running:
    elapsed_time = (pygame.time.get_ticks() - game_start_time) / 1000
    remaining_time = GAME_DURATION - elapsed_time
    
    if remaining_time <= 0:
        if score > high_score:
            high_score = score
            print(f"Новый рекорд: {high_score}!")
        print(f"Игра окончена! Финальный счёт: {score}")
        remaining_time = 0
    
    min_coins = 5 + int(elapsed_time / 10)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_screen_x, mouse_screen_y = event.pos
                robot_x = mouse_screen_x - WIDTH // 2
                robot_y = HEIGHT // 2 - mouse_screen_y
                print(f"Телепортация в ({int(robot_x)}, {int(robot_y)})")
            if event.button == 2:
                robot_x = 0
                robot_y = 0
                print("Возврат в центр")
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if control_mode == "keyboard":
                    control_mode = "mouse"
                    print("Режим: следование за мышью")
                else:
                    control_mode = "keyboard"
                    print("Режим: управление клавиатурой")
            
            if event.key == pygame.K_r:
                restart_game()
            
            if event.key == pygame.K_EQUALS:
                speed_multiplier += 0.25
                speed_multiplier = min(3.0, speed_multiplier)
                print(f"Скорость: {speed_multiplier * 100:.0f}%")
            
            elif event.key == pygame.K_MINUS:
                speed_multiplier -= 0.25
                speed_multiplier = max(0.25, speed_multiplier)
                print(f"Скорость: {speed_multiplier * 100:.0f}%")
    
    dt = clock.tick(60) / 1000.0
    
    linear_speed = 0
    angular_speed = 0
    
    if control_mode == "keyboard":
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w] and keys[pygame.K_s]:
            linear_speed = 0
        elif keys[pygame.K_w]:
            linear_speed = 150 * speed_multiplier
        elif keys[pygame.K_s]:
            linear_speed = -100 * speed_multiplier
        
        if keys[pygame.K_a] and keys[pygame.K_d]:
            angular_speed = 0
        elif keys[pygame.K_a]:
            angular_speed = 120 * speed_multiplier
        elif keys[pygame.K_d]:
            angular_speed = -120 * speed_multiplier

    elif control_mode == "mouse":
        mouse_screen_x, mouse_screen_y = pygame.mouse.get_pos()
        target_x = mouse_screen_x - WIDTH // 2
        target_y = HEIGHT // 2 - mouse_screen_y
        
        dx = target_x - robot_x
        dy = target_y - robot_y
        distance = math.hypot(dx, dy)
        
        angle_to_target_rad = math.atan2(dy, dx)
        angle_to_target_deg = math.degrees(angle_to_target_rad)
        
        angle_difference = angle_to_target_deg - robot_direction
        
        if angle_difference > 180:
            angle_difference -= 360
        elif angle_difference < -180:
            angle_difference += 360
        
        if abs(angle_difference) > 5:
            angular_speed = (angle_difference * 3) * speed_multiplier
        else:
            angular_speed = 0
        
        if distance > 5 and abs(angle_difference) < 30:
            linear_speed = 150 * speed_multiplier
        else:
            linear_speed = 0
    
    robot_direction += angular_speed * dt
    
    angle_rad = math.radians(robot_direction)
    robot_x += linear_speed * math.cos(angle_rad) * dt
    robot_y += linear_speed * math.sin(angle_rad) * dt
    
    for obs in obstacles:
        dx = obs['x'] - robot_x
        dy = obs['y'] - robot_y
        distance = math.hypot(dx, dy)
        if distance < ROBOT_RADIUS + obs['radius']:
            push_angle = math.atan2(dy, dx)
            push_distance = (ROBOT_RADIUS + obs['radius']) - distance + 5
            robot_x -= math.cos(push_angle) * push_distance
            robot_y -= math.sin(push_angle) * push_distance
    
    coins_to_remove = []
    for coin in coins:
        dx = coin['x'] - robot_x
        dy = coin['y'] - robot_y
        distance = math.hypot(dx, dy)
        
        if distance < ROBOT_RADIUS + coin['radius']:
            coins_to_remove.append(coin)
            score += coin['value']
    
    for coin in coins_to_remove:
        coins.remove(coin)
    
    if len(coins) < min_coins:
        coins.append(spawn_coin())
    
    trail.append((robot_x, robot_y))
    
    if len(trail) > MAX_TRAIL_LENGTH:
        trail.pop(0)
    
    if robot_x > MAX_X:
        robot_x = MAX_X
    elif robot_x < -MAX_X:
        robot_x = -MAX_X
    
    if robot_y > MAX_Y:
        robot_y = MAX_Y
    elif robot_y < -MAX_Y:
        robot_y = -MAX_Y
    
    screen.fill(WHITE)
    
    draw_trail(screen, trail)
    
    draw_obstacles(screen, obstacles)
    
    draw_robot(screen, robot_x, robot_y, robot_direction, 30)
    
    draw_coins(screen, coins)
    
    draw_info(screen, robot_x, robot_y, robot_direction, linear_speed, angular_speed, control_mode, speed_multiplier, score, remaining_time, high_score)
    
    pygame.display.flip()

pygame.quit()
