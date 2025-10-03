import pygame

# Инициализация Pygame
pygame.init()

# Создаем окно
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Задание 2.1: Вывод текста")

# Шрифт для текста
font = pygame.font.Font(None, 24)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 100, 255)


def draw_grid(screen):
    """Рисует сетку координат"""
    for x in range(0, 800, 50):
        color = GRAY if x != 400 else BLACK
        width = 1 if x != 400 else 2
        pygame.draw.line(screen, color, (x, 0), (x, 600), width)
    
    for y in range(0, 600, 50):
        color = GRAY if y != 300 else BLACK
        width = 1 if y != 300 else 2
        pygame.draw.line(screen, color, (0, y), (800, y), width)


# Главный игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Заливаем экран белым цветом
    screen.fill(WHITE)
    
    # Рисуем сетку
    draw_grid(screen)
    
    # Рисуем синий круг в центре
    pygame.draw.circle(screen, BLUE, (400, 300), 15)
    
    # Выводим текст
    text = font.render("Позиция: (0, 0)", True, BLACK)
    screen.blit(text, (10, 10))
    
    # Обновляем экран
    pygame.display.flip()

# Завершение
pygame.quit()