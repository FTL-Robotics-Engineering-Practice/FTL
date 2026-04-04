"""Модуль для сохранения и загрузки карт"""
import json

class MapManager:
    """Класс для работы с сохранением/загрузкой карт в JSON"""

    def __init__(self, filename="map.json"):
        """
        Инициализация менеджера карт

        Args:
            filename: имя файла для сохранения/загрузки
        """
        self.filename = filename

    def save_map(self, grid):
        """
        Сохранить карту в файл

        Args:
            grid: объект Grid с сеткой

        Returns:
            True если сохранение успешно, False иначе
        """
        try:
            # TODO: Преобразуйте множество клеток в список
            # JSON не умеет работать с множествами, только со списками
            filled_cells_list = list(grid.filled_cells)

            # TODO: Создайте словарь с данными карты
            map_data = {
                "grid_cols": grid.cols,      # grid.cols
                "grid_rows": grid.rows,      # grid.rows
                "cell_width": grid.cell_width,     # grid.cell_width
                "cell_height": grid.cell_height,    # grid.cell_height
                "filled_cells": filled_cells_list    # filled_cells_list
            }

            # TODO: Сохраните в файл
            # open() с режимом 'w' (write) создаёт/перезаписывает файл
            # encoding='utf-8' для поддержки русских символов
            # indent=2 для красивого форматирования
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(map_data, f, indent=2)

            print(f"✅ Карта сохранена в файл: {self.filename}")
            print(f"   Клеток сохранено: {len(filled_cells_list)}")
            return True

        except Exception as e:
            print(f"❌ Ошибка при сохранении: {e}")
            return False

    def load_map(self, grid):
        """
        Загрузить карту из файла

        Args:
            grid: объект Grid с сеткой

        Returns:
            True если загрузка успешна, False иначе
        """
        try:
            # TODO: Загрузите данные из файла
            with open(self.filename, 'r', encoding='utf-8') as f:
                map_data = json.load(f)

            # TODO: Проверьте совместимость размеров сетки
            if (map_data["grid_cols"] != grid.cols or
                map_data["grid_rows"] != grid.rows):
                print(f"⚠️ Предупреждение: размер сетки в файле не совпадает!")
                print(f"   Файл: {map_data['grid_cols']}×{map_data['grid_rows']}")
                print(f"   Текущий: {grid.cols}×{grid.rows}")

            # TODO: Очистите текущую карту
            grid.clear_all()

            # TODO: Загрузите клетки из файла
            loaded_count = 0
            for cell in map_data["filled_cells"]:
                col, row = cell

                # Проверяем, что клетка в пределах текущей сетки
                if 0 <= col < grid.cols and 0 <= row < grid.rows:
                    grid.fill_cell(col, row)
                    loaded_count += 1

            print(f"✅ Карта загружена из файла: {self.filename}")
            print(f"   Клеток загружено: {loaded_count}")
            return True

        except FileNotFoundError:
            print(f"❌ Файл не найден: {self.filename}")
            return False

        except Exception as e:
            print(f"❌ Ошибка при загрузке: {e}")
            return False