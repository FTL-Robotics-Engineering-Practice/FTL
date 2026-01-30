"""Модуль для отрисовки сетки и интерфейса"""
import pygame

class Renderer:
    """Класс для отрисовки элементов редактора"""

    def __init__(self, screen):
        """
        Инициализация рендерера

        Args:
            screen: экран pygame для отрисовки
        """
        self.screen = screen

        # Цвета
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (100, 100, 100)
        self.BLUE = (150, 150, 255)
        self.BLACK = (0, 0, 0)

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
            x = col * grid.cell_width
            y = row * grid.cell_height
            pygame.draw.rect(self.screen, self.DARK_GRAY, (x, y, grid.cell_width, grid.cell_height))

        # TODO: Нарисовать подсветку клетки под курсором
        if hover_cell is not None:
            col, row = hover_cell
            if not grid.is_cell_filled(col, row):
                x = col * grid.cell_width
                y = row * grid.cell_height
                pygame.draw.rect(self.screen, self.BLUE, (x, y, grid.cell_width, grid.cell_height))

        # TODO: Нарисовать линии сетки
        # Вертикальные линии
        for col in range(grid.cols + 1):
            x = col * grid.cell_width
            pygame.draw.line(self.screen, self.GRAY, (x, 0), (x, grid.height), 1)

        # Горизонтальные линии
        for row in range(grid.rows + 1):
            y = row * grid.cell_height
            pygame.draw.line(self.screen, self.GRAY, (0, y), (grid.width, y), 1)