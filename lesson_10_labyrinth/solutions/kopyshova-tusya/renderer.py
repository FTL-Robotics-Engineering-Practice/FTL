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

        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (100, 100, 100)
        self.BLUE = (150, 150, 255)
        self.BLACK = (0, 0, 0)
        self.DARK_GREEN = (35, 101, 51)
        self.LIGHT_GREEN = (194, 218, 184)

        import pygame
        self.font = pygame.font.Font(None, 20)

    def draw_grid(self, grid, hover_cell=None):
        """
        Отрисовать сетку на экране

        Args:
            grid: объект Grid с данными сетки
            hover_cell: клетка под курсором (col, row) или None
        """
        self.screen.fill(self.WHITE)

        for col, row in grid.filled_cells:
            x = col * grid.cell_width + grid.offset_x
            y = row * grid.cell_height
            pygame.draw.rect(self.screen, self.DARK_GRAY, (x, y, grid.cell_width, grid.cell_height))

        if hover_cell is not None:
            col, row = hover_cell
            if not grid.is_cell_filled(col, row):
                x = col * grid.cell_width + grid.offset_x
                y = row * grid.cell_height
                pygame.draw.rect(self.screen, self.BLUE, (x, y, grid.cell_width, grid.cell_height))

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
        #Преобразуем координаты робота из клеток в пиксели
        screen_x = robot.x * grid.cell_width + grid.offset_x
        screen_y = robot.y * grid.cell_height 

        #Преобразуем радиус робота из клеток в пиксели
        radius_pixels = int(robot.radius * (grid.cell_width + grid.cell_height) / 2)

        pygame.draw.circle(
            self.screen,
            (0, 200, 0),  # зелёный цвет
            (int(screen_x), int(screen_y)),
            radius_pixels  
        )

        # Линия от центра робота в направлении robot.angle
        import math

        end_x = screen_x + radius_pixels * math.cos(robot.angle)
        end_y = screen_y + radius_pixels * math.sin(robot.angle)

        pygame.draw.line(
            self.screen,
            (0, 100, 0),  # темно-зелёный
            (int(screen_x), int(screen_y)),  # начало - центр робота
            (int(end_x), int(end_y)),            # конец - в направлении angle
            3 
        )

    def draw_detection_zones(self, robot, grid):
        """
        Отрисовать зоны обнаружения робота

        Args:
            robot: объект Robot
            grid: объект Grid
        """
        detection_cells = robot.get_detection_zone_cells(grid)
        forward_cells = robot.get_forward_sector_cells(grid)

        for col, row in detection_cells:
            if (col, row) not in forward_cells:
                x = col * grid.cell_width + grid.offset_x
                y = row * grid.cell_height

                surface = pygame.Surface((grid.cell_width, grid.cell_height))
                surface.set_alpha(50)  
                surface.fill((100, 150, 255))  # светло-синий
                self.screen.blit(surface, (x, y))

        for col, row in forward_cells:
            x = col * grid.cell_width + grid.offset_x
            y = row * grid.cell_height

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
        if self.panel_width == 0:
            return

        pygame.draw.rect(
            self.screen,
            (50, 50, 50),  # тёмно-серый
            (0, 0, self.panel_width , self.screen.get_height()) 
        )

        y_offset = 10

        def draw_text(text, color=(255, 255, 255)):
            """Вспомогательная функция для отрисовки текста"""
            nonlocal y_offset  

            text_surface = self.font.render(text, True, color)
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 25  

        if mode_manager is not None:
            mode_name = mode_manager.get_mode_name()
            draw_text(f"Режим: {mode_name}", color=(255, 255, 0)) 
            draw_text("")  

        if mode_manager is not None and mode_manager.is_map_mode():
            draw_text("РЕДАКТОР КАРТЫ", color=(100, 200, 255))
            draw_text("")
            draw_text("ЛКМ - рисовать")
            draw_text("ПКМ - стирать")
            draw_text("Z - отменить")
            draw_text("C - очистить всё")
            draw_text("TAB - режим робота")

        elif robot is not None:
            draw_text("РОБОТ", color=(0, 255, 100))
            draw_text("")

            draw_text(f"X: {robot.x:.2f}")
            draw_text(f"Y: {robot.y:.2f}")
            draw_text("")

            import math
            angle_deg = math.degrees(robot.angle)  
            draw_text(f"Угол: {angle_deg:.1f}°")
            draw_text("")

            draw_text(f"V лин: {robot.linear_velocity:.2f}") 
            draw_text(f"V угл: {robot.angular_velocity:.2f}")  
            draw_text("")

            if grid is not None:
                draw_text("")
                draw_text("ПРЕПЯТСТВИЯ:")

                detection_cells = robot.get_detection_zone_cells(grid)
                forward_cells = robot.get_forward_sector_cells(grid)

                obstacles_in_zone = sum(1 for col, row in detection_cells
                                       if grid.is_cell_filled(col, row))
                obstacles_ahead = sum(1 for col, row in forward_cells
                                     if grid.is_cell_filled(col, row))

                draw_text(f"В зоне: {obstacles_in_zone}")

                ahead_color = (255, 100, 100) if obstacles_ahead > 0 else (255, 255, 255)
                draw_text(f"Впереди: {obstacles_ahead}", color=ahead_color)

            draw_text("")

            draw_text("УПРАВЛЕНИЕ:")
            draw_text("W - вперёд")
            draw_text("S - назад")
            draw_text("A - влево")
            draw_text("D - вправо")
            draw_text("TAB - режим карты")

    def finish_panel(self, robot=None):
        """
        Отрисовать финальную табличку
        
        Args:
            robot: объект Robot (для отображения статистики)
        """
        
        panel_x = 350
        panel_y = 200
        panel_width = 1000 - 2*panel_x
        panel_height = 600 - 2*panel_y
        
        pygame.draw.rect(
            self.screen,
            self.LIGHT_GREEN, 
            (panel_x, panel_y, panel_width, panel_height) 
        )

        pygame.draw.rect(
            self.screen,
            self.DARK_GREEN, 
            (panel_x, panel_y, panel_width, panel_height),
            5  
        )

        text_x = panel_x + (panel_width / 4) + 15
        text_y = panel_y + (panel_height / 2) - 15

        finish_font = pygame.font.Font(None, 48)
        text_surface = finish_font.render("FINISH!", True, self.DARK_GREEN)
        self.screen.blit(text_surface, (text_x, text_y))