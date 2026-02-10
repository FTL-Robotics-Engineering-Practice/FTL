"""Класс для области видения робота"""
import math


# Функция-помощник для нормализации угла
def normalize_angle(angle):
    """Нормализовать угол в диапазон [-π, π]"""
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle


class Sight:
    """Класс для обработки области видения робота"""

    def __init__(self, radius=4):
        """
        Инициализация области видения

        Args:
            radius: радиус области видения в клетках
        """
        self.radius = radius
        self.visible_cells = set()
        self.obstacle_cells = set()
        self.center_of_mass = None

    def update(self, robot, grid):
        """
        Обновить область видения

        Args:
            robot: объект Robot
            grid: объект Grid
        """
        # Получаем все клетки в круге
        self.visible_cells = self.get_visible_cells(robot, grid)

        # TODO: Фильтруем препятствия (Задание 2)
        # Нужно оставить только те клетки из visible_cells, которые заполнены в grid
        # Используйте grid.is_cell_filled(col, row)
        self.obstacle_cells = set()
        for col, row in self.visible_cells:
            if grid.is_cell_filled(col, row):  # проверить, заполнена ли клетка
                self.obstacle_cells.add((col, row))  # добавить в obstacle_cells

        # Вычисляем центр масс препятствий
        self.center_of_mass = self.calculate_center_of_mass(grid)

    def get_visible_cells(self, robot, grid):
        """
        Получить все клетки в секторе 270° (слепая зона сзади 90°)

        Args:
            robot: объект Robot
            grid: объект Grid

        Returns:
            set: множество клеток (col, row) в секторе
        """
        cells = set()

        # Перебираем все клетки в квадрате вокруг робота
        min_col = int((robot.x - grid.offset_x) / grid.cell_width - self.radius)
        max_col = int((robot.x - grid.offset_x) / grid.cell_width + self.radius) + 1
        min_row = int(robot.y / grid.cell_height - self.radius)
        max_row = int(robot.y / grid.cell_height + self.radius) + 1

        # Угол слепой зоны (270° видимость = 90° слепая зона сзади = ±45° от направления назад)
        max_angle_diff = math.radians(135)  # ±135° от направления робота = 270° сектор

        for col in range(min_col, max_col):
            for row in range(min_row, max_row):
                if 0 <= col < grid.cols and 0 <= row < grid.rows:
                    # Центр клетки (с учетом offset_x)
                    cell_x = (col + 0.5) * grid.cell_width + grid.offset_x
                    cell_y = (row + 0.5) * grid.cell_height

                    # Вектор от робота до клетки
                    dx = cell_x - robot.x
                    dy = cell_y - robot.y
                    distance = math.sqrt(dx*dx + dy*dy) / grid.cell_width

                    # TODO: Проверить, что клетка в радиусе (Задание 1)
                    if distance<=self.radius:
                        # Угол к клетке
                        cell_angle = math.atan2(dy, dx)

                        # Разница углов между направлением робота и направлением на клетку
                        angle_diff = cell_angle - robot.angle

                        # TODO: Нормализовать в диапазон [-π, π]
                        # Подсказка: используйте функцию normalize_angle(angle)
                        angle_diff = normalize_angle(angle_diff)

                        # TODO: Проверить, что клетка в секторе видимости
                        # Используйте max_angle_diff
                        if abs(angle_diff)<=max_angle_diff:
                            cells.add((col, row))

        return cells

    def calculate_center_of_mass(self, grid):
        """
        Вычислить центр масс препятствий в области видения

        Args:
            grid: объект Grid

        Returns:
            tuple: (x, y) координаты центра масс или None если нет препятствий
        """
        # TODO: Проверить наличие препятствий (Задание 3)
        if len(self.obstacle_cells)==0:  # Если нет препятствий - вернуть None
            return None

        # TODO: Инициализировать переменные для суммы координат
        sum_x = 0
        sum_y = 0
        count = len(self.obstacle_cells)  # количество препятствий

        # TODO: Перебрать все препятствия и просуммировать их координаты (в пикселях!)
        # for col, row in self.obstacle_cells:
        for col, row in self.obstacle_cells:
            # Получить центр клетки в пиксельных координатах
            # Можно использовать метод grid.cell_to_pixels(col, row) -> возвращает (x, y)
            cell_x, cell_y = grid.cell_to_pixels(col, row)
            
            sum_x += cell_x
            sum_y += cell_y

        # TODO: Вернуть среднее арифметическое координат
        # (сумма / количество)
        return (sum_x/count, sum_y/count)

    def print_debug_info(self):
        """Вывести отладочную информацию в консоль"""
        print(f"\n=== Область видения ===")
        print(f"Видимые клетки: {len(self.visible_cells)}")
        print(f"Препятствия в зоне: {len(self.obstacle_cells)}")

        if self.obstacle_cells:
            print(f"Клетки с препятствиями: {sorted(self.obstacle_cells)}")
            if self.center_of_mass:
                print(f"Центр масс: ({self.center_of_mass[0]:.1f}, {self.center_of_mass[1]:.1f})")
        else:
            print("Препятствий не обнаружено")
