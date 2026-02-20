from robot import Robot
from grid import Grid


class Brain:
    def __init__(self, robot, grid, linear_velocity=8.0, angular_velocity=0.0):
        """

        Args:
            robot: управляемый объект `Robot`.
            grid: карта препятствий `Grid`.
            linear_velocity: линейная скорость (клеток/сек) при свободном пути.
            angular_velocity: угловая скорость (рад/сек) при повороте по часовой стрелке.
        """
        self.robot = robot
        self.grid = grid
        self.linear_velocity = linear_velocity
        self.angular_velocity = angular_velocity
        self.was_obstacle_ahead = False  # Флаг для отслеживания предыдущего состояния
        self.side = 'right'
        self.old_vel = linear_velocity

        self.alpha = 0


    def _has_obstacle_ahead(self):
        """Возвращает True, если в переднем секторе обнаружено препятствие"""

        forward_cells = self.robot.get_forward_sector_cells(self.grid)

        for col, row in forward_cells:
            if self.grid.is_cell_filled(col, row):

                return True

        return False


    def update_angular_speed(self, robot):
        """Обновляет угловую скорость, чтобы робот катался против часовой стрелки"""

        forward_cells = self.robot.get_forward_sector_cells(self.grid)

        center_x = 0
        center_y = 0
        n = 0

        cell = (center_x, center_y)

        filled_cells = []

        for col, row in forward_cells:
            if self.grid.is_cell_filled(col, row):
                center_x += col 
                center_y += row
                n += 1
                filled_cells.append((col, row))

        if n > 0:
            cell = (center_x / n, center_y / n)

            if robot.what_side_sector_cell(cell):
                self.angular_velocity -= 0.0001
                self.side = 'right'
            else:
                self.angular_velocity += 0.0001
                self.side = 'left'


        
    def update(self, dt, robot):
        """Обновляет состояние робота за временной шаг dt"""
        has_obstacle = self._has_obstacle_ahead()
        
        self.update_angular_speed(robot)
        angular_velocity = min(self.angular_velocity, self.robot.max_angular_velocity)
        linear_velocity = min(self.linear_velocity, self.robot.max_linear_velocity)
        
        if has_obstacle:
            # Регистрируем столкновение только при переходе от "нет препятствия" к "есть препятствие"
            if not self.was_obstacle_ahead:
                robot.count_colisions += 1
                robot.time_collisions.append(robot.time)
                robot.distance_collisions.append(robot.distance)
            self.was_obstacle_ahead = True
            self.update_angular_speed
        else:
            self.was_obstacle_ahead = False

        self.robot.set_velocities(linear_velocity, angular_velocity)
        self.robot.update_with_collision_check(dt, self.grid)

    def p_regulator(self, robot, norm = 4):
        """Обновляет угловую скорость на основе принципа п-регулятора"""

        import math

        k = 5.5

        forward_cells = self.robot.get_forward_sector_cells(self.grid)

        center_x = 0
        center_y = 0
        n = 0
        min_dist = 1000000

        cell = (center_x, center_y)

        filled_cells = []

        for col, row in forward_cells:
            if self.grid.is_cell_filled(col, row):
                center_x += col 
                center_y += row
                n += 1
                filled_cells.append((col, row))

                dist = math.sqrt((col - robot.x)**2 + (row - robot.y)**2)
                if dist < min_dist:
                    min_dist = dist

        if n > 0:

            cell = (center_x / n, center_y / n)



            dx = (cell[0] + 0.5) - robot.x
            dy = (cell[1] + 0.5) - robot.y

            lab_cell_angle = math.atan2(dy, dx)

            robo_angle = robot.angle

            while robo_angle > math.pi: 
                robo_angle -= 2 * math.pi
            while robo_angle < -math.pi:
                robo_angle += 2 * math.pi

            while lab_cell_angle > math.pi:
                lab_cell_angle -= 2 * math.pi
            while lab_cell_angle < -math.pi:
                lab_cell_angle += 2 * math.pi

            eps = 0.01

            if (abs(robo_angle - math.pi) < eps):
                robo_angle = math.pi

            robo_cell_angle = lab_cell_angle - robo_angle

            while robo_cell_angle > math.pi:
                robo_cell_angle -= 2 * math.pi
            while robo_cell_angle < -math.pi:
                robo_cell_angle += 2 * math.pi

            self.alpha = round(robo_cell_angle, 5)

            if robot.what_side_sector_cell(cell):
                n = 0
            else:
                n = 1
            dist_coeff = 0.13
            if min_dist <= norm:
                self.angular_velocity = -robot.max_angular_velocity* dist_coeff* pow(-1, n)
            else:
                self.angular_velocity = -k * ((math.pi / 2) - (self.alpha*pow(-1, n))) * pow(-1, n)


        else:
            self.alpha = math.pi/2
            self.angular_velocity = 0


    def labirint(self, dt, robot):
        
        """Обновляет состояние робота за временной шаг dt при прохождении лабиринта"""
        
        self.p_regulator(robot)

        self.linear_velocity = self.old_vel

        angular_velocity = min(self.angular_velocity, self.robot.max_angular_velocity)
        linear_velocity = min(self.linear_velocity, self.robot.max_linear_velocity)

        self.robot.set_velocities(linear_velocity, angular_velocity)
        self.robot.update_with_collision_check(dt, self.grid)