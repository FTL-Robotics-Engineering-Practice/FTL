"""Главный файл программы - редактор препятствий"""
import pygame
import sys

from grid import Grid
from history import History
from renderer import Renderer
from input_manager import InputManager
from mode_manager import ModeManager
from robot import Robot

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

    # Часы
    clock = pygame.time.Clock()

    # Флаг работы (используем список, чтобы InputManager мог его изменять)
    running = [True]

    grid = Grid(GRID_WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT, offset_x=PANEL_WIDTH)
    history = History()
    renderer = Renderer(screen, panel_width=PANEL_WIDTH)
    mode_manager = ModeManager()

    # Создаём робота в центре карты
    robot = Robot(
        x=GRID_COLS / 2.0,
        y=GRID_ROWS / 2.0,
        angle=0.0,
        radius=1.0
    )

    # Создаём менеджер ввода (теперь с robot)
    input_manager = InputManager(grid, history, running, mode_manager, robot)  

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

        input_manager.update_robot_velocities()

        # Обновляем позицию робота (если в режиме ROBOT)
        if mode_manager.is_robot_mode():
            #robot.update(dt=0.016)
            # TODO: НОВЫЙ КОД - используем проверку столкновений
            robot.update_with_collision_check(dt=0.016, grid=grid)  

            # Ограничиваем робота границами карты
            robot.clamp_position(robot.radius, grid.cols - robot.radius,
                                robot.radius, grid.rows - robot.radius)

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
        clock.tick(60)

    # Завершение
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()