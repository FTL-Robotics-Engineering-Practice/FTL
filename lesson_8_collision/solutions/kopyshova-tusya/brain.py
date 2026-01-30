from robot import Robot
from grid import Grid


class Brain:
    def __init__(self, robot, grid, linear_velocity=5.0, angular_velocity=1.5):
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

    def _has_obstacle_ahead(self):
        """Возвращает True, если в переднем секторе обнаружено препятствие."""
        forward_cells = self.robot.get_forward_sector_cells(self.grid)
        for col, row in forward_cells:
            if self.grid.is_cell_filled(col, row):
                return True
        return False

    def update(self, dt, robot):
        """Обновляет состояние робота за временной шаг dt"""
        has_obstacle = self._has_obstacle_ahead()
        
        if has_obstacle:
            linear_velocity = 0.0
            angular_velocity = min(self.angular_velocity, self.robot.max_angular_velocity)
            # Регистрируем столкновение только при переходе от "нет препятствия" к "есть препятствие"
            if not self.was_obstacle_ahead:
                robot.count_colisions += 1
                robot.time_collisions.append(robot.time)
                robot.distance_collisions.append(robot.distance)
                print(f"Номер столкновения: {robot.count_colisions-1}, Текущее время: {round(robot.time_collisions[-1]/1000, 1)}, Пройденное расстояние: {round(robot.distance_collisions[-1], 1)}, Средний период столкновения: {round(robot.time_collisions[-1] / (robot.count_colisions) / 1000, 1)}")
            self.was_obstacle_ahead = True
        else:
            linear_velocity = min(self.linear_velocity, self.robot.max_linear_velocity)
            angular_velocity = 0.0
            self.was_obstacle_ahead = False

        self.robot.set_velocities(linear_velocity, angular_velocity)
        self.robot.update_with_collision_check(dt, self.grid)