"""Главный файл программы - редактор препятствий"""
import pygame
import sys

from grid import Grid
from history import History
from renderer import Renderer
from input_manager import InputManager
from map_manager import MapManager
from mode_manager import ModeManager
from robot import Robot
from brain import Brain

def main():
    """Главная функция программы"""
    # Инициализация pygame
    pygame.init()

    # Настройки окна
    PANEL_WIDTH = 200 
    GRID_WIDTH = 800   
    WIDTH = WIDTH = PANEL_WIDTH + GRID_WIDTH 
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Редактор препятствий")

    # Настройки сетки
    GRID_COLS = 80
    GRID_ROWS = 60
    CELL_WIDTH = WIDTH // GRID_COLS
    CELL_HEIGHT = HEIGHT // GRID_ROWS

    # Флаг работы (используем список, чтобы InputManager мог его изменять)
    running = [True]

    grid = Grid(GRID_WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT, offset_x=PANEL_WIDTH)
    history = History()
    renderer = Renderer(screen, panel_width=PANEL_WIDTH)
    mode_manager = ModeManager()
    map_manager = MapManager()

    # Создаём робота в центре карты
    robot = Robot(
        x=GRID_COLS / 2.0,
        y=GRID_ROWS / 2.0,
        angle=0.0,
        radius=1.0
    )
    # Часы
    robot.clock = pygame.time.Clock()

    brain = Brain(robot, grid, linear_velocity=5.0, angular_velocity=0.0)

    # Создаём менеджер ввода (теперь с robot)
    input_manager = InputManager(grid, history, map_manager, running, mode_manager, robot)  

    # Отслеживаем предыдущий режим для сброса метрик при переходе в ROBOT
    previous_mode_was_robot = mode_manager.is_robot_mode()

    # Игровой цикл
    while running[0]:
        # Вычисляем реальный delta time в секундах
        dt_ms = robot.clock.tick(60)  # Возвращает миллисекунды с прошлого кадра
        dt = dt_ms / 1000.0  # Конвертируем в секунды

        # Проверяем переход в режим ROBOT и сбрасываем метрики
        current_mode_is_robot = mode_manager.is_robot_mode()
        if current_mode_is_robot and not previous_mode_was_robot:
            # Переход в режим ROBOT - сбрасываем метрики
            robot.reset_metrics()
            # Также сбрасываем флаг в brain для корректного отслеживания столкновений
            brain.was_obstacle_ahead = False
        previous_mode_was_robot = current_mode_is_robot

        # Обновляем время ДО обновления робота
        robot.time = pygame.time.get_ticks() - robot.time_start

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running[0] = False
            else:
                input_manager.handle_event(event)

        # Получаем позицию мыши
        mouse_x, mouse_y = pygame.mouse.get_pos()

        input_manager.update_robot_velocities()

        # Обновляем позицию робота (если в режиме ROBOT)
        if mode_manager.is_robot_mode():

            if input_manager.simu_going:              #ОСТАНОВКА ПРИ ЗАЖАТОЙ Х

                brain.update(dt=dt, robot = robot)

                # Ограничиваем робота границами карты
                robot.clamp_position(robot.radius, grid.cols - robot.radius,
                                    robot.radius, grid.rows - robot.radius)

        else:
            robot.set_velocities(linear=0, angular=0)

        hover_cell = None

        if mode_manager.is_map_mode():
            hover_cell = grid.get_cell_at_position(mouse_x, mouse_y)
            input_manager.handle_mouse_motion(mouse_x, mouse_y)

        # Отрисовка (правильный порядок: сетка -> зоны -> робот)
        renderer.draw_grid(grid, hover_cell=hover_cell)

        if mode_manager.is_robot_mode():
            # Сначала рисуем зоны обнаружения (под роботом)
            renderer.draw_detection_zones(robot, grid)
            # Потом рисуем робота поверх зон
            renderer.draw_robot(robot, grid)

        # Рисуем робота только в режиме ROBOT
        if mode_manager.is_robot_mode():
            renderer.draw_detection_zones(robot, grid)
            renderer.draw_robot(robot, grid)

        # Рисуем информационную панель слева
        renderer.draw_info_panel(
            robot=robot if mode_manager.is_robot_mode() else None, 
            mode_manager=mode_manager,
            grid=grid
        )

        # Обновление экрана
        pygame.display.flip()

    # print(robot.count_colisions)
    # print(robot.time_collisions)
    # print(robot.distance_collisions)
    print("\n=== Статистика робота ===")
    try:
        formatted_times = [round(t, 3) for t in brain.collision_times]
    except Exception:
        formatted_times = []
    print(f"Количество столкновений: {brain.collision_count}")
    print(f"Моменты столкновений (с): {formatted_times}")
    print(f"Длина пройденного пути: {brain.path_length:.2f} клеток")
    # Завершение
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()