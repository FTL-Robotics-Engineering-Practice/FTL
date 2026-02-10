"""Модуль для работы с историей действий"""

class History:
    """Класс для управления историей действий с поддержкой отмены"""

    def __init__(self):
        """Инициализация истории"""
        self.actions = []

    def add_action(self, action):
        """Добавить действие в историю"""
        self.actions.append(action)

    def undo(self):
        """Отменить последнее действие"""
        if len(self.actions) == 0:
            return None
        return self.actions.pop()

    def clear(self):
        """Очистить всю историю"""
        self.actions.clear()

    def get_size(self):
        """Получить количество действий в истории"""
        return len(self.actions)

