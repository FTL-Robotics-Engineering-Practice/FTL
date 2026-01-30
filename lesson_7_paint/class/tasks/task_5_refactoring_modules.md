# 🗂️ Блок 5: Рефакторинг в модули (20 мин)

## 🎯 Зачем разбивать на файлы?

Сейчас весь код в одной ячейке notebook. Это работает, но:

❌ **Проблемы:**
- Сложно найти нужный код
- Трудно тестировать отдельные части
- Нельзя переиспользовать классы в других проектах
- Код становится длинным и запутанным

✅ **Решение:** Разбить на модули (отдельные файлы)

---

## 📂 Структура проекта

Создадим такую структуру:

```
lesson_7_sensors/class/
├── grid.py           # Класс Grid
├── history.py        # Класс History
├── renderer.py       # Класс Renderer (отрисовка)
└── main.py          # Главный файл (игровой цикл)
```

**Каждый файл - отдельная ответственность!**

---

## 📝 Задание 5.1: Создаём grid.py (5 мин)

Переносим класс Grid в отдельный файл.

**Создайте файл `grid.py` и скопируйте туда:**

```python
"""Модуль для работы с сеткой препятствий"""

class Grid:
    """Класс для управления сеткой препятствий"""

    def __init__(self, width, height, cell_width, cell_height):
        """Инициализация сетки"""
        self.width = width
        self.height = height
        self.cell_width = cell_width
        self.cell_height = cell_height

        self.cols = width // cell_width
        self.rows = height // cell_height

        # Множество заполненных клеток
        self.filled_cells = set()

    def get_cell_at_position(self, x, y):
        """Получить индексы клетки по экранным координатам"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None

        col = int(x // self.cell_width)
        row = int(y // self.cell_height)
        return (col, row)

    def fill_cell(self, col, row):
        """Заполнить клетку"""
        self.filled_cells.add((col, row))

    def clear_cell(self, col, row):
        """Очистить клетку"""
        self.filled_cells.discard((col, row))

    def is_cell_filled(self, col, row):
        """Проверить, заполнена ли клетка"""
        return (col, row) in self.filled_cells

    def clear_all(self):
        """Очистить все клетки"""
        self.filled_cells.clear()
```

**Сохраните файл.**

---

## 📝 Задание 5.2: Создаём history.py (3 мин)

**Создайте файл `history.py` и скопируйте:**

```python
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
```

**Сохраните файл.**

---

## 📝 Задание 5.3: Создаём renderer.py (7 мин)

Переносим функцию отрисовки в класс Renderer.

**Создайте файл `renderer.py` и скопируйте:**

```python
"""Модуль для отрисовки сетки и интерфейса"""
import pygame

class Renderer:
    """Класс для отрисовки элементов редактора"""

    def __init__(self, screen):
        """
        Инициализация рендерера

        Args:
            screen: экран pygame для отрисовки
        """
        self.screen = screen

        # Цвета
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (100, 100, 100)
        self.BLUE = (150, 150, 255)
        self.BLACK = (0, 0, 0)

    def draw_grid(self, grid, hover_cell=None):
        """
        Отрисовать сетку на экране

        Args:
            grid: объект Grid с данными сетки
            hover_cell: клетка под курсором (col, row) или None
        """
        # Очистить экран
        self.screen.fill(self.WHITE)

        # TODO: Нарисовать все заполненные клетки
        for col, row in grid.filled_cells:
            x = col * grid.cell_width
            y = row * grid.cell_height
            pygame.draw.rect(self.screen, self.___, (x, y, grid.cell_width, grid.cell_height))

        # TODO: Нарисовать подсветку клетки под курсором
        if hover_cell is not None:
            col, row = hover_cell
            if not grid.is_cell_filled(col, row):
                x = col * grid.cell_width
                y = row * grid.cell_height
                pygame.draw.rect(self.screen, self.___, (x, y, grid.cell_width, grid.cell_height))

        # TODO: Нарисовать линии сетки
        # Вертикальные линии
        for col in range(grid.cols + 1):
            x = col * grid.cell_width
            pygame.draw.line(self.screen, self.___, (x, 0), (x, grid.height), 1)

        # Горизонтальные линии
        for row in range(grid.rows + 1):
            y = row * grid.cell_height
            pygame.draw.line(self.screen, self.___, (0, y), (grid.width, y), 1)
```

**Сохраните файл.**

**Подсказка для пропусков:**
- Заполненные клетки: `DARK_GRAY`
- Подсветка: `BLUE`
- Линии сетки: `GRAY`

---

## 📝 Задание 5.4: Создаём main.py (5 мин)

Теперь главный файл с импортами и игровым циклом.

**Создайте файл `main.py` и скопируйте:**

