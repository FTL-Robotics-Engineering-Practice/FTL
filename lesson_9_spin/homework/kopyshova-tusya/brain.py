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

            print(f" препятствия: {filled_cells}, центр масс: {cell[0]}, {cell[1]}")

        
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
                print(self.robot.get_forward_sector_cells(self.grid))
                print(f"Номер столкновения: {robot.count_colisions-1}, Текущее время: {round(robot.time_collisions[-1]/1000, 1)}, Пройденное расстояние: {round(robot.distance_collisions[-1], 1)}, Средний период столкновения: {round(robot.time_collisions[-1] / (robot.count_colisions) / 1000, 1)}, Угловая скорость: {angular_velocity}, положение препятствия: {self.side}, roboangle : {self.robot.angle}")
            self.was_obstacle_ahead = True
            self.update_angular_speed
        else:
            self.was_obstacle_ahead = False

        self.robot.set_velocities(linear_velocity, angular_velocity)
        self.robot.update_with_collision_check(dt, self.grid)