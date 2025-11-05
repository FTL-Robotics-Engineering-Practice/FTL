"""Главный файл программы - редактор препятствий"""
import pygame
import sys

from grid import Grid
from history import History
from renderer import Renderer
from input_manager import InputManager
from map_manager import MapManager

def main():
    """Главная функция программы"""
    # Инициализация pygame
    pygame.init()

    # Настройки окна
    WIDTH = 800
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Редактор препятствий")

    # Настройки сетки
    GRID_COLS = 75
    GRID_ROWS = 50
    CELL_WIDTH = WIDTH // GRID_COLS
    CELL_HEIGHT = HEIGHT // GRID_ROWS

    # Часы
    clock = pygame.time.Clock()

    # Флаг работы (используем список, чтобы InputManager мог его изменять)
    running = [True]

    # TODO: Создайте объекты
    grid = Grid(WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT)
    history = History()
    renderer = Renderer(screen)
    map_manager = MapManager()
    input_manager = InputManager(grid, history, map_manager, running)

    print("Редактор препятствий запущен!")
    print("Нажмите H для справки по управлению")

    # Игровой цикл
    while running[0]:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running[0] = False
            else:
                # TODO: Передайте событие в InputManager
                input_manager.handle_event(event)

        # TODO: Получите позицию мыши и передайте в InputManager
        mouse_x, mouse_y = pygame.mouse.get_pos()
        input_manager.handle_mouse_motion(mouse_x, mouse_y)

        # Определяем клетку под курсором для подсветки
        hover_cell = grid.get_cell_at_position(mouse_x, mouse_y)

        # Отрисовка
        renderer.draw_grid(grid, hover_cell=hover_cell)

        # Обновление экрана
        pygame.display.flip()
        clock.tick(60)

    # Завершение
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

"""I tried harder""" 