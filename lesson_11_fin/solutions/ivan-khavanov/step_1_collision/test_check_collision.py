"""Тест для метода check_collision()"""
import sys
import math
from pathlib import Path
import io

# Настройка кодировки для Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent / "code"))

from robot import Robot
from grid import Grid


def test_no_movement():
    """Тест: нулевая скорость должна вернуть 0"""
    grid = Grid(width=800, height=600, cell_width=40, cell_height=40, offset_x=200)
    robot = Robot(x=400, y=300, angle=0)
    
    result = robot.check_collision(grid, desired_linear_velocity=0)
    
    assert result == 0, "При нулевой скорости должен вернуться 0"
    print("✓ Тест 1 пройден: нулевая скорость работает")


def test_forward_no_obstacles():
    """Тест: движение вперед без препятствий"""
    grid = Grid(width=800, height=600, cell_width=40, cell_height=40, offset_x=200)
    robot = Robot(x=400, y=300, angle=0)
    
    # Очищаем сетку
    grid.clear_all()
    
    result = robot.check_collision(grid, desired_linear_velocity=100)
    
    assert result == 100, "Без препятствий должна вернуться желаемая скорость"
    print("✓ Тест 2 пройден: движение вперед без препятствий")


def test_forward_with_obstacle():
    """Тест: движение вперед с препятствием"""
    grid = Grid(width=800, height=600, cell_width=40, cell_height=40, offset_x=200)
    robot = Robot(x=400, y=300, angle=0)  # Смотрит вправо
    
    # Очищаем сетку
    grid.clear_all()
    
    # Добавляем препятствие справа от робота
    robot_col = int((robot.x - grid.offset_x) / grid.cell_width)
    robot_row = int(robot.y / grid.cell_height)
    grid.fill_cell(robot_col + 2, robot_row)  # Препятствие впереди
    
    result = robot.check_collision(grid, desired_linear_velocity=100)
    
    assert result == 0, "При препятствии впереди должен вернуться 0"
    print("✓ Тест 3 пройден: обнаружение препятствия спереди")


def test_backward_no_obstacles():
    """Тест: движение назад без препятствий"""
    grid = Grid(width=800, height=600, cell_width=40, cell_height=40, offset_x=200)
    robot = Robot(x=400, y=300, angle=0)
    
    # Очищаем сетку
    grid.clear_all()
    
    result = robot.check_collision(grid, desired_linear_velocity=-50)
    
    assert result == -50, "Движение назад без препятствий должно быть разрешено"
    print("✓ Тест 4 пройден: движение назад без препятствий")


def test_backward_with_obstacle():
    """Тест: движение назад с препятствием"""
    grid = Grid(width=800, height=600, cell_width=40, cell_height=40, offset_x=200)
    robot = Robot(x=400, y=300, angle=0)  # Смотрит вправо
    
    # Очищаем сетку
    grid.clear_all()
    
    # Добавляем препятствие слева от робота (сзади)
    robot_col = int((robot.x - grid.offset_x) / grid.cell_width)
    robot_row = int(robot.y / grid.cell_height)
    grid.fill_cell(robot_col - 2, robot_row)  # Препятствие сзади
    
    result = robot.check_collision(grid, desired_linear_velocity=-50)
    
    assert result == 0, "При препятствии сзади движение назад должно быть запрещено"
    print("✓ Тест 5 пройден: обнаружение препятствия сзади")


def test_obstacle_on_side():
    """Тест: препятствие сбоку не должно мешать"""
    grid = Grid(width=800, height=600, cell_width=40, cell_height=40, offset_x=200)
    robot = Robot(x=400, y=300, angle=0)  # Смотрит вправо
    
    # Очищаем сетку
    grid.clear_all()
    
    # Добавляем препятствие сверху (вне сектора ±45°)
    robot_col = int((robot.x - grid.offset_x) / grid.cell_width)
    robot_row = int(robot.y / grid.cell_height)
    grid.fill_cell(robot_col, robot_row - 3)  # Препятствие сверху, далеко
    
    result = robot.check_collision(grid, desired_linear_velocity=100)
    
    # Препятствие сбоку или далеко не должно мешать
    # (может быть 0 или 100 в зависимости от того, попадает ли в сектор)
    # Но для клетки прямо сверху и далеко - должно быть 100
    assert result == 100, "Препятствие вне сектора не должно мешать"
    print("✓ Тест 6 пройден: препятствие сбоку не мешает")


def test_different_angles():
    """Тест: проверка с разными углами"""
    grid = Grid(width=800, height=600, cell_width=40, cell_height=40, offset_x=200)
    
    # Робот смотрит вверх
    robot = Robot(x=400, y=300, angle=math.pi * 1.5)  # Вверх
    grid.clear_all()
    
    # Без препятствий
    result = robot.check_collision(grid, desired_linear_velocity=100)
    assert result == 100, "Движение вверх без препятствий"
    
    # Добавляем препятствие сверху
    robot_col = int((robot.x - grid.offset_x) / grid.cell_width)
    robot_row = int(robot.y / grid.cell_height)
    grid.fill_cell(robot_col, robot_row - 2)  # Сверху
    
    result = robot.check_collision(grid, desired_linear_velocity=100)
    assert result == 0, "Препятствие сверху должно остановить робота"
    
    print("✓ Тест 7 пройден: разные углы работают")


def run_all_tests():
    """Запустить все тесты"""
    print("=" * 50)
    print("Тестирование метода check_collision()")
    print("=" * 50)
    
    try:
        test_no_movement()
        test_forward_no_obstacles()
        test_forward_with_obstacle()
        test_backward_no_obstacles()
        test_backward_with_obstacle()
        test_obstacle_on_side()
        test_different_angles()
        
        print("=" * 50)
        print("✓ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("=" * 50)
        return True
        
    except AssertionError as e:
        print("=" * 50)
        print(f"✗ ТЕСТ НЕ ПРОЙДЕН: {e}")
        print("=" * 50)
        return False
    except Exception as e:
        print("=" * 50)
        print(f"✗ ОШИБКА ПРИ ВЫПОЛНЕНИИ ТЕСТА: {e}")
        print("=" * 50)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
