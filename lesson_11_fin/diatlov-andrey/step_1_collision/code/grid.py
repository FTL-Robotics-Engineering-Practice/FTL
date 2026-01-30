"""Модуль для работы с сеткой"""


class Grid:
    """Класс сетки с клетками"""

    def __init__(self, width, height, cell_width, cell_height, offset_x=0):
        """
        Инициализация сетки

        Args:
            width: ширина сетки в пикселях
            height: высота сетки в пикселях
            cell_width: ширина одной клетки в пикселях
            cell_height: высота одной клетки в пикселях
            offset_x: смещение по X (для боковой панели)
        """
        self.width = width
        self.height = height
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.offset_x = offset_x

        # Вычисляем количество клеток
        self.cols = width // cell_width
        self.rows = height // cell_height

        # Множество заполненных клеток (препятствия)
        self.filled_cells = set()

    def cell_to_pixels(self, cell_x, cell_y):
        """
        Преобразовать координаты клетки в пиксели

        Args:
            cell_x: координата X в клетках
            cell_y: координата Y в клетках

        Returns:
            tuple: (pixel_x, pixel_y) - координаты в пикселях
        """
        pixel_x = cell_x * self.cell_width + self.offset_x
        pixel_y = cell_y * self.cell_height
        return (pixel_x, pixel_y)

    def pixels_to_cell(self, pixel_x, pixel_y):
        """
        Преобразовать координаты пикселей в клетки

        Args:
            pixel_x: координата X в пикселях
            pixel_y: координата Y в пикселях

        Returns:
            tuple: (cell_x, cell_y) - координаты в клетках (float)
        """
        cell_x = (pixel_x - self.offset_x) / self.cell_width
        cell_y = pixel_y / self.cell_height
        return (cell_x, cell_y)

    def get_cell_at_position(self, pixel_x, pixel_y):
        """
        Получить клетку по координатам пикселей

        Args:
            pixel_x: координата X в пикселях
            pixel_y: координата Y в пикселях

        Returns:
            tuple: (col, row) или None если вне сетки
        """
        if pixel_x < self.offset_x or pixel_x >= self.offset_x + self.width:
            return None
        if pixel_y < 0 or pixel_y >= self.height:
            return None

        col = int((pixel_x - self.offset_x) // self.cell_width)
        row = int(pixel_y // self.cell_height)

        if 0 <= col < self.cols and 0 <= row < self.rows:
            return (col, row)
        return None

    def fill_cell(self, col, row):
        """
        Заполнить клетку (добавить препятствие)

        Args:
            col: колонка
            row: строка
        """
        if 0 <= col < self.cols and 0 <= row < self.rows:
            self.filled_cells.add((col, row))

    def clear_cell(self, col, row):
        """
        Очистить клетку (убрать препятствие)

        Args:
            col: колонка
            row: строка
        """
        self.filled_cells.discard((col, row))

    def is_cell_filled(self, col, row):
        """
        Проверить, заполнена ли клетка

        Args:
            col: колонка
            row: строка

        Returns:
            bool: True если заполнена
        """
        return (col, row) in self.filled_cells

    def clear_all(self):
        """Очистить все заполненные клетки"""
        self.filled_cells = set()
