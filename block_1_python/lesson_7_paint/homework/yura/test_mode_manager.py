"""Тест ModeManager"""
from mode_manager import ModeManager, Mode

# Создаём менеджер режимов (по умолчанию MAP_EDIT)
mode_manager = ModeManager()

print("=== ТЕСТ 1: Начальный режим ===")
print(f"Текущий режим: {mode_manager.get_mode_name()}")
print(f"Это режим карты? {mode_manager.is_map_mode()}")
print(f"Это режим робота? {mode_manager.is_robot_mode()}")

print("\n=== ТЕСТ 2: Переключение режима ===")
mode_manager.toggle_mode()
print(f"Текущий режим: {mode_manager.get_mode_name()}")
print(f"Это режим карты? {mode_manager.is_map_mode()}")
print(f"Это режим робота? {mode_manager.is_robot_mode()}")

print("\n=== ТЕСТ 3: Переключение обратно ===")
mode_manager.toggle_mode()
print(f"Текущий режим: {mode_manager.get_mode_name()}")

print("\n=== ТЕСТ 4: Несколько переключений ===")
for i in range(4):
    mode_manager.toggle_mode()

print("\n✅ Все тесты пройдены!")
