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
    WIDTH = PANEL_WIDTH + GRID_WIDTH
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
    grid = Grid(GRID_WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT, offset_x=PANEL_WIDTH)
    history = History()
    renderer = Renderer(screen, panel_width=PANEL_WIDTH)  # PANEL_WIDTH
    map_manager = MapManager()
    mode_manager = ModeManager()
    

    # Создаём робота в центре карты
    robot = Robot(
        x=GRID_COLS / 2.0,
        y=GRID_ROWS / 2.0,
        angle=0.0,
        radius=1.0
    )
    input_manager = InputManager(grid, history, map_manager, running, mode_manager, robot)
    brain = Brain(robot, grid)

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

        # input_manager.update_robot_velocities()  # управление вручную (отключено, теперь управляет мозг)

        # TODO: Обновляем робота только в режиме ROBOT
        if mode_manager.is_robot_mode():
            brain.update(dt=0.016)

            # robot.update_with_collision_check(dt=0.016, grid=grid)

            # Ограничиваем робота границами карты
            robot.clamp_position(robot.radius, grid.cols - robot.radius,
                                robot.radius, grid.rows - robot.radius)
        else:
            robot.set_velocities(0.0, 0.0)

        # TODO: Определяем клетку под курсором только в режиме MAP_EDIT
        hover_cell = None
        if mode_manager.is_map_mode():
            hover_cell = grid.get_cell_at_position(mouse_x, mouse_y)
            input_manager.handle_mouse_motion(mouse_x, mouse_y)

        # Отрисовка
        renderer.draw_grid(grid, hover_cell=hover_cell)

                # Рисуем робота только в режиме ROBOT
        if mode_manager.is_robot_mode():
            # TODO: Сначала рисуем зоны обнаружения (под роботом)
            renderer.draw_detection_zones(robot, grid)
            # Потом рисуем робота поверх зон
            renderer.draw_robot(robot, grid)
        
        # TODO: Рисуем информационную панель слева
        renderer.draw_info_panel(
            robot=robot if mode_manager.is_robot_mode() else None,  # robot
            mode_manager=mode_manager,  # mode_manager
            grid=grid
            )
            

        # Обновление экрана
        pygame.display.flip()
        clock.tick(60)
    # Завершение
    print("\n=== Статистика робота ===")
    try:
        formatted_times = [round(t, 3) for t in brain.collision_times]
    except Exception:
        formatted_times = []
    print(f"Количество столкновений: {brain.collision_count}")
    print(f"Моменты столкновений (с): {formatted_times}")
    print(f"Длина пройденного пути: {brain.path_length:.2f} клеток")
    chastota = brain.collision_count / brain.elapsed_time
    print(f"Частота столкновений: {chastota:.2f} столкновений в секунду")
    print(f"Период столкновений: {1/chastota:.2f} секунд")
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

"""I tried harder""" 