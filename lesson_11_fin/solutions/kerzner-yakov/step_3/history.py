"""Модуль для истории действий с возможностью отмены"""


class History:
    """Класс для хранения истории действий с возможностью отмены"""

    def __init__(self):
        """Инициализация пустой истории"""
        self.actions = []

    def add_action(self, action):
        """
        Добавить действие в историю

        Args:
            action: словарь с информацией о действии
                   {'type': 'fill'/'erase', 'cell': (col, row)}
        """
        self.actions.append(action)

    def undo(self):
        """
        Отменить последнее действие

        Returns:
            dict: информация о последнем действии или None
        """
        if self.actions:
            return self.actions.pop()
        return None

    def clear(self):
        """Очистить всю историю"""
        self.actions = []

    def get_size(self):
        """
        Получить количество действий в истории

        Returns:
            int: количество действий
        """
        return len(self.actions)
