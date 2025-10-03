import pygame

# Инициализация Pygame
pygame.init()

# Создаем окно
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Задание 1.2: Круг в центре")

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)

# Главный игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Заливаем экран белым цветом
    screen.fill(WHITE)
    
    # Рисуем синий круг в центре экрана
    # pygame.draw.circle(surface, color, center, radius)
    pygame.draw.circle(screen, BLUE, (400, 300), 15)
    
    # Обновляем экран
    pygame.display.flip()

# Завершение
pygame.quit()