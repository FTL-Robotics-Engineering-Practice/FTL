"""Тест отрисовки робота"""
import pygame
import sys
from grid import Grid
from renderer import Renderer
from robot import Robot

# Инициализация pygame
pygame.init()

# Настройки окна
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Тест отрисовки робота")

# Настройки сетки
GRID_COLS = 75
GRID_ROWS = 50
CELL_WIDTH = WIDTH // GRID_COLS
CELL_HEIGHT = HEIGHT // GRID_ROWS

# Создаём объекты
grid = Grid(WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT, offset_x=0)
renderer = Renderer(screen)

# Создаём робота в центре карты
robot = Robot(
    x=GRID_COLS / 2.0,  # центр по X
    y=GRID_ROWS / 2.0,  # центр по Y
    angle=0.0,          # смотрит вправо
    radius=1.0
)

# Рисуем несколько препятствий для контекста
grid.fill_cell(35, 20)
grid.fill_cell(36, 20)
grid.fill_cell(37, 20)

clock = pygame.time.Clock()
running = True

print("Тест отрисовки робота")
print("Закройте окно для выхода")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # TODO: ДОБАВЬТЕ ЭТИ СТРОКИ - робот едет по кругу
    robot.set_velocities(linear=5.0, angular=1.0)  # едет и поворачивает
    robot.update(dt=0.016)  # ~60 FPS

    # Ограничиваем робота границами
    robot.clamp_position(robot.radius, grid.cols - robot.radius,
                        robot.radius, grid.rows - robot.radius)

    # Отрисовка
    renderer.draw_grid(grid)
    renderer.draw_robot(robot, grid)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()