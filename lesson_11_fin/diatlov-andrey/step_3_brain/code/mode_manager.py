"""Менеджер режимов работы программы"""
from enum import Enum


class Mode(Enum):
    """Режимы работы"""
    MAP_EDIT = "map_edit"  # Режим редактирования карты
    ROBOT = "robot"        # Режим управления роботом
    BRAIN = "brain"        # Режим автоматического управления через Brain


class ModeManager:
    """Управление режимами работы"""

    def __init__(self, initial_mode=Mode.MAP_EDIT):
        """
        Инициализация менеджера режимов

        Args:
            initial_mode: начальный режим (по умолчанию MAP_EDIT)
        """
        self.current_mode = initial_mode

    def toggle_mode(self):
        """Переключить режим циклически: MAP_EDIT -> ROBOT -> BRAIN -> MAP_EDIT"""
        if self.current_mode == Mode.MAP_EDIT:
            self.current_mode = Mode.ROBOT
            print("Режим: РОБОТ")
        elif self.current_mode == Mode.ROBOT:
            self.current_mode = Mode.BRAIN
            print("Режим: BRAIN")
        else:  # BRAIN
            self.current_mode = Mode.MAP_EDIT
            print("Режим: РЕДАКТОР КАРТЫ")

    def get_mode_name(self):
        """Получить название текущего режима"""
        if self.current_mode == Mode.MAP_EDIT:
            return "РЕДАКТОР КАРТЫ"
        elif self.current_mode == Mode.ROBOT:
            return "РОБОТ"
        elif self.current_mode == Mode.BRAIN:
            return "BRAIN"
        return "UNKNOWN"

    def is_map_mode(self):
        """Проверить, активен ли режим редактирования карты"""
        return self.current_mode == Mode.MAP_EDIT

    def is_robot_mode(self):
        """Проверить, активен ли режим робота"""
        return self.current_mode == Mode.ROBOT

    def is_brain_mode(self):
        """Проверить, активен ли режим Brain"""
        return self.current_mode == Mode.BRAIN

    def is_manual_mode(self):
        """Проверить, активен ли ручной режим (алиас для is_robot_mode)"""
        return self.is_robot_mode()
