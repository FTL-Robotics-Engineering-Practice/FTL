# 🎨 Блок 2: Отрисовка робота

## 🎯 Цель

Сейчас у нас есть класс Robot, но мы его не видим! Давайте научимся рисовать робота на экране.

Робот будет выглядеть как **круг** с **линией-указателем** направления движения.

---

## 🧠 Теория: Преобразование координат

**Проблема:** Робот использует координаты в **клетках** (float), а pygame рисует в **пикселях** (int).

```python
# Координаты робота (в клетках)
robot.x = 10.5
robot.y = 15.3

# Размер клетки (в пикселях)
cell_width = 10
cell_height = 12

# Экранные координаты (в пикселях)
screen_x = robot.x * cell_width   # 10.5 * 10 = 105 пикселей
screen_y = robot.y * cell_height  # 15.3 * 12 = 183.6 пикселей
```

Также нужно учесть, что у grid может быть **смещение** (offset_x), если есть панель слева.

---

## 📝 Задание 2.1: Обновляем renderer.py

Добавим метод для отрисовки робота в класс Renderer.

**Откройте файл `renderer.py` и добавьте в конец класса Renderer:**

```python
    def draw_robot(self, robot, grid):
        """
        Отрисовать робота на сетке

        Args:
            robot: объект Robot
            grid: объект Grid (для преобразования координат)
        """
        # TODO: Преобразуем координаты робота из клеток в пиксели
        # Формула: screen_x = robot.x * grid.cell_width + grid.offset_x
        screen_x = robot.x * grid.cell_width + grid.___
        screen_y = robot.y * grid.___

        # TODO: Преобразуем радиус робота из клеток в пиксели
        # Используем среднее между cell_width и cell_height для радиуса
        radius_pixels = int(robot.radius * (grid.cell_width + grid.cell_height) / ___)

        # TODO: Нарисуйте круг робота
        # pygame.draw.circle(surface, color, center, radius)
        # Цвет: (0, 200, 0) - зелёный
        # center: (int(screen_x), int(screen_y))
        pygame.draw.circle(
            self.screen,
            (0, 200, 0),  # зелёный цвет
            (int(___), int(___)),
            ___  # radius_pixels
        )

        # TODO: Нарисуйте линию-указатель направления
        # Линия от центра робота в направлении robot.angle
        import math

        # Вычисляем конец линии (длина = radius_pixels)
        end_x = screen_x + radius_pixels * math.cos(robot.___)
        end_y = screen_y + radius_pixels * math.___(robot.angle)

        # pygame.draw.line(surface, color, start_pos, end_pos, width)
        pygame.draw.line(
            self.screen,
            (0, 100, 0),  # темно-зелёный
            (int(screen_x), int(screen_y)),  # начало - центр робота
            (int(___), int(___)),            # конец - в направлении angle
            ___  # толщина 3 пикселя
        )
```

**Сохраните файл.**

---

## 📝 Задание 2.2: Обновляем Grid для поддержки смещения

Если у вас будет левая панель (как в решении), нужно учитывать смещение сетки.

**Откройте `grid.py` и обновите `__init__`:**

```python
    def __init__(self, width, height, cell_width, cell_height, offset_x=0):
        """
        Инициализация сетки

        Args:
            width: ширина окна в пикселях
            height: высота окна в пикселях
            cell_width: ширина одной клетки
            cell_height: высота одной клетки
            offset_x: смещение сетки по X (для панели слева)
        """
        self.width = width
        self.height = height
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.offset_x = offset_x  # <-- ДОБАВЬТЕ ЭТУ СТРОКУ

        # Вычисляем количество клеток
        self.cols = width // cell_width
        self.rows = height // cell_height

        # Множество заполненных клеток
        self.filled_cells = set()
```

**Также обновите метод `get_cell_at_position`:**

```python
    def get_cell_at_position(self, x, y):
        """
        Получить индексы клетки по экранным координатам

        Args:
            x: координата X курсора мыши
            y: координата Y курсора мыши

        Returns:
            (col, row) - индексы клетки или None, если вне границ
        """
        # TODO: Учитываем смещение сетки
        x = x - self.offset_x

        # Проверяем границы
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None

        col = int(x // self.cell_width)
        row = int(y // self.cell_height)

        return (col, row)
```

**Сохраните файл.**

---

## 📝 Задание 2.3: Обновляем Renderer.draw_grid для смещения

**Откройте `renderer.py` и обновите метод `draw_grid`:**

Найдите цикл рисования вертикальных линий и добавьте смещение:

```python
    def draw_grid(self, grid, hover_cell=None):
        """
        Отрисовать сетку на экране

        Args:
            grid: объект Grid с данными сетки
            hover_cell: клетка под курсором (col, row) или None
        """
        # Очистить экран
        self.screen.fill(self.WHITE)

        # Нарисовать все заполненные клетки
        for col, row in grid.filled_cells:
            x = col * grid.cell_width + grid.offset_x  # <-- ДОБАВЬТЕ + grid.offset_x
            y = row * grid.cell_height
            pygame.draw.rect(self.screen, self.DARK_GRAY, (x, y, grid.cell_width, grid.cell_height))

        # Нарисовать подсветку клетки под курсором
        if hover_cell is not None:
            col, row = hover_cell
            if not grid.is_cell_filled(col, row):
                x = col * grid.cell_width + grid.offset_x  # <-- ДОБАВЬТЕ + grid.offset_x
                y = row * grid.cell_height
                pygame.draw.rect(self.screen, self.BLUE, (x, y, grid.cell_width, grid.cell_height))

        # Нарисовать линии сетки
        # Вертикальные линии
        for col in range(grid.cols + 1):
            x = col * grid.cell_width + grid.offset_x  # <-- ДОБАВЬТЕ + grid.offset_x
            pygame.draw.line(self.screen, self.GRAY, (x, 0), (x, grid.height), 1)

        # Горизонтальные линии
        for row in range(grid.rows + 1):
            y = row * grid.cell_height
            pygame.draw.line(self.screen, self.GRAY, (grid.offset_x, y), (grid.offset_x + grid.width, y), 1)
            # <-- ИЗМЕНИЛИ: линия начинается с grid.offset_x и заканчивается на offset_x + width
```

**Сохраните файл.**

---

## ✅ Задание 2.4: Тестирование - рисуем робота

Создадим простую программу для проверки отрисовки робота.

**Создайте файл `test_robot_render.py`:**

```python
"""Тест отрисовки робота"""
import pygame
import sys
from grid import Grid
from renderer import Renderer
from robot import Robot

# Инициализация pygame
pygame.init()

# Настройки окна
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Тест отрисовки робота")

# Настройки сетки
GRID_COLS = 75
GRID_ROWS = 50
CELL_WIDTH = WIDTH // GRID_COLS
CELL_HEIGHT = HEIGHT // GRID_ROWS

# Создаём объекты
grid = Grid(WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT, offset_x=0)
renderer = Renderer(screen)

# Создаём робота в центре карты
robot = Robot(
    x=GRID_COLS / 2.0,  # центр по X
    y=GRID_ROWS / 2.0,  # центр по Y
    angle=0.0,          # смотрит вправо
    radius=1.0
)

# Рисуем несколько препятствий для контекста
grid.fill_cell(35, 20)
grid.fill_cell(36, 20)
grid.fill_cell(37, 20)

clock = pygame.time.Clock()
running = True

print("Тест отрисовки робота")
print("Закройте окно для выхода")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Отрисовка
    renderer.draw_grid(grid)
    renderer.draw_robot(robot, grid)

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
```

**Запустите тест:**

```bash
python test_robot_render.py
```

**Что вы должны увидеть:**
- Сетка с несколькими препятствиями
- **Зелёный круг в центре** — робот
- **Тёмно-зелёная линия вправо** — указатель направления

**Отлично! Робот виден на экране! 🎉**

---

## 📝 Задание 2.5: БОНУС - Движущийся робот (опционально)

Давайте заставим робота двигаться по кругу для проверки!

**Измените файл `test_robot_render.py`, добавьте в игровой цикл:**

```python
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # TODO: ДОБАВЬТЕ ЭТИ СТРОКИ - робот едет по кругу
    robot.set_velocities(linear=5.0, angular=1.0)  # едет и поворачивает
    robot.update(dt=0.016)  # ~60 FPS

    # Ограничиваем робота границами
    robot.clamp_position(robot.radius, grid.cols - robot.radius,
                        robot.radius, grid.rows - robot.radius)

    # Отрисовка
    renderer.draw_grid(grid)
    renderer.draw_robot(robot, grid)

    pygame.display.flip()
    clock.tick(60)
```

**Запустите снова — робот должен ехать по спирали! 🚀**

---

## 🎓 Что мы узнали?

1. ✅ **Преобразование координат** — клетки (float) → пиксели (int)
2. ✅ **Отрисовка круга** — `pygame.draw.circle()`
3. ✅ **Отрисовка линии направления** — используя `cos(angle)` и `sin(angle)`
4. ✅ **Смещение сетки** — `offset_x` для панели слева
5. ✅ **Визуализация угла** — линия показывает, куда смотрит робот
6. ✅ **Интеграция компонентов** — Robot + Grid + Renderer работают вместе

---

## 🚀 Следующий шаг

Теперь мы видим робота на экране! Но у нас есть проблема: редактор карты и робот работают одновременно.

**Дальше:** Создадим систему режимов — TAB переключает между редактированием карты и управлением роботом!
