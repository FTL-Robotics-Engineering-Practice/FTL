"""Модуль для работы с жирной сеткой"""


class Points:
    """Класс для рисования жирной сетки"""

    def __init__(self, grid, step=100):
        """
        Инициализация жирной сетки

        Args:
            grid: объект Grid
            step: шаг между линиями в пикселях (по умолчанию 100)
        """
        self.color = (150, 150, 150)  # Серый цвет для линий
        self.step = step
        self.width = grid.width
        self.height = grid.height
        self.line_width = 3  # Толщина линий

        # Создаем список позиций для вертикальных линий
        self.vertical_lines = []
        x = 0
        while x <= grid.width:
            self.vertical_lines.append(x)
            x += step

        # Создаем список позиций для горизонтальных линий
        self.horizontal_lines = []
        y = 0
        while y <= grid.height:
            self.horizontal_lines.append(y)
            y += step

    def get_color(self):
        """
        Получить цвет линий

        Returns:
            tuple: (R, G, B)
        """
        return self.color

    def get_line_width(self):
        """
        Получить толщину линий

        Returns:
            int: толщина в пикселях
        """
        return self.line_width

    def get_vertical_lines(self):
        """
        Получить позиции вертикальных линий

        Returns:
            list: список координат X
        """
        return self.vertical_lines

    def get_horizontal_lines(self):
        """
        Получить позиции горизонтальных линий

        Returns:
            list: список координат Y
        """
        return self.horizontal_lines
