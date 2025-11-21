"""Главный файл программы - редактор препятствий"""
import pygame
import sys

from grid import Grid
from history import History
from renderer import Renderer
from input_manager import InputManager
from mode_manager import ModeManager  # <-- ДОБАВЛЕНО
from robot import Robot                # <-- ДОБАВЛЕНО

def main():
    """Главная функция программы"""
    # Инициализация pygame
    pygame.init()

    # Настройки окна
    PANEL_WIDTH = 200  # <-- ДОБАВЛЕНО: ширина левой панели
    GRID_WIDTH = 800   # <-- ИЗМЕНЕНО: ширина области сетки
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
        # Создаём объекты (с учётом панели)
    grid = Grid(GRID_WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT, offset_x=PANEL_WIDTH)  # PANEL_WIDTH
    history = History()
    renderer = Renderer(screen, panel_width=PANEL_WIDTH)  # PANEL_WIDTH
    mode_manager = ModeManager()
        # Создаём менеджер ввода (теперь с robot)
    

    robot = Robot(
        x=GRID_COLS / 2.0,
        y=GRID_ROWS / 2.0,
        angle=0.0,
        radius=1.0
    )

    input_manager = InputManager(grid, history, running, mode_manager, robot)
    print("Редактор препятствий запущен!")
    print("Нажмите H для справки по управлению")

        # Игровой цикл
    # Игровой цикл
    while running[0]:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running[0] = False
            else:
                input_manager.handle_event(event)

        # Получаем позицию мыши
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # TODO: Обновляем скорости робота на основе нажатых клавиш
        input_manager.update_robot_velocities()

        # Обновляем робота только в режиме ROBOT
                # Обновляем робота только в режиме ROBOT
        if mode_manager.is_robot_mode():
            # СТАРЫЙ КОД - УДАЛИТЕ:
            # robot.update(dt=0.016)

            # TODO: НОВЫЙ КОД - используем проверку столкновений
            robot.update_with_collision_check(dt=0.016, grid=grid)  # update_with_collision_check

            # Ограничиваем робота границами карты
            robot.clamp_position(robot.radius, grid.cols - robot.radius,
                                robot.radius, grid.rows - robot.radius)

        # ... остальной код без изменений

        # TODO: Определяем клетку под курсором только в режиме MAP_EDIT
        hover_cell = None       
        if mode_manager.is_map_mode():
            hover_cell = grid.get_cell_at_position(mouse_x, mouse_y)
            input_manager.handle_mouse_motion(mouse_x, mouse_y)

        # Отрисовка
        renderer.draw_grid(grid, hover_cell=hover_cell)

        # TODO: Рисуем робота только в режиме ROBOT
        # Рисуем робота только в режиме ROBOT
        if mode_manager.is_robot_mode():
            # TODO: Сначала рисуем зоны обнаружения (под роботом)
            renderer.draw_detection_zones(robot, grid)

            # Потом рисуем робота поверх зон
            renderer.draw_robot(robot, grid)
        # Рисуем робота только в режиме ROBOT
        if mode_manager.is_robot_mode():
            renderer.draw_detection_zones(robot, grid)
            renderer.draw_robot(robot, grid)

        # TODO: Рисуем информационную панель слева
        renderer.draw_info_panel(
            robot=robot if mode_manager.is_robot_mode() else None,  # robot
            mode_manager=mode_manager  # mode_manager
        )

        # Обновление экрана
        pygame.display.flip()
        # Обновление экрана
        pygame.display.flip()
        clock.tick(60)

    # Завершение
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()