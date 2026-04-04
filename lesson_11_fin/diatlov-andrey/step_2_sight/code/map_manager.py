"""Модуль для сохранения и загрузки карт"""
import json
import os


class MapManager:
    """Класс для работы с файлами карт"""

    def __init__(self, default_filename="map.json"):
        """
        Инициализация менеджера карт

        Args:
            default_filename: имя файла по умолчанию
        """
        self.default_filename = default_filename

    def save_map(self, grid, filename=None):
        """
        Сохранить карту в файл

        Args:
            grid: объект Grid с filled_cells
            filename: имя файла (если None, используется default_filename)

        Returns:
            bool: True если успешно, False если ошибка
        """
        if filename is None:
            filename = self.default_filename

        try:
            # Преобразуем set в список для сериализации
            cells_list = [list(cell) for cell in grid.filled_cells]

            data = {
                'cells': cells_list,
                'cols': grid.cols,
                'rows': grid.rows
            }

            with open(filename, 'w') as f:
                json.dump(data, f)

            print(f"Карта сохранена: {filename} ({len(cells_list)} клеток)")
            return True

        except Exception as e:
            print(f"Ошибка сохранения карты: {e}")
            return False

    def load_map(self, grid, filename=None):
        """
        Загрузить карту из файла

        Args:
            grid: объект Grid для загрузки данных
            filename: имя файла (если None, используется default_filename)

        Returns:
            bool: True если успешно, False если ошибка
        """
        if filename is None:
            filename = self.default_filename

        if not os.path.exists(filename):
            print(f"Файл не найден: {filename}")
            return False

        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            # Очищаем текущую карту
            grid.filled_cells = set()

            # Загружаем клетки
            for cell in data['cells']:
                col, row = cell
                grid.filled_cells.add((col, row))

            print(f"Карта загружена: {filename} ({len(data['cells'])} клеток)")
            return True

        except Exception as e:
            print(f"Ошибка загрузки карты: {e}")
            return False
