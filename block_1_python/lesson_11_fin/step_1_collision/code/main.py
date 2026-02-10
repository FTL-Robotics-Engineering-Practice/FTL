"""Главный файл программы - робот с редактором карт"""
import pygame
import sys
from robot import Robot
from renderer import Renderer
from mode_manager import ModeManager
from input_manager import InputManager
from grid import Grid
from points import Points
from history import History
from map_manager import MapManager


def main():
    """Главная функция программы"""
    # Инициализация pygame
    pygame.init()

    # Настройки окна
    PANEL_WIDTH = 200
    WORLD_WIDTH = 800
    WIDTH = PANEL_WIDTH + WORLD_WIDTH
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Робот - Ручной режим")

    # Настройки сетки
    CELL_SIZE = 10  # Размер клетки в пикселях
    grid = Grid(
        width=WORLD_WIDTH,
        height=HEIGHT,
        cell_width=CELL_SIZE,
        cell_height=CELL_SIZE,
        offset_x=PANEL_WIDTH
    )

    # Создаем точки (сетка с шагом 100 пикселей)
    points = Points(grid, step=100)

    # История и менеджер карт
    history = History()
    map_manager = MapManager()

    # Флаг работы программы
    running = [True]

    # Создаем объекты
    robot = Robot(
        x=PANEL_WIDTH + WORLD_WIDTH // 2,  # Центр мира
        y=HEIGHT // 2,
        angle=0.0
    )
    renderer = Renderer(screen, panel_width=PANEL_WIDTH)
    mode_manager = ModeManager()  # Начинаем с режима редактирования карты
    input_manager = InputManager(robot, grid, history, map_manager, mode_manager, running)

    # Часы для контроля FPS
    clock = pygame.time.Clock()

    # Игровой цикл
    while running[0]:
        # Вычисляем dt в секундах
        dt = clock.tick(60) / 1000.0  # 60 FPS

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running[0] = False
            else:
                input_manager.handle_event(event)

        # Получаем позицию мыши
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Обрабатываем рисование мышью (в режиме карты)
        if mode_manager.is_map_mode():
            input_manager.handle_mouse_motion(mouse_x, mouse_y)

        # Обновляем скорости робота на основе нажатых клавиш (в режиме робота)
        input_manager.update()

        # Обновляем робота (только в режиме робота)
        if mode_manager.is_robot_mode():
            robot.update(dt)

        # Отрисовка
        renderer.clear_screen()

        # Определяем клетку под курсором (для подсветки в режиме карты)
        hover_cell = None
        if mode_manager.is_map_mode():
            hover_cell = grid.get_cell_at_position(mouse_x, mouse_y)

        renderer.draw_grid(grid, hover_cell)
        renderer.draw_axes(grid, points)

        # Рисуем робота только в режиме робота
        if mode_manager.is_robot_mode():
            renderer.draw_collision_zone(robot, grid)
            renderer.draw_robot(robot)

        renderer.draw_info_panel(robot, mode_manager, grid, points)

        # Обновление экрана
        pygame.display.flip()

    # Завершение
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
