"""Модуль для работы с сеткой препятствий"""

class Grid:
    """Класс для управления сеткой препятствий"""

    def __init__(self, width, height, cell_width, cell_height, offset_x=0):
        """
        Инициализация сетки

        Args:
            width: ширина окна в пикселях
            height: высота окна в пикселях
            cell_width: ширина одной клетки
            cell_height: высота одной клетки
            offset_x: смещение сетки по X (для панели слева)
        """
        self.width = width
        self.height = height
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.offset_x = offset_x  # <-- ДОБАВЬТЕ ЭТУ СТРОКУ

        # Вычисляем количество клеток
        self.cols = width // cell_width
        self.rows = height // cell_height

        # Множество заполненных клеток
        self.filled_cells = set()

    def get_cell_at_position(self, x, y):
        """
        Получить индексы клетки по экранным координатам

        Args:
            x: координата X курсора мыши
            y: координата Y курсора мыши

        Returns:
            (col, row) - индексы клетки или None, если вне границ
        """
        # TODO: Учитываем смещение сетки
        x = x - self.offset_x

        # Проверяем границы
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None

        col = int(x // self.cell_width)
        row = int(y // self.cell_height)

        return (col, row)

    def fill_cell(self, col, row):
        """Заполнить клетку"""
        self.filled_cells.add((col, row))

    def clear_cell(self, col, row):
        """Очистить клетку"""
        self.filled_cells.discard((col, row))

    def is_cell_filled(self, col, row):
        """Проверить, заполнена ли клетка"""
        return (col, row) in self.filled_cells

    def clear_all(self):
        """Очистить все клетки"""
        self.filled_cells.clear()