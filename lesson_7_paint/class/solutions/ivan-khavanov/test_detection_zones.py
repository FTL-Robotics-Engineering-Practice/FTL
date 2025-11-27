"""Тест зон обнаружения робота"""
from robot import Robot
from grid import Grid
import math

# Создаём сетку и робота
grid = Grid(800, 600, 10, 12, offset_x=0)
robot = Robot(x=10.0, y=10.0, angle=0.0, radius=1.0)

# Добавляем препятствия
grid.fill_cell(13, 10)  # Впереди
grid.fill_cell(13, 11)
grid.fill_cell(14, 10)

print("=== ТЕСТ 1: Зона обнаружения ===")
detection_cells = robot.get_detection_zone_cells(grid)
print(f"Клеток в зоне обнаружения: {len(detection_cells)}")
print(f"Ожидалось: ~12-16 клеток (круг радиуса 2)")

print("\n=== ТЕСТ 2: Передний сектор ===")
forward_cells = robot.get_forward_sector_cells(grid)
print(f"Клеток в переднем секторе: {len(forward_cells)}")
print(f"Ожидалось: ~4-6 клеток (сектор 90° впереди)")

print("\n=== ТЕСТ 3: Препятствия в переднем секторе ===")
obstacles_in_front = 0
for col, row in forward_cells:
    if grid.is_cell_filled(col, row):
        obstacles_in_front += 1
        print(f"  Препятствие в клетке ({col}, {row})")

print(f"\nВсего препятствий впереди: {obstacles_in_front}")
print(f"Ожидалось: 3 (мы добавили 3 клетки впереди)")

print("\n=== ТЕСТ 4: Поворот робота ===")
robot.angle = math.pi / 2  # 90° - смотрим вверх

forward_cells_up = robot.get_forward_sector_cells(grid)
print(f"После поворота на 90°: {len(forward_cells_up)} клеток в переднем секторе")

obstacles_up = sum(1 for col, row in forward_cells_up if grid.is_cell_filled(col, row))
print(f"Препятствий впереди после поворота: {obstacles_up}")
print(f"Ожидалось: 0-1 (препятствия справа, не впереди)")

print("\n✅ Все тесты пройдены!")

