"""Класс робота с базовой физикой"""
import math


class Robot:
    """Простой робот с линейной и угловой скоростями"""

    def __init__(self, x, y, angle=0.0):
        """
        Инициализация робота

        Args:
            x: начальная позиция X (в пикселях)
            y: начальная позиция Y (в пикселях)
            angle: начальный угол в радианах (0 = вправо)
        """
        self.x = x
        self.y = y
        self.angle = angle

        # Скорости (устанавливаются через управление)
        self.linear_velocity = 0.0  # пикселей/сек
        self.angular_velocity = 0.0  # радиан/сек

    @staticmethod
    def normalize_angle(angle):
        """
        Нормализовать угол в диапазон [-π, π]
        
        Args:
            angle: угол в радианах
            
        Returns:
            float: нормализованный угол
        """
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

    def update(self, dt):
        """
        Обновить позицию робота

        Args:
            dt: временной шаг в секундах
        """
        # Обновляем позицию на основе линейной скорости и угла
        self.x += self.linear_velocity * math.cos(self.angle) * dt
        self.y += self.linear_velocity * math.sin(self.angle) * dt

        # Обновляем угол
        self.angle += self.angular_velocity * dt

        # Нормализуем угол в диапазон [0, 2π]
        self.angle = self.angle % (2 * math.pi)

    def set_velocities(self, linear, angular):
        """
        Установить скорости робота

        Args:
            linear: линейная скорость (пикселей/сек)
            angular: угловая скорость (радиан/сек)
        """
        self.linear_velocity = linear
        self.angular_velocity = angular

    def get_sector_cells(self, grid, angle_offset=0):
        """
        Получить клетки в секторе ±45° от направления робота

        Args:
            grid: объект Grid
            angle_offset: смещение угла (0 для переднего, π для заднего)

        Returns:
            set: множество клеток (col, row) в секторе
        """
        cells = set()
        radius = 3  # радиус зоны обнаружения
        sector_angle = math.radians(45)  # ±45° = 90° сектор

        # TODO: Вычислить направление центра сектора
        # Это угол робота + смещение (angle_offset)
        check_angle = self.angle + angle_offset

        # Перебираем все клетки в квадрате вокруг робота
        # Учитываем offset_x для колонок
        min_col = int((self.x - grid.offset_x) / grid.cell_width - radius)
        max_col = int((self.x - grid.offset_x) / grid.cell_width + radius) + 1
        min_row = int(self.y / grid.cell_height - radius)
        max_row = int(self.y / grid.cell_height + radius) + 1

        for col in range(min_col, max_col):
            for row in range(min_row, max_row):
                if 0 <= col < grid.cols and 0 <= row < grid.rows:
                    # Центр клетки (с учетом offset_x)
                    cell_x = (col + 0.5) * grid.cell_width + grid.offset_x
                    cell_y = (row + 0.5) * grid.cell_height

                    # Вектор от робота до клетки
                    dx = cell_x - self.x
                    dy = cell_y - self.y
                    distance = math.sqrt(dx*dx + dy*dy) / grid.cell_width

                    # TODO: Проверить, что клетка в радиусе
                    if distance<=radius:
                        # Угол к клетке (используйте math.atan2(dy, dx))
                        cell_angle = math.atan2(dy, dx)

                        # Разница углов
                        angle_diff = cell_angle - check_angle

                        # TODO: Нормализовать angle_diff в диапазон [-π, π]
                        # Подсказка: используйте Robot.normalize_angle(angle_diff)
                        angle_diff = Robot.normalize_angle(angle_diff)

                        # TODO: Проверить, что клетка в секторе ±45°
                        # (модуль разницы углов должен быть меньше sector_angle)
                        if abs(angle_diff)<=sector_angle:
                            cells.add((col, row))

        return cells

    def check_collision(self, grid, desired_linear_velocity):
        """
        Проверить, можно ли двигаться с заданной скоростью

        Args:
            grid: объект Grid
            desired_linear_velocity: желаемая линейная скорость

        Returns:
            float: разрешенная линейная скорость (0 если коллизия)
        """
        # TODO: Проверить особый случай (скорость 0)
        if desired_linear_velocity==0:
            return 0

        # TODO: Определить, какой сектор проверять (передний или задний)
        # в зависимости от знака скорости
        if desired_linear_velocity>0:
            # Движение вперед - проверяем передний сектор (offset = 0)
            sector_cells = self.get_sector_cells(grid, 0)
        else:
            # Движение назад - проверяем задний сектор (offset = math.pi)
            sector_cells = self.get_sector_cells(grid, math.pi)

        # Проверяем, есть ли препятствия в секторе
        for col, row in sector_cells:
            if grid.is_cell_filled(col, row):  # проверить, заполнена ли клетка (grid.is_cell_filled)
                # Нашли препятствие - запрещаем движение
                return 0
            

        # Препятствий нет - разрешаем движение
        return desired_linear_velocity
