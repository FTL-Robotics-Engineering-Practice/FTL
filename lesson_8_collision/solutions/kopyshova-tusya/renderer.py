"""Модуль для отрисовки сетки и интерфейса"""
import pygame

class Renderer:
    """Класс для отрисовки элементов редактора"""

    def __init__(self, screen, panel_width=0):
        """
        Инициализация рендерера

        Args:
            screen: экран pygame для отрисовки
        """
        self.screen = screen
        self.panel_width = panel_width

        # Цвета
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (100, 100, 100)
        self.BLUE = (150, 150, 255)
        self.BLACK = (0, 0, 0)

        import pygame
        self.font = pygame.font.Font(None, 20)

    def draw_grid(self, grid, hover_cell=None):
        """
        Отрисовать сетку на экране

        Args:
            grid: объект Grid с данными сетки
            hover_cell: клетка под курсором (col, row) или None
        """
        # Очистить экран
        self.screen.fill(self.WHITE)

        # TODO: Нарисовать все заполненные клетки
        for col, row in grid.filled_cells:
            x = col * grid.cell_width + grid.offset_x
            y = row * grid.cell_height
            pygame.draw.rect(self.screen, self.DARK_GRAY, (x, y, grid.cell_width, grid.cell_height))

        # TODO: Нарисовать подсветку клетки под курсором
        if hover_cell is not None:
            col, row = hover_cell
            if not grid.is_cell_filled(col, row):
                x = col * grid.cell_width + grid.offset_x
                y = row * grid.cell_height
                pygame.draw.rect(self.screen, self.BLUE, (x, y, grid.cell_width, grid.cell_height))

        # TODO: Нарисовать линии сетки
        # Вертикальные линии
        for col in range(grid.cols + 1):
            x = col * grid.cell_width + grid.offset_x
            pygame.draw.line(self.screen, self.GRAY, (x, 0), (x, grid.height), 1)

        # Горизонтальные линии
        for row in range(grid.rows + 1):
            y = row * grid.cell_height
            pygame.draw.line(self.screen, self.GRAY, (0, y), (grid.width + grid.offset_x, y), 1)

    def draw_robot(self, robot, grid):
        """
        Отрисовать робота на сетке

        Args:
            robot: объект Robot
            grid: объект Grid (для преобразования координат)
        """
        # TODO: Преобразуем координаты робота из клеток в пиксели
        # Формула: screen_x = robot.x * grid.cell_width + grid.offset_x
        screen_x = robot.x * grid.cell_width + grid.offset_x
        screen_y = robot.y * grid.cell_height 

        # TODO: Преобразуем радиус робота из клеток в пиксели
        # Используем среднее между cell_width и cell_height для радиуса
        radius_pixels = int(robot.radius * (grid.cell_width + grid.cell_height) / 2)

        # TODO: Нарисуйте круг робота
        # pygame.draw.circle(surface, color, center, radius)
        # Цвет: (0, 200, 0) - зелёный
        # center: (int(screen_x), int(screen_y))
        pygame.draw.circle(
            self.screen,
            (0, 200, 0),  # зелёный цвет
            (int(screen_x), int(screen_y)),
            radius_pixels  # radius_pixels
        )

        # Линия от центра робота в направлении robot.angle
        import math

        # Вычисляем конец линии (длина = radius_pixels)
        end_x = screen_x + radius_pixels * math.cos(robot.angle)
        end_y = screen_y + radius_pixels * math.sin(robot.angle)

        # pygame.draw.line(surface, color, start_pos, end_pos, width)
        pygame.draw.line(
            self.screen,
            (0, 100, 0),  # темно-зелёный
            (int(screen_x), int(screen_y)),  # начало - центр робота
            (int(end_x), int(end_y)),            # конец - в направлении angle
            3 # толщина 3 пикселя
        )

    def draw_detection_zones(self, robot, grid):
        """
        Отрисовать зоны обнаружения робота

        Args:
            robot: объект Robot
            grid: объект Grid
        """
        # Получаем клетки в зонах
        detection_cells = robot.get_detection_zone_cells(grid)
        forward_cells = robot.get_forward_sector_cells(grid)

        # Рисуем зону обнаружения (синюю), исключая передний сектор
        for col, row in detection_cells:
            # Пропускаем клетки переднего сектора - они будут нарисованы отдельно
            if (col, row) not in forward_cells:
                x = col * grid.cell_width + grid.offset_x
                y = row * grid.cell_height

                # Создаём полупрозрачную поверхность
                surface = pygame.Surface((grid.cell_width, grid.cell_height))
                surface.set_alpha(50)  
                surface.fill((100, 150, 255))  # светло-синий
                self.screen.blit(surface, (x, y))

        # Рисуем передний сектор (жёлтый/красный) поверх зоны обнаружения
        for col, row in forward_cells:
            x = col * grid.cell_width + grid.offset_x
            y = row * grid.cell_height

            # Проверяем, заполнена ли клетка препятствием
            if grid.is_cell_filled(col, row):
                # Препятствие впереди - красный!
                color = (255, 100, 100)
            else:
                # Пусто - жёлтый
                color = (255, 255, 100)

            surface = pygame.Surface((grid.cell_width, grid.cell_height))
            surface.set_alpha(50)
            surface.fill(color)
            self.screen.blit(surface, (x, y))

    def draw_info_panel(self, robot=None, mode_manager=None, grid=None):
        """
        Отрисовать информационную панель слева

        Args:
            robot: объект Robot (или None в режиме карты)
            mode_manager: объект ModeManager
            grid: объект Grid (для подсчёта препятствий) 
        """
        # Если панели нет - выходим
        if self.panel_width == 0:
            return

        # Рисуем фон панели (тёмно-серый)
        pygame.draw.rect(
            self.screen,
            (50, 50, 50),  # тёмно-серый
            (0, 0, self.panel_width , self.screen.get_height()) 
        )

        # Начальная позиция текста
        y_offset = 10

        # TODO: Функция для отрисовки строки текста
        def draw_text(text, color=(255, 255, 255)):
            """Вспомогательная функция для отрисовки текста"""
            nonlocal y_offset  # Используем внешнюю переменную y_offset

            text_surface = self.font.render(text, True, color)
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 25  # 25 - расстояние между строками

        # Заголовок - текущий режим
        if mode_manager is not None:
            mode_name = mode_manager.get_mode_name()
            draw_text(f"Режим: {mode_name}", color=(255, 255, 0))  # mode_name, жёлтый (255, 255, 0)
            draw_text("")  # Пустая строка для отступа

        # Если в режиме карты - показываем инструкции
        if mode_manager is not None and mode_manager.is_map_mode():
            draw_text("РЕДАКТОР КАРТЫ", color=(100, 200, 255))
            draw_text("")
            draw_text("ЛКМ - рисовать")
            draw_text("ПКМ - стирать")
            draw_text("Z - отменить")
            draw_text("C - очистить всё")
            draw_text("TAB - режим робота")

        # Если в режиме робота - показываем данные робота
        elif robot is not None:
            draw_text("РОБОТ", color=(0, 255, 100))
            draw_text("")

            # Координаты
            draw_text(f"X: {robot.x:.2f}")
            draw_text(f"Y: {robot.y:.2f}")
            draw_text("")

            # Угол (в градусах)
            import math
            angle_deg = math.degrees(robot.angle)  
            draw_text(f"Угол: {angle_deg:.1f}°")
            draw_text("")

            # Скорости
            draw_text(f"V лин: {robot.linear_velocity:.2f}") 
            draw_text(f"V угл: {robot.angular_velocity:.2f}")  
            draw_text("")

            # TODO: Препятствия в зонах (если есть grid)
            if grid is not None:
                draw_text("")
                draw_text("ПРЕПЯТСТВИЯ:")

                # Получаем зоны
                detection_cells = robot.get_detection_zone_cells(grid)
                forward_cells = robot.get_forward_sector_cells(grid)

                # Считаем препятствия
                obstacles_in_zone = sum(1 for col, row in detection_cells
                                       if grid.is_cell_filled(col, row))
                obstacles_ahead = sum(1 for col, row in forward_cells
                                     if grid.is_cell_filled(col, row))

                # Выводим с цветовой индикацией
                draw_text(f"В зоне: {obstacles_in_zone}")

                # Если впереди препятствие - красный цвет!
                ahead_color = (255, 100, 100) if obstacles_ahead > 0 else (255, 255, 255)
                draw_text(f"Впереди: {obstacles_ahead}", color=ahead_color)

            draw_text("")

            # Для этого нужно передать grid в параметры метода
            draw_text("УПРАВЛЕНИЕ:")
            draw_text("W - вперёд")
            draw_text("S - назад")
            draw_text("A - влево")
            draw_text("D - вправо")
            draw_text("TAB - режим карты")