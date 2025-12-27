"""Модуль для робота с непрерывной физикой"""
import math


class Robot:
    """Класс робота с линейной и угловой скоростями"""

    def __init__(self, x, y, angle=0.0, max_linear_velocity=10.0, max_angular_velocity=5.0, radius=1.0):
        """
        Инициализация робота

        Args:
            x: начальная позиция X (в клетках, float)
            y: начальная позиция Y (в клетках, float)
            angle: начальный угол в радианах (0 = вправо)
            max_linear_velocity: максимальная линейная скорость (клеток/сек)
            max_angular_velocity: максимальная угловая скорость (радиан/сек)
            radius: радиус робота (в клетках)
        """
        # TODO: Сохраните начальную позицию
        self.x = x
        self.y = y
        self.angle = angle

        # TODO: Сохраните радиус робота (для отрисовки и столкновений)
        self.radius = radius  # в клетках

        # Максимальные скорости
        self.max_linear_velocity = max_linear_velocity    # клеток/сек
        self.max_angular_velocity = max_angular_velocity  # радиан/сек

        # TODO: Текущие скорости (изначально робот стоит на месте)
        self.linear_velocity = 0  # 0.0
        self.angular_velocity = 0  # 0.0

    def update(self, dt=1.0):
        """
        Обновить позицию и угол робота на основе скоростей

        Args:
            dt: временной шаг (по умолчанию 1.0)
        """
        # TODO: Обновите позицию X
        # Формула: x += linear_velocity * cos(angle) * dt
        # Подсказка: используйте math.cos()
        self.x += self.linear_velocity * math.cos(self.angle)  * dt

        # TODO: Обновите позицию Y
        # Формула: y += linear_velocity * sin(angle) * dt
        self.y += self.linear_velocity * math.sin(self.angle) * dt

        # TODO: Обновите угол
        # Формула: angle += angular_velocity * dt
        self.angle += self.angular_velocity * dt

        # Нормализуем угол в диапазон [0, 2π]
        # Это нужно, чтобы угол не рос бесконечно
        self.angle = self.angle % (2 * math.pi)

    def set_velocities(self, linear, angular):
        """
        Установить скорости робота

        Args:
            linear: линейная скорость (клеток/сек)
            angular: угловая скорость (радиан/сек)
        """
        # TODO: Сохраните скорости
        self.linear_velocity = linear
        self.angular_velocity = angular

    def clamp_position(self, min_x, max_x, min_y, max_y):
        """
        Ограничить позицию робота границами карты

        Args:
            min_x, max_x: границы по X
            min_y, max_y: границы по Y
        """

        self.x = max(min_x, min(max_x, self.x))

        self.y = max(min_y, min(max_y, self.y))

    def get_position(self):
        """Получить текущую позицию робота (x, y)"""
        return (self.x, self.y)

    def get_angle(self):
        """Получить текущий угол робота в радианах"""
        return self.angle

    def get_detection_zone_cells(self, grid):
        """
        Получить все клетки в зоне обнаружения (радиус 2*radius от робота)

        Args:
            grid: объект Grid

        Returns:
            set клеток (col, row) в зоне обнаружения
        """
        cells = set()

        detection_radius = 2 * self.radius

        # Мы проверяем квадрат вокруг робота, а потом фильтруем по расстоянию
        min_col = int(self.x - detection_radius)
        max_col = int(self.x + detection_radius) + 1
        min_row = int(self.y - detection_radius)
        max_row = int(self.y + detection_radius) + 1

        # Проверяем каждую клетку в квадрате
        for col in range(min_col, max_col):
            for row in range(min_row, max_row):
                if 0 <= col < grid.cols and 0 <= row < grid.rows:
                    # Вычисляем расстояние от центра робота до центра клетки
                    # Центр клетки: (col + 0.5, row + 0.5)
                    dx = (col + 0.5) - self.x
                    dy = (row + 0.5) - self.y

                    # distance = √(dx² + dy²)
                    import math
                    distance = math.sqrt(dx*dx + dy*dy)

                    if distance <= detection_radius:  # detection_radius
                        cells.add((col, row))

        return cells

    def get_forward_sector_cells(self, grid):
        """
        Получить клетки в секторе ±45° впереди робота (в зоне обнаружения)

        Args:
            grid: объект Grid

        Returns:
            set клеток (col, row) в переднем секторе
        """
        cells = set()
        detection_radius = 2 * self.radius

        # 45° в радианах = π/4 ≈ 0.785
        import math
        sector_angle = math.radians(45) 

        # Вычисляем границы квадрата для проверки
        min_col = int(self.x - detection_radius)
        max_col = int(self.x + detection_radius) + 1
        min_row = int(self.y - detection_radius)
        max_row = int(self.y + detection_radius) + 1

        # Проверяем каждую клетку в квадрате
        for col in range(min_col, max_col):
            for row in range(min_row, max_row):
                # Проверяем границы сетки
                if 0 <= col < grid.cols and 0 <= row < grid.rows:
                    # Вектор от робота до клетки
                    dx = (col + 0.5) - self.x
                    dy = (row + 0.5) - self.y
                    distance = math.sqrt(dx*dx + dy*dy)

                    # Клетка должна быть в радиусе обнаружения
                    if distance <= detection_radius and distance > 0.1:
                        # atan2(dy, dx) возвращает угол в радианах
                        cell_angle = math.atan2(dy, dx)

                        angle_diff = cell_angle - self.angle

                        # Нормализуем угол в диапазон [-π, π]
                        while angle_diff > math.pi:
                            angle_diff -= 2 * math.pi
                        while angle_diff < -math.pi:
                            angle_diff += 2 * math.pi

                        if abs(angle_diff) <= sector_angle:  # sector_angle
                            cells.add((col, row))

        return cells

    def update_with_collision_check(self, dt, grid):
        """
        Обновить позицию робота с проверкой столкновений

        Проверяем передний сектор (±45°) перед движением вперед.
        Если в секторе есть препятствие - запрещаем движение.
        Назад можно двигаться всегда (или с проверкой заднего сектора).
        Поворот всегда разрешен.

        Args:
            dt: временной шаг
            grid: объект Grid для проверки препятствий
        """
        import math
        self.angle += self.angular_velocity * dt
        self.angle = self.angle % (2 * math.pi)

        if abs(self.linear_velocity) > 0.01:  # Если едем
            can_move = True  # По умолчанию разрешаем движение

            # Если двигаемся вперед - проверяем передний сектор
            if self.linear_velocity > 0:  # 0 (вперёд = положительная скорость)
                # Получаем клетки переднего сектора
                forward_cells = self.get_forward_sector_cells(grid)

                # Проверяем, есть ли препятствия в секторе
                for col, row in forward_cells:
                    if grid.is_cell_filled(col, row):
                        can_move = False 
                        break  # Нашли препятствие - хватит проверять

            # БОНУС - Если двигаемся назад - проверяем задний сектор
            elif self.linear_velocity < 0:
                # Создаём временного робота, повёрнутого на 180°
                
                backward_angle = self.angle + math.pi  # +180°

                # Сохраняем текущий угол
                old_angle = self.angle
                self.angle = backward_angle

                # Получаем сектор (теперь это задний сектор)
                backward_cells = self.get_forward_sector_cells(grid)

                # Восстанавливаем угол
                self.angle = old_angle

                # Проверяем препятствия
                for col, row in backward_cells:
                    if grid.is_cell_filled(col, row):
                        can_move = False
                        break


            # Если можем двигаться - обновляем позицию
            if can_move:
                self.x += self.linear_velocity * math.cos(self.angle) * dt
                self.y += self.linear_velocity * math.sin(self.angle) * dt
            # Если can_move == False - робот просто стоит на месте
