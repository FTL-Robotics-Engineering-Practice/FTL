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
from sight import Sight
from brain import Brain


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
        x=950,  # Центр мира
        y=50,
        angle=0.0
    )
    renderer = Renderer(screen, panel_width=PANEL_WIDTH)
    mode_manager = ModeManager()  # Начинаем с режима редактирования карты
    input_manager = InputManager(robot, grid, history, map_manager, mode_manager, running)
    sight = Sight(radius=5)  # Область видения радиусом 5 клеток
    brain = Brain(kp=7  , linear_velocity=50.0)  # P-контроллер с линейной скоростью 50

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

        # Обновляем робота (в режиме робота или Brain)
        if mode_manager.is_robot_mode() or mode_manager.is_brain_mode():
            # Обновляем область видения
            old_obstacle_count = len(sight.obstacle_cells)
            sight.update(robot, grid)
            # Выводим в консоль только если изменилось количество препятствий
            if len(sight.obstacle_cells) != old_obstacle_count:
                sight.print_debug_info()
            
            # Обновляем brain в обоих режимах (для вычисления целевого угла)
            brain.update(robot, sight, grid)
            
            # В режиме ROBOT перезаписываем скорости из input_manager (ручное управление)
            if mode_manager.is_robot_mode():
                # Обновляем скорости робота на основе нажатых клавиш ПОСЛЕ brain.update()
                # чтобы ручное управление имело приоритет
                input_manager.update()
            
            # Обновляем позицию робота с проверкой границ
            robot.update(dt, grid)

        # Отрисовка
        renderer.clear_screen()

        # Определяем клетку под курсором (для подсветки в режиме карты)
        hover_cell = None
        if mode_manager.is_map_mode():
            hover_cell = grid.get_cell_at_position(mouse_x, mouse_y)

        renderer.draw_grid(grid, hover_cell)
        renderer.draw_axes(grid, points)

        # Рисуем робота в режиме робота или Brain
        if mode_manager.is_robot_mode() or mode_manager.is_brain_mode():
            renderer.draw_sight_zone(sight, grid)
            renderer.draw_collision_zone(robot, grid)
            renderer.draw_robot(robot)
            renderer.draw_sight_line(robot, sight)
            
        renderer.draw_info_panel(robot=robot, brain=brain, mode_manager=mode_manager, grid=grid, points=points, sight=sight)

        # Обновление экрана
        pygame.display.flip()

    # Завершение
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
