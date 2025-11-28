import math
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
        self.elapsed_time = 0.0
        self.collision_times = []
        self.collision_count = 0
        self.path_length = 0.0
        self._obstacle_active = False
        self._last_position = self.robot.get_position()

    def _has_obstacle_ahead(self, current_time):
        """Возвращает True, если в переднем секторе обнаружено препятствие."""
        forward_cells = self.robot.get_forward_sector_cells(self.grid)
        obstacle_found = False
        for col, row in forward_cells:
            if self.grid.is_cell_filled(col, row):
                obstacle_found = True
                break

        if obstacle_found and not self._obstacle_active:
            self.collision_times.append(current_time)
            self.collision_count += 1
            print(
                f"Столкновение #{self.collision_count}: "
                f"время столкновения = {current_time:.3f} с, "
                f"длина пути = {self.path_length:.2f} клеток,"
                f"частота столкновений = {self.collision_count / self.elapsed_time:.2f} столкновений в секунду"
            )
        if not obstacle_found and self._obstacle_active:
            self._last_position = self.robot.get_position()

        self._obstacle_active = obstacle_found
        return obstacle_found

    def update(self, dt):
        """Обновляет состояние робота за временной шаг `dt`."""
        previous_position = self.robot.get_position()

        self.elapsed_time += dt
        obstacle_ahead = self._has_obstacle_ahead(self.elapsed_time)
        if obstacle_ahead:
            linear_velocity = 0.0
            angular_velocity = min(self.angular_velocity, self.robot.max_angular_velocity)
        else:
            linear_velocity = min(self.linear_velocity, self.robot.max_linear_velocity)
            angular_velocity = 0.0

        self.robot.set_velocities(linear_velocity, angular_velocity)
        self.robot.update_with_collision_check(dt, self.grid)

        new_x, new_y = self.robot.get_position()
        dx = new_x - previous_position[0]
        dy = new_y - previous_position[1]
        step_distance = math.hypot(dx, dy)
        self.path_length += step_distance
        self._last_position = (new_x, new_y)

    