import pygame
import math

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600

# Создаем окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Задание 4.2: Треугольник направления")
clock = pygame.time.Clock()

# Шрифт для текста
font = pygame.font.Font(None, 24)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 100, 255)

# Позиция робота (математические координаты)
robot_x = 0
robot_y = 0
robot_direction = 0  # градусы: 0 = вправо, 90 = вверх
robot_radius = 15

# Скорость перемещения
move_speed = 3


def draw_grid(screen):
    """Рисует сетку координат"""
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    
    for x in range(0, WIDTH, 50):
        color = GRAY if x != center_x else BLACK
        width = 1 if x != center_x else 2
        pygame.draw.line(screen, color, (x, 0), (x, HEIGHT), width)
    
    for y in range(0, HEIGHT, 50):
        color = GRAY if y != center_y else BLACK
        width = 1 if y != center_y else 2
        pygame.draw.line(screen, color, (0, y), (WIDTH, y), width)


def draw_robot(screen, x, y, direction, radius):
    """Рисует робота с направлением"""
    # Преобразование координат
    screen_x = int(x + WIDTH/2)
    screen_y = int(HEIGHT/2 - y)
    
    # Рисуем тело (круг)
    pygame.draw.circle(screen, BLUE, (screen_x, screen_y), radius)
    
    # Рисуем направление (треугольник)
    angle = math.radians(direction)
    
    # Вершина треугольника (направление)
    tip_x = screen_x + math.cos(angle) * radius * 0.9
    tip_y = screen_y - math.sin(angle) * radius * 0.9
    
    # Две задние точки
    left_angle = angle + math.radians(140)
    right_angle = angle - math.radians(140)
    
    left_x = screen_x + math.cos(left_angle) * radius * 0.8
    left_y = screen_y - math.sin(left_angle) * radius * 0.8
    
    right_x = screen_x + math.cos(right_angle) * radius * 0.8
    right_y = screen_y - math.sin(right_angle) * radius * 0.8
    
    # Рисуем треугольник
    pygame.draw.polygon(screen, WHITE, [
        (tip_x, tip_y),
        (left_x, left_y),
        (right_x, right_y)
    ])
    
    # Контур круга
    pygame.draw.circle(screen, BLACK, (screen_x, screen_y), radius, 2)


def draw_info(screen, x, y, direction, font):
    """Рисует информацию на экране"""
    info_texts = [
        f"Позиция: ({x:.1f}, {y:.1f})",
        f"Направление: {direction:.1f}°",
        "",
        "Управление:",
        "W A S D - движение",
        "R - сброс в центр"
    ]
    
    y_offset = 10
    for text in info_texts:
        surface = font.render(text, True, BLACK)
        screen.blit(surface, (10, y_offset))
        y_offset += 25


# Главный игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                robot_x = 0
                robot_y = 0
                robot_direction = 0
    
    # Управление
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w]:
        robot_y += move_speed
    if keys[pygame.K_s]:
        robot_y -= move_speed
    if keys[pygame.K_a]:
        robot_x -= move_speed
    if keys[pygame.K_d]:
        robot_x += move_speed
    
    # Заливаем экран белым цветом
    screen.fill(WHITE)
    
    # Рисуем сетку
    draw_grid(screen)
    
    # Рисуем робота с треугольником
    draw_robot(screen, robot_x, robot_y, robot_direction, robot_radius)
    
    # Выводим информацию
    draw_info(screen, robot_x, robot_y, robot_direction, font)
    
    # Обновляем экран
    pygame.display.flip()
    
    # Контроль FPS
    clock.tick(60)

# Завершение
pygame.quit()