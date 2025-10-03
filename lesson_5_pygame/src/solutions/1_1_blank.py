import pygame

# Инициализация Pygame
pygame.init()

# Создаем окно
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Задание 1.1: Пустое окно")

# Главный игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Заливаем экран белым цветом
    screen.fill((255, 255, 255))
    
    # Обновляем экран
    pygame.display.flip()

# Завершение
pygame.quit()