```python
"""Главный файл программы - редактор препятствий"""
import pygame
import sys

# TODO: Импортируйте классы из наших модулей
from grid import ___
from history import ___
from renderer import ___

def main():
    """Главная функция программы"""
    # Инициализация pygame
    pygame.init()

    # Настройки окна
    WIDTH = 800
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Редактор препятствий")

    # Настройки сетки
    GRID_COLS = 75
    GRID_ROWS = 50
    CELL_WIDTH = WIDTH // GRID_COLS
    CELL_HEIGHT = HEIGHT // GRID_ROWS

    # Часы
    clock = pygame.time.Clock()

    # TODO: Создайте объекты
    grid = ___(WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT)
    history = ___()
    renderer = ___(screen)

    # Флаги состояния мыши
    left_mouse_pressed = False
    right_mouse_pressed = False
    last_drawn_cell = None
    last_erased_cell = None

    # Игровой цикл
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Обработка клавиш
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    # Отмена
                    action = history.undo()
                    if action is not None:
                        col, row = action['cell']
                        if action['type'] == 'fill':
                            grid.clear_cell(col, row)
                            print(f"Отменено заполнение ({col}, {row})")
                        elif action['type'] == 'erase':
                            grid.fill_cell(col, row)
                            print(f"Отменено стирание ({col}, {row})")

            # Обработка мыши
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_mouse_pressed = True
                    last_drawn_cell = None
                elif event.button == 3:
                    right_mouse_pressed = True
                    last_erased_cell = None

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    left_mouse_pressed = False
                    last_drawn_cell = None
                elif event.button == 3:
                    right_mouse_pressed = False
                    last_erased_cell = None

        # Получаем позицию мыши
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover_cell = grid.get_cell_at_position(mouse_x, mouse_y)

        # Рисование
        if left_mouse_pressed:
            cell = grid.get_cell_at_position(mouse_x, mouse_y)
            if cell is not None:
                col, row = cell
                if cell != last_drawn_cell:
                    grid.fill_cell(col, row)
                    history.add_action({'type': 'fill', 'cell': (col, row)})
                    last_drawn_cell = cell

        # Стирание
        if right_mouse_pressed:
            cell = grid.get_cell_at_position(mouse_x, mouse_y)
            if cell is not None:
                col, row = cell
                if cell != last_erased_cell:
                    if grid.is_cell_filled(col, row):
                        grid.clear_cell(col, row)
                        history.add_action({'type': 'erase', 'cell': (col, row)})
                    last_erased_cell = cell

        # TODO: Отрисовка
        renderer.draw_grid(___, hover_cell=___)

        # Обновление экрана
        pygame.display.flip()
        clock.tick(60)

    # Завершение
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
```

**Сохраните файл.**

---

## ✅ Запуск и тестирование

**Из командной строки в папке с файлами:**

```bash
python main.py
```

**Или в новой ячейке notebook:**

```python
%run main.py
```

**Проверка:**
- Программа запускается?
- Рисование работает?
- Стирание работает?
- Подсветка работает?
- Отмена (Z) работает?

**Если есть ошибки импорта:**
- Проверьте, что все файлы в одной папке
- Проверьте названия файлов (grid.py, history.py, renderer.py, main.py)
- Проверьте, что классы названы правильно (Grid, History, Renderer)

---

## 🎓 Что мы узнали?

1. ✅ **Модульная архитектура** - разбиение кода на файлы
2. ✅ **Импорты** - использование классов из других файлов
3. ✅ **Ответственность** - каждый модуль делает одну вещь
4. ✅ **Переиспользование** - классы можно использовать в других проектах

---

## 📊 Преимущества модульной структуры:

| До (монолит) | После (модули) |
|-------------|----------------|
| Весь код в одном месте | Код разделён по ответственности |
| Сложно найти нужное | Ясно, где что искать |
| Нельзя переиспользовать | Можно использовать Grid в других проектах |
| Сложно тестировать | Легко тестировать отдельные модули |

---

## 💡 Тестирование модулей

Теперь можем тестировать каждый модуль отдельно!

**Создайте ячейку в notebook:**

```python
# Тест модуля Grid
from grid import Grid

grid = Grid(800, 600, 10, 12)
grid.fill_cell(5, 5)
print(f"Клетка (5, 5) заполнена: {grid.is_cell_filled(5, 5)}")
print(f"Всего заполнено: {len(grid.filled_cells)}")
```

**Создайте ещё одну ячейку:**

```python
# Тест модуля History
from history import History

history = History()
history.add_action({'type': 'fill', 'cell': (1, 1)})
history.add_action({'type': 'fill', 'cell': (2, 2)})

print(f"Размер истории: {history.get_size()}")
action = history.undo()
print(f"Отменили: {action}")
print(f"Размер после отмены: {history.get_size()}")
```

---

## 🚀 Следующий шаг

Отлично! Код организован и работает!

Но можно улучшить: сейчас вся логика управления (мышь, клавиатура) размазана по main.py.

**Дальше:** Создадим класс InputManager, который будет управлять всем вводом!
