"""Модуль для управления режимами работы программы"""
from enum import Enum


class Mode(Enum):
    """Режимы работы программы"""
    MAP_EDIT = "map_edit"  # Режим редактирования карты
    ROBOT = "robot"        # Режим управления роботом


class ModeManager:
    """Класс для управления переключением режимов"""

    def __init__(self, initial_mode=Mode.MAP_EDIT):
        """
        Инициализация менеджера режимов

        Args:
            initial_mode: начальный режим работы (по умолчанию MAP_EDIT)
        """
        # Сохраняем текущий режим
        self.current_mode = initial_mode

    def toggle_mode(self):
        """Переключить режим на противоположный"""
        # Если текущий режим MAP_EDIT, переключаем на ROBOT
        if self.current_mode == Mode.MAP_EDIT:
            self.current_mode = Mode.ROBOT
            print("Режим: РОБОТ (управление WASD)")

        # Иначе переключаем на MAP_EDIT
        else:
            self.current_mode = Mode.MAP_EDIT
            print("Режим: РЕДАКТОР КАРТЫ")

    def is_map_mode(self):
        """Проверить, активен ли режим редактирования карты"""
        # Верните True, если текущий режим MAP_EDIT
        return self.current_mode == Mode.MAP_EDIT

    def is_robot_mode(self):
        """Проверить, активен ли режим робота"""
        # Верните True, если текущий режим ROBOT
        return self.current_mode == Mode.ROBOT

    def get_mode_name(self):
        """Получить название текущего режима"""
        if self.current_mode == Mode.MAP_EDIT:
            return "MAP EDIT"
        else:
            return "ROBOT"

