"""Модуль для робота с непрерывной физикой"""
import math
import pygame

class Robot:
    """Класс робота с линейной и угловой скоростями"""

    def __init__(self, x, y, angle=0.0, max_linear_velocity=10.0, max_angular_velocity=10.0, radius=1.0):
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
        self.x = x
        self.y = y
        self.angle = angle

        self.radius = radius  # в клетках

        # Максимальные скорости
        self.max_linear_velocity = max_linear_velocity    # клеток/сек
        self.max_angular_velocity = max_angular_velocity  # радиан/сек

        self.linear_velocity = 0  # 0.0
        self.angular_velocity = 0  # 0.0

        # Часы
        self.clock = pygame.time.Clock()

        self.count_colisions = 0
        self.time_collisions = []
        self.distance_collisions = []

        self.distance = 0
        self.time_start = pygame.time.get_ticks()
        self.time = 0

        self.finish_flag = False
        self.contr_dist = False
        
    
    def reset_metrics(self):
        """Сбросить все метрики (время, расстояние, столкновения)"""
        self.time_start = pygame.time.get_ticks()
        self.time = 0
        self.distance = 0
        self.count_colisions = 0
        self.time_collisions = []
        self.distance_collisions = []

    
    def update(self, dt=1.0):
        """
        Обновить позицию и угол робота на основе скоростей

        Args:
            dt: временной шаг (по умолчанию 1.0)
        """
        
        self.x += self.linear_velocity * math.cos(self.angle)  * dt

        self.y += self.linear_velocity * math.sin(self.angle) * dt

        self.angle += self.angular_velocity * dt

        self.angle = self.angle % (2 * math.pi)


    def set_velocities(self, linear, angular):
        """
        Установить скорости робота

        Args:
            linear: линейная скорость (клеток/сек)
            angular: угловая скорость (радиан/сек)
        """
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

        detection_radius = 5 * self.radius

        min_col = int(self.x - detection_radius)
        max_col = int(self.x + detection_radius) + 1
        min_row = int(self.y - detection_radius)
        max_row = int(self.y + detection_radius) + 1

        for col in range(min_col, max_col):
            for row in range(min_row, max_row):
                if 0 <= col < grid.cols and 0 <= row < grid.rows:
                    dx = (col + 0.5) - self.x
                    dy = (row + 0.5) - self.y

                    import math
                    distance = math.sqrt(dx*dx + dy*dy)

                    if distance <= detection_radius: 
                        cells.add((col, row))

        return cells


    def get_forward_sector_cells(self, grid):
        """
        Получить клетки в секторе ±60° впереди робота (в зоне обнаружения)

        Args:
            grid: объект Grid

        Returns:
            set клеток (col, row) в переднем секторе
        """
        cells = set()
        detection_radius = 5 * self.radius

        import math
        sector_angle = math.radians(135) 

        min_col = int(self.x - detection_radius)
        max_col = int(self.x + detection_radius) + 1
        min_row = int(self.y - detection_radius)
        max_row = int(self.y + detection_radius) + 1

        for col in range(min_col, max_col):
            for row in range(min_row, max_row):
                if 0 <= col < grid.cols and 0 <= row < grid.rows:
                    dx = (col + 0.5) - self.x
                    dy = (row + 0.5) - self.y
                    distance = math.sqrt(dx*dx + dy*dy)

                    if distance <= detection_radius and distance > 0.1:
                        cell_angle = math.atan2(dy, dx)

                        angle_diff = cell_angle - self.angle

                        while angle_diff > math.pi:
                            angle_diff -= 2 * math.pi
                        while angle_diff < -math.pi:
                            angle_diff += 2 * math.pi

                        if abs(angle_diff) <= sector_angle: 
                            cells.add((col, row))

        return cells


    def get_move_sector_cells(self, grid):
        """
        Получить клетки в секторе ±60° впереди робота (в зоне обнаружения)

        Args:
            grid: объект Grid

        Returns:
            set клеток (col, row) в переднем секторе
        """
        cells = set()
        detection_radius = 2 * self.radius

        import math
        sector_angle = math.radians(45) 

        min_col = int(self.x - detection_radius)
        max_col = int(self.x + detection_radius) + 1
        min_row = int(self.y - detection_radius)
        max_row = int(self.y + detection_radius) + 1

        for col in range(min_col, max_col):
            for row in range(min_row, max_row):
                if 0 <= col < grid.cols and 0 <= row < grid.rows:
                    dx = (col + 0.5) - self.x
                    dy = (row + 0.5) - self.y
                    distance = math.sqrt(dx*dx + dy*dy)

                    if distance <= detection_radius and distance > 0.1:
                        cell_angle = math.atan2(dy, dx)

                        angle_diff = cell_angle - self.angle

                        while angle_diff > math.pi:
                            angle_diff -= 2 * math.pi
                        while angle_diff < -math.pi:
                            angle_diff += 2 * math.pi

                        if abs(angle_diff) <= sector_angle: 
                            cells.add((col, row))

        return cells


    def update_with_collision_check(self, dt, grid):
        """
        Обновить позицию робота с проверкой столкновений

        Проверяем передний сектор (±135°) перед движением вперед.
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
        can_move = True

        if self.linear_velocity >= 0: 
            forward_cells = self.get_move_sector_cells(grid)

            for col, row in forward_cells:
                if grid.is_cell_filled(col, row):
                    can_move = False 
                    break  

        elif self.linear_velocity < 0:
            
            backward_angle = self.angle + math.pi  

            old_angle = self.angle
            self.angle = backward_angle

            backward_cells = self.get_move_sector_cells(grid)

            self.angle = old_angle

            for col, row in backward_cells:
                if grid.is_cell_filled(col, row):
                    can_move = False
                    break

        if can_move:
            old_x = self.x
            old_y = self.y
            self.x += self.linear_velocity * math.cos(self.angle) * dt
            self.y += self.linear_velocity * math.sin(self.angle) * dt
            self.distance += math.sqrt((self.x - old_x)**2 + (self.y - old_y)**2)


    def what_side_sector_cell(self, cell):
        """
        Получить клетки в правом секторе относительно робота (в зоне обнаружения)

        Args:
            grid: объект Grid

        Returns:
            True - правый сектор, False - левый
        """

        col, row = cell

        flag = True

        dx = (col + 0.5) - self.x
        dy = (row + 0.5) - self.y

        cell_angle = math.atan2(dy, dx)
        robo_angle = self.angle

        while robo_angle > math.pi:
            robo_angle -= 2 * math.pi
        while robo_angle < -math.pi:
            robo_angle += 2 * math.pi

        while cell_angle > math.pi:
            cell_angle -= 2 * math.pi
        while cell_angle < -math.pi:
            cell_angle += 2 * math.pi

        if (cell_angle * robo_angle) > 0:

            angle_diff = cell_angle - robo_angle

            if angle_diff < 0:  #слева
                flag = False

            else:   #справа
                flag = True

        else:
            angle_diff = abs(cell_angle) + abs(robo_angle)

            if angle_diff >= math.pi :

                if robo_angle < cell_angle:  #слева
                    return False

                else:   #справа
                    flag = True

            else:

                if robo_angle > cell_angle:  #слева
                    return False

                else:   #справа
                    flag = True

        return flag


    def finish(self):
        ''' 
        Проверяет, дошёл ли робот до финиша
        '''
        
        if (self.x <= 10) and (self.y <= 5):
            self.finish_flag = True


    def distance_control(self, grid, norm = 4):
        ''' 
        Если робот слишком близко к стене, он отодвигается от нее
        '''

        import math

        forward_cells = self.get_forward_sector_cells(grid)

        center_x = 0
        center_y = 0
        n = 0

        cell = (center_x, center_y)

        filled_cells = []

        for col, row in forward_cells:
            if grid.is_cell_filled(col, row):
                center_x += col 
                center_y += row
                n += 1
                filled_cells.append((col, row))

        if n > 0:

            cell = (center_x / n, center_y / n)

            dx = (cell[0] + 0.5) - self.x
            dy = (cell[1] + 0.5) - self.y

            distance = math.sqrt(dx*dx + dy*dy)
            print(f"distance: {distance}")

            if distance < norm :
                self.contr_dist = True
                self.set_velocities(self.linear_velocity, self.max_angular_velocity)
                print(f"ang velocity1: {self.angular_velocity}")
            else:
                self.contr_dist = False

        else:
            self.contr_dist = False
