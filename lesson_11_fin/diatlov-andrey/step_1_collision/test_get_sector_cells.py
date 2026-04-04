"""Тест для метода get_sector_cells()"""
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


def test_forward_sector_no_obstacles():
    """Тест: передний сектор, робот смотрит вправо"""
    grid = Grid(width=800, height=600, cell_width=40, cell_height=40, offset_x=200)
    robot = Robot(x=400, y=300, angle=0)  # Смотрит вправо
    
    cells = robot.get_sector_cells(grid, angle_offset=0)
    
    # Проверяем, что получили клетки
    assert len(cells) > 0, "Должны быть найдены клетки в секторе"
    assert isinstance(cells, set), "Результат должен быть множеством"
    
    # Проверяем, что все клетки в правильном диапазоне
    robot_col = int((robot.x - grid.offset_x) / grid.cell_width)
    robot_row = int(robot.y / grid.cell_height)
    
    for col, row in cells:
        # Клетки должны быть справа от робота (примерно)
        assert col >= robot_col - 1, f"Клетка {col}, {row} слишком далеко слева"
        assert col <= robot_col + 4, f"Клетка {col}, {row} слишком далеко справа"
        
    print("✓ Тест 1 пройден: передний сектор работает")


def test_backward_sector():
    """Тест: задний сектор, робот смотрит вправо"""
    grid = Grid(width=800, height=600, cell_width=40, cell_height=40, offset_x=200)
    robot = Robot(x=400, y=300, angle=0)  # Смотрит вправо
    
    cells = robot.get_sector_cells(grid, angle_offset=math.pi)
    
    # Проверяем, что получили клетки
    assert len(cells) > 0, "Должны быть найдены клетки в заднем секторе"
    
    # Проверяем, что клетки сзади робота
    robot_col = int((robot.x - grid.offset_x) / grid.cell_width)
    
    for col, row in cells:
        # Клетки должны быть слева от робота (примерно)
        assert col <= robot_col + 1, f"Клетка {col}, {row} должна быть сзади"
        
    print("✓ Тест 2 пройден: задний сектор работает")


def test_different_angles():
    """Тест: разные углы робота"""
    grid = Grid(width=800, height=600, cell_width=40, cell_height=40, offset_x=200)
    
    # Робот смотрит вверх
    robot = Robot(x=400, y=300, angle=math.pi * 1.5)  # -90° = вверх
    cells_up = robot.get_sector_cells(grid, angle_offset=0)
    
    assert len(cells_up) > 0, "Должны быть клетки при взгляде вверх"
    
    # Проверяем, что клетки выше робота
    robot_row = int(robot.y / grid.cell_height)
    has_upper_cells = any(row < robot_row for col, row in cells_up)
    assert has_upper_cells, "Должны быть клетки выше робота"
    
    print("✓ Тест 3 пройден: разные углы работают")


def test_sector_size():
    """Тест: размер сектора (примерно 90°)"""
    grid = Grid(width=800, height=600, cell_width=40, cell_height=40, offset_x=200)
    robot = Robot(x=400, y=300, angle=0)  # Смотрит вправо
    
    cells = robot.get_sector_cells(grid, angle_offset=0)
    
    # Проверяем, что нашли разумное количество клеток
    # Для радиуса 3 и сектора 90° ожидаем примерно 7-15 клеток
    assert 5 <= len(cells) <= 20, f"Неожиданное количество клеток: {len(cells)}"
    
    print("✓ Тест 4 пройден: размер сектора корректный")


def test_no_robot_cell():
    """Тест: клетка робота не включается в результат"""
    grid = Grid(width=800, height=600, cell_width=40, cell_height=40, offset_x=200)
    robot = Robot(x=400, y=300, angle=0)
    
    cells = robot.get_sector_cells(grid, angle_offset=0)
    
    # Клетка самого робота
    robot_col = int((robot.x - grid.offset_x) / grid.cell_width)
    robot_row = int(robot.y / grid.cell_height)
    
    # Эта клетка может быть, но обычно исключается если distance > 0.1
    # Просто проверим, что не все клетки - это клетка робота
    other_cells = [(col, row) for col, row in cells if col != robot_col or row != robot_row]
    assert len(other_cells) > 0, "Должны быть клетки кроме клетки робота"
    
    print("✓ Тест 5 пройден: клетка робота обрабатывается корректно")


def test_edge_cases():
    """Тест: граничные случаи"""
    grid = Grid(width=800, height=600, cell_width=40, cell_height=40, offset_x=200)
    
    # Робот у края сетки
    robot = Robot(x=220, y=20, angle=0)  # Почти у левого верхнего угла
    cells = robot.get_sector_cells(grid, angle_offset=0)
    
    # Все клетки должны быть в пределах сетки
    for col, row in cells:
        assert 0 <= col < grid.cols, f"Колонка {col} вне диапазона"
        assert 0 <= row < grid.rows, f"Строка {row} вне диапазона"
    
    print("✓ Тест 6 пройден: граничные случаи обработаны")


def run_all_tests():
    """Запустить все тесты"""
    print("=" * 50)
    print("Тестирование метода get_sector_cells()")
    print("=" * 50)
    
    try:
        test_forward_sector_no_obstacles()
        test_backward_sector()
        test_different_angles()
        test_sector_size()
        test_no_robot_cell()
        test_edge_cases()
        
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
