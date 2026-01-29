"""Класс Brain - контроллер для управления роботом"""
import math
import numpy as np
import random


class Brain:
    """Класс для управления роботом с помощью P-контроллера по углу"""

    def __init__(self, kp=0.5, max_angular_velocity=10.0, linear_velocity=5.0):
        """
        Инициализация Brain

        Args:
            kp: коэффициент пропорциональности P-контроллера
            max_angular_velocity: максимальная угловая скорость (радиан/сек)
            linear_velocity: линейная скорость движения вперед
        """
        self.kp = kp  # Коэффициент пропорциональности
        self.max_angular_velocity = max_angular_velocity  # Максимальная угловая скорость
        self.linear_velocity = linear_velocity  # Линейная скорость
        self.target_angle = 0.0

    def update(self, robot, sight, grid):
        """
        Обновить управление роботом на основе области видения

        Args:
            robot: объект Robot
            sight: объект Sight
            grid: объект Grid (для проверки коллизий)
        """
        # Если робот видит препятствие в области видения, можно вращаться
        if sight.center_of_mass is None:
            # Нет препятствий - движемся вперед прямо
            # Проверяем коллизию перед движением
            safe_velocity = robot.check_collision(grid, self.linear_velocity)
            robot.set_velocities(linear=safe_velocity, angular=0.0)
            return

        # Вычисляем угол до препятствия
        cx, cy = sight.center_of_mass
        dx = cx - robot.x
        dy = cy - robot.y
        
        # Угол к центру масс препятствий
        obstacle_angle = math.atan2(dy, dx)

        # Разница углов между направлением робота и направлением на препятствие
        angle_diff = obstacle_angle - robot.angle
        
        # Нормализуем в диапазон [-π, π]
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi
        
        # TODO ЗАДАНИЕ 4: Проверить, если препятствие ровно по курсу (угол < 5°)
        if abs(angle_diff) < math.radians(5):
            # Выбрать случайное направление поворота (-1 или +1)
            random_direction = random.choice([-1, 1])
            # Установить угловую скорость в случайном направлении
            angular_velocity = random_direction * self.max_angular_velocity
            # Остановить линейное движение и установить скорости
            robot.set_velocities(linear=0.0, angular=angular_velocity)
            # Установить целевой угол для отображения
            self.target_angle = robot.angle + random_direction * (math.pi / 2)
            return
        
        # TODO ЗАДАНИЕ 1: Определить целевой угол в зависимости от стороны
        # Если препятствие слева (angle_diff > 0), цель - повернуть влево на 90° (+π/2)
        # Если препятствие справа (angle_diff < 0), цель - повернуть вправо на 90° (-π/2)
        # Подсказка: np.sign(angle_diff) вернет 1 или -1
        target_angle = np.sign(angle_diff) * (math.pi / 2)
        self.target_angle = target_angle
        
        # TODO ЗАДАНИЕ 2: Вычислить ошибку угла
        # Ошибка = текущая разница углов - целевой угол
        error = angle_diff - target_angle
        
        # TODO ЗАДАНИЕ 3: П-регулятор
        # Вычислить угловую скорость = ошибка * коэффициент
        angular_velocity = error * self.kp
        
        # Ограничить угловую скорость максимумом
        # (используйте max(min(...)) или if/else)
        angular_velocity = max(-self.max_angular_velocity, min(self.max_angular_velocity, angular_velocity))
        
        # Установить скорости робота с проверкой коллизии
        safe_velocity = robot.check_collision(grid, self.linear_velocity)
        robot.set_velocities(linear=safe_velocity, angular=angular_velocity)
