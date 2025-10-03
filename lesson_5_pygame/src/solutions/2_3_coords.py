import pygame

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600

# Создаем окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Задание 2.3: Математические координаты")
clock = pygame.time.Clock()

# Шрифт для текста
font = pygame.font.Font(None, 24)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 100, 255)

# Позиция робота (МАТЕМАТИЧЕСКИЕ координаты, центр = 0,0)
robot_x = 0
robot_y = 0


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


# Главный игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # ДВИЖЕНИЕ: робот двигается вправо в математических координатах
    robot_x += 2
    
    # Если вышел за край, вернуть назад
    if robot_x > 450:
        robot_x = -450
    
    # ПРЕОБРАЗОВАНИЕ: математические → экранные координаты
    screen_x = int(robot_x + WIDTH/2)
    screen_y = int(HEIGHT/2 - robot_y)  # Y инвертируется!
    
    # Заливаем экран белым цветом
    screen.fill(WHITE)
    
    # Рисуем сетку
    draw_grid(screen)
    
    # Рисуем синий круг
    pygame.draw.circle(screen, BLUE, (screen_x, screen_y), 15)
    
    # Выводим математические координаты
    text1 = font.render(f"Математические: ({robot_x:.0f}, {robot_y:.0f})", True, BLACK)
    text2 = font.render(f"Экранные: ({screen_x}, {screen_y})", True, BLACK)
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 35))
    
    # Обновляем экран
    pygame.display.flip()
    
    # Контроль FPS
    clock.tick(60)

# Завершение
pygame.quit()