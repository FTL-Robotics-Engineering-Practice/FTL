"""Модуль для отрисовки экрана и боковой панели"""
import pygame
import math


class Renderer:
    """Класс для отрисовки робота и информационной панели"""

    def __init__(self, screen, panel_width=200):
        """
        Инициализация рендерера

        Args:
            screen: экран pygame
            panel_width: ширина боковой панели
        """
        self.screen = screen
        self.panel_width = panel_width

        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.DARK_GRAY = (50, 50, 50)
        self.LIGHT_GRAY = (200, 200, 200)
        self.GREEN = (0, 200, 0)
        self.YELLOW = (255, 255, 0)

        # Шрифты
        self.font = pygame.font.Font(None, 15)
        self.small_font = pygame.font.Font(None, 15)

    def draw_grid(self, grid, hover_cell=None):
        """
        Отрисовать сетку и препятствия

        Args:
            grid: объект Grid
            hover_cell: клетка под курсором (col, row) или None
        """
        # Рисуем заполненные клетки (препятствия)
        for col, row in grid.filled_cells:
            x = col * grid.cell_width + grid.offset_x
            y = row * grid.cell_height
            pygame.draw.rect(
                self.screen,
                self.DARK_GRAY,
                (x, y, grid.cell_width, grid.cell_height)
            )

        # Рисуем подсветку клетки под курсором
        if hover_cell is not None:
            col, row = hover_cell
            if not grid.is_cell_filled(col, row):
                x = col * grid.cell_width + grid.offset_x
                y = row * grid.cell_height
                pygame.draw.rect(
                    self.screen,
                    (150, 150, 255),  # Светло-синий
                    (x, y, grid.cell_width, grid.cell_height)
                )

        # Вертикальные линии
        for col in range(grid.cols + 1):
            x = col * grid.cell_width + grid.offset_x
            pygame.draw.line(
                self.screen,
                self.LIGHT_GRAY,
                (x, 0),
                (x, grid.height),
                1
            )

        # Горизонтальные линии
        for row in range(grid.rows + 1):
            y = row * grid.cell_height
            pygame.draw.line(
                self.screen,
                self.LIGHT_GRAY,
                (grid.offset_x, y),
                (grid.offset_x + grid.width, y),
                1
            )

    def draw_axes(self, grid, axes):
        """
        Отрисовать жирную сетку

        Args:
            grid: объект Grid
            axes: объект Points (жирная сетка)
        """
        color = axes.get_color()
        line_width = axes.get_line_width()

        # Рисуем все вертикальные линии
        for x in axes.get_vertical_lines():
            pygame.draw.line(
                self.screen,
                color,
                (grid.offset_x + x, 0),
                (grid.offset_x + x, grid.height),
                line_width
            )

        # Рисуем все горизонтальные линии
        for y in axes.get_horizontal_lines():
            pygame.draw.line(
                self.screen,
                color,
                (grid.offset_x, y),
                (grid.offset_x + grid.width, y),
                line_width
            )

    def draw_robot(self, robot):
        """
        Отрисовать робота

        Args:
            robot: объект Robot
        """
        # Радиус робота в пикселях
        radius = 15

        # Рисуем круг робота
        pygame.draw.circle(
            self.screen,
            self.GREEN,
            (int(robot.x), int(robot.y)),
            radius
        )

        # Рисуем направление робота (короткая линия)
        line_length = radius * 1.5  # Линия в 1.5 раза длиннее радиуса
        end_x = robot.x + line_length * math.cos(robot.angle)
        end_y = robot.y + line_length * math.sin(robot.angle)
        pygame.draw.line(
            self.screen,
            self.BLACK,
            (int(robot.x), int(robot.y)),
            (int(end_x), int(end_y)),
            3
        )

    def draw_collision_zone(self, robot, grid):
        """
        Отрисовать зону обнаружения коллизий

        Args:
            robot: объект Robot
            grid: объект Grid
        """
        # Получаем клетки переднего сектора
        forward_cells = robot.get_sector_cells(grid, angle_offset=0)

        # Получаем клетки заднего сектора
        backward_cells = robot.get_sector_cells(grid, angle_offset=math.pi)

        # Рисуем передний сектор
        for col, row in forward_cells:
            x = col * grid.cell_width + grid.offset_x
            y = row * grid.cell_height

            # Если препятствие - красный, иначе - зеленый
            if grid.is_cell_filled(col, row):
                color = (255, 100, 100)  # Красный
            else:
                color = (100, 255, 100)  # Зеленый

            # Полупрозрачная заливка
            surface = pygame.Surface((grid.cell_width, grid.cell_height))
            surface.set_alpha(80)
            surface.fill(color)
            self.screen.blit(surface, (x, y))

        # Рисуем задний сектор
        for col, row in backward_cells:
            x = col * grid.cell_width + grid.offset_x
            y = row * grid.cell_height

            # Если препятствие - красный, иначе - желтый
            if grid.is_cell_filled(col, row):
                color = (255, 100, 100)  # Красный
            else:
                color = (255, 255, 100)  # Желтый

            # Полупрозрачная заливка
            surface = pygame.Surface((grid.cell_width, grid.cell_height))
            surface.set_alpha(80)
            surface.fill(color)
            self.screen.blit(surface, (x, y))

    def draw_sight_zone(self, sight, grid):
        """
        Отрисовать область видения

        Args:
            sight: объект Sight
            grid: объект Grid
        """
        # Рисуем все видимые клетки
        for col, row in sight.visible_cells:
            x = col * grid.cell_width + grid.offset_x
            y = row * grid.cell_height

            # Если препятствие - более яркий синий, иначе - светло-голубой
            if (col, row) in sight.obstacle_cells:
                color = (100, 150, 255)  # Светло-синий
                alpha = 150  # Более непрозрачный для препятствий
            else:
                color = (70, 70, 150)  # Очень светло-голубой
                alpha = 30  # Очень прозрачный для пустых клеток

            # Полупрозрачная заливка
            surface = pygame.Surface((grid.cell_width, grid.cell_height))
            surface.set_alpha(alpha)
            surface.fill(color)
            self.screen.blit(surface, (x, y))

        # Рисуем центр масс если есть препятствия
        if sight.center_of_mass:
            cx, cy = sight.center_of_mass
            # Рисуем красную точку
            pygame.draw.circle(
                self.screen,
                (255, 0, 0),  # Красный
                (int(cx), int(cy)),
                5
            )

    def draw_sight_line(self, robot, sight):
        """
        Отрисовать линию от робота до центра масс препятствий

        Args:
            robot: объект Robot
            sight: объект Sight
        """
        if sight.center_of_mass:
            cx, cy = sight.center_of_mass
            pygame.draw.line(
                self.screen,
                (255, 0, 0),  # Красный
                (int(robot.x), int(robot.y)),
                (int(cx), int(cy)),
                2
            )

    def draw_info_panel(self, robot, mode_manager, brain, grid=None, points=None, sight=None):
        """
        Отрисовать информационную панель

        Args:
            robot: объект Robot
            mode_manager: объект ModeManager
            grid: объект Grid (опционально)
            points: объект Points (опционально)
            sight: объект Sight (опционально)
        """
        # Фон панели
        pygame.draw.rect(
            self.screen,
            self.DARK_GRAY,
            (0, 0, self.panel_width, self.screen.get_height())
        )

        y_offset = 20

        def draw_text(text, color=None, font=None):
            """Вспомогательная функция для отрисовки текста"""
            nonlocal y_offset
            if color is None:
                color = self.WHITE
            if font is None:
                font = self.font

            text_surface = font.render(text, True, color)
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 15

        # Режим
        mode_name = mode_manager.get_mode_name()
        draw_text(mode_name, color=self.YELLOW)
        draw_text("")  # Пустая строка

        # Позиция робота
        draw_text("ПОЗИЦИЯ:", color=self.YELLOW)
        draw_text(f"X: {robot.x:.1f} px")
        draw_text(f"Y: {robot.y:.1f} px")
        draw_text("")  # Пустая строка

        # Угол
        angle_deg = math.degrees(robot.angle) % 360
        draw_text("УГОЛ:", color=self.YELLOW)
        draw_text(f"{angle_deg:.1f}°")
        draw_text("")  # Пустая строка

        # TODO ЗАДАНИЕ 5: Вывести угол до препятствий, целевой угол и ошибку
        if ...:  # sight is not None and sight.center_of_mass
            cx, cy = ...  # получить координаты центра масс
            # Вектор от робота до центра масс
            dx = ...
            dy = ...
            # Угол к центру масс
            target_angle = ...  # math.atan2(dy, dx)
            # Разница углов
            angle_diff = ...  # target_angle - robot.angle
            
            # Нормализовать в диапазон [-π, π]
            while ...:  # angle_diff > math.pi
                angle_diff -= ...
            while ...:  # angle_diff < -math.pi
                angle_diff += ...
            
            # Конвертировать в градусы
            angle_diff_deg = ...  # math.degrees(angle_diff)
            
            draw_text("УГОЛ ДО ПРЕПЯТСТВИЙ:", color=self.YELLOW)
            draw_text(f"{angle_diff_deg:.1f}°")
            draw_text("ЦЕЛЬ:", color=self.YELLOW)
            draw_text(f"{...:.1f}°")  # math.degrees(brain.target_angle)
            draw_text("ОШИБКА:", color=self.YELLOW)
            error = ...  # angle_diff_deg - math.degrees(brain.target_angle)
            draw_text(f"{error:.1f}°")
            draw_text("")  # Пустая строка

        # Скорости
        draw_text("СКОРОСТИ:", color=self.YELLOW)
        draw_text(f"Линейная: {robot.linear_velocity:.1f}")
        draw_text(f"Угловая: {robot.angular_velocity:.2f}")
        draw_text("")  # Пустая строка

        # Жирная сетка (если переданы)
        if grid is not None and points is not None:
            draw_text("ЖИРНАЯ СЕТКА:", color=self.YELLOW)
            draw_text(f"Шаг: {points.step} px", font=self.small_font)
            draw_text(f"Толщина: {points.get_line_width()} px", font=self.small_font)
            draw_text("")  # Пустая строка

        # Управление (зависит от режима)
        if mode_manager.is_map_mode():
            draw_text("УПРАВЛЕНИЕ:", color=self.YELLOW)
            draw_text("ЛКМ - рисовать", font=self.small_font)
            draw_text("ПКМ - стирать", font=self.small_font)
            draw_text("Z - отменить", font=self.small_font)
            draw_text("C - очистить", font=self.small_font)
            draw_text("K - сохранить", font=self.small_font)
            draw_text("L - загрузить", font=self.small_font)
            draw_text("TAB - робот", font=self.small_font)
        else:
            draw_text("УПРАВЛЕНИЕ:", color=self.YELLOW)
            draw_text("W - вперед", font=self.small_font)
            draw_text("S - назад", font=self.small_font)
            draw_text("A - влево", font=self.small_font)
            draw_text("D - вправо", font=self.small_font)
            draw_text("TAB - карта", font=self.small_font)

    def clear_screen(self):
        """Очистить экран"""
        self.screen.fill(self.WHITE)
