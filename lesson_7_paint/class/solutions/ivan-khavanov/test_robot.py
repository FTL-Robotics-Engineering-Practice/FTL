"""Тест класса Robot"""
from robot import Robot
import math

# Создаём робота в позиции (10, 10), смотрящего вправо (угол 0)
robot = Robot(x=10.0, y=10.0, angle=0.0, radius=1.0)

print("=== ТЕСТ 1: Начальное состояние ===")
print(f"Позиция: {robot.get_position()}")
print(f"Угол: {robot.get_angle():.2f} радиан")
print(f"Линейная скорость: {robot.linear_velocity}")
print(f"Угловая скорость: {robot.angular_velocity}")

print("\n=== ТЕСТ 2: Установка скорости и движение вперёд ===")
# Устанавливаем линейную скорость 5 клеток/сек, без поворота
robot.set_velocities(linear=5.0, angular=0.0)
print(f"Установлены скорости: linear={robot.linear_velocity}, angular={robot.angular_velocity}")

# Симулируем 5 кадров с dt=0.1 секунды
print("\nДвижение вперёд (5 кадров по 0.1 сек):")
for i in range(5):
    robot.update(dt=0.1)
    x, y = robot.get_position()
    print(f"  Кадр {i+1}: x={x:.2f}, y={y:.2f}")

print(f"\nИтоговая позиция: {robot.get_position()}")
print(f"Ожидалось: x ≈ 12.5, y ≈ 10.0 (прошёл 2.5 клетки вправо)")

print("\n=== ТЕСТ 3: Поворот ===")
# Останавливаем движение, включаем поворот
robot.set_velocities(linear=0.0, angular=math.pi / 2)  # 90° за секунду
print(f"Установлена угловая скорость: {robot.angular_velocity:.2f} рад/сек")

# Поворачиваем 1 секунду (должен повернуться на 90°)
robot.update(dt=1.0)
angle_degrees = math.degrees(robot.get_angle())
print(f"Угол после поворота: {angle_degrees:.2f}° (ожидалось ≈90°)")

print("\n=== ТЕСТ 4: Движение вверх ===")
# Теперь робот смотрит вверх (90°), едем вперёд
robot.set_velocities(linear=5.0, angular=0.0)
robot.update(dt=0.5)  # 0.5 секунды
x, y = robot.get_position()
print(f"Позиция после движения вверх: x={x:.2f}, y={y:.2f}")
print(f"Ожидалось: x ≈ 12.5, y ≈ 12.5 (прошёл 2.5 клетки вверх)")

print("\n=== ТЕСТ 5: Ограничение границами ===")
# Перемещаем робота за границы
robot.x = 100.0
robot.y = -5.0
print(f"До ограничения: {robot.get_position()}")

# Ограничиваем карту размером 75×50
robot.clamp_position(0, 75, 0, 50)
print(f"После clamp(0, 75, 0, 50): {robot.get_position()}")
print(f"Ожидалось: x=75, y=0")

print("\n✅ Все тесты пройдены!")

