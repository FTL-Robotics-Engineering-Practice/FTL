from robot import Robot
from grid import Grid
import math
import numpy as np

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
        self.angle = 0


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
            d_omega = 0.0005
            k = 2
            dx = cell[0] - robot.x
            dy = cell[1] - robot.y
            
            angle = math.atan2(dy, dx) - robot.angle
            angle = (angle + math.pi)%(2*math.pi)-math.pi
            print("Arctg:", round(math.atan2(dy, dx), 3), round(math.atan2(dy, dx)*180/math.pi, 3))
            print("Robot:", round(robot.angle, 3), round(robot.angle*180/math.pi,3))
            self.angle=angle
            print("Угол:", round(angle, 3), round(angle*180/math.pi, 3))
            if angle > 0:
                print("Дополнение угла:", round(90-angle*180/math.pi, 2))

            else:
                print("Дополнение угла:", round(angle*180/math.pi+90, 2))

            print(f"Препятствия: {filled_cells}, центр масс: {cell[0]-robot.x}, {cell[1]-robot.y}")
            if abs(angle*180/math.pi) <= 10:
                rand_sign = 2 * np.random.randint(2) - 1
                print("Rand_sign:", rand_sign)
                self.angular_velocity = self.robot.max_angular_velocity * rand_sign
            else:
                if angle<=-math.pi/2:
                    sign = 1
                elif angle <= 0:
                    sign = -1
                elif angle <=math.pi/2:
                    sign = 1
                else:
                    sign = -1
                print("Sign:", sign)
                adj = abs(abs(angle) - math.pi/2)
                print("Adj:", adj*180/math.pi)
                self.angular_velocity = -k*adj*sign
            
        else:
            robot.has_collision = 0
            self.angular_velocity = 0.0

        print("Angular_velocity:", self.angular_velocity)

    def update(self, dt, robot):
        """Обновляет состояние робота за временной шаг dt"""
        has_obstacle = self._has_obstacle_ahead()
        print("Есть ли столкновение:", self._has_obstacle_ahead())
        self.update_angular_speed(robot)
        angular_velocity = min(self.angular_velocity, self.robot.max_angular_velocity) #* int((-1)**robot.has_collision)
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