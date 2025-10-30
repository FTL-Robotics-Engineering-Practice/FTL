# 🔄 Блок 3: Режимы работы - ModeManager

## 🎯 Цель

Сейчас у нас есть проблема: редактор карты и робот работают одновременно. Если мы хотим управлять роботом, мышь всё равно рисует на карте!

**Решение:** Разделить программу на **два режима**:
1. **MAP_EDIT** — режим редактирования карты (мышь рисует, робот стоит)
2. **ROBOT** — режим робота (WASD управление, мышь не рисует)

Переключение между режимами — клавиша **TAB**.

---

## 🧠 Теория: Паттерн State Machine

**State Machine (Машина состояний)** — это паттерн, где программа может находиться в разных **состояниях**, и в каждом состоянии ведёт себя по-разному.

### Пример из жизни: Светофор

```
Состояния: КРАСНЫЙ, ЖЁЛТЫЙ, ЗЕЛЁНЫЙ
- В состоянии КРАСНЫЙ: машины стоят
- В состоянии ЗЕЛЁНЫЙ: машины едут
- Переключение: по таймеру
```

### Наша программа

```
Состояния: MAP_EDIT, ROBOT
- В состоянии MAP_EDIT:
  ✅ Мышь рисует препятствия
  ❌ WASD не работают
  ❌ Робот не двигается

- В состоянии ROBOT:
  ❌ Мышь не рисует
  ✅ WASD управляют роботом
  ✅ Робот обновляется и двигается

Переключение: клавиша TAB
```

---

## 🧠 Теория: Enum в Python

**Enum (enumeration)** — это специальный тип для набора именованных констант.

```python
from enum import Enum

class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

# Использование
current_color = Color.RED
print(current_color)  # Color.RED
print(current_color.value)  # "red"

# Сравнение
if current_color == Color.RED:
    print("Красный!")
```

**Зачем enum?**
- ✅ Избегаем опечаток (Color.RED вместо строки "red")
- ✅ Автодополнение в IDE
- ✅ Явный набор возможных значений

---

## 📝 Задание 3.1: Создаём mode_manager.py

Создадим класс для управления режимами работы.

**Создайте файл `mode_manager.py`:**

```python
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
        # TODO: Сохраните текущий режим
        self.current_mode = ___

    def toggle_mode(self):
        """Переключить режим на противоположный"""
        # TODO: Если текущий режим MAP_EDIT, переключаем на ROBOT
        if self.current_mode == Mode.___:
            self.current_mode = Mode.___
            print("Режим: РОБОТ (управление WASD)")

        # TODO: Иначе переключаем на MAP_EDIT
        else:
            self.current_mode = Mode.___
            print("Режим: РЕДАКТОР КАРТЫ")

    def is_map_mode(self):
        """Проверить, активен ли режим редактирования карты"""
        # TODO: Верните True, если текущий режим MAP_EDIT
        return self.current_mode == Mode.___

    def is_robot_mode(self):
        """Проверить, активен ли режим робота"""
        # TODO: Верните True, если текущий режим ROBOT
        return self.current_mode == Mode.___

    def get_mode_name(self):
        """Получить название текущего режима"""
        if self.current_mode == Mode.MAP_EDIT:
            return "MAP EDIT"
        else:
            return "ROBOT"
```

**Сохраните файл.**

---

## ✅ Задание 3.2: Тестирование ModeManager

**Создайте файл `test_mode_manager.py`:**

```python
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
```

**Запустите:**

```bash
python test_mode_manager.py
```

**Ожидаемый вывод:**

```
=== ТЕСТ 1: Начальный режим ===
Текущий режим: MAP EDIT
Это режим карты? True
Это режим робота? False

=== ТЕСТ 2: Переключение режима ===
Режим: РОБОТ (управление WASD)
Текущий режим: ROBOT
Это режим карты? False
Это режим робота? True

=== ТЕСТ 3: Переключение обратно ===
Режим: РЕДАКТОР КАРТЫ
Текущий режим: MAP EDIT

=== ТЕСТ 4: Несколько переключений ===
Режим: РОБОТ (управление WASD)
Режим: РЕДАКТОР КАРТЫ
Режим: РОБОТ (управление WASD)
Режим: РЕДАКТОР КАРТЫ

✅ Все тесты пройдены!
```

---

## 📝 Задание 3.3: Интегрируем режимы в InputManager

Теперь InputManager должен вести себя по-разному в разных режимах.

**Откройте `input_manager.py` и обновите:**

### Шаг 1: Добавьте mode_manager в __init__

```python
    def __init__(self, grid, history, running_flag, mode_manager):
        """
        Инициализация менеджера ввода

        Args:
            grid: объект Grid
            history: объект History
            running_flag: список [True/False] для управления циклом
            mode_manager: объект ModeManager  # <-- ДОБАВЛЕНО
        """
        self.grid = grid
        self.history = history
        self.running_flag = running_flag
        self.mode_manager = mode_manager  # <-- ДОБАВЛЕНО

        # Флаги состояния мыши
        self.left_mouse_pressed = False
        self.right_mouse_pressed = False
        self.last_drawn_cell = None
        self.last_erased_cell = None

        # Словарь привязок клавиш
        self.key_bindings = {}

        # Настраиваем привязки клавиш
        self._setup_default_bindings()
```

### Шаг 2: Добавьте привязку клавиши TAB

В методе `_setup_default_bindings()` добавьте:

```python
    def _setup_default_bindings(self):
        """Настроить привязки клавиш по умолчанию"""
        self.bind_key(pygame.K_ESCAPE, "выход", self._exit_program)
        self.bind_key(pygame.K_h, "показать справку", self._show_help)
        self.bind_key(pygame.K_z, "отменить последнее действие", self._undo_action)
        self.bind_key(pygame.K_c, "очистить всё", self._clear_all)
        # TODO: Добавьте привязку TAB для переключения режима
        self.bind_key(pygame.K_TAB, "переключить режим", self.___)
```

### Шаг 3: Добавьте метод переключения режима

В конец класса InputManager добавьте:

```python
    def _toggle_mode(self):
        """Переключить режим работы"""
        # TODO: Вызовите метод toggle_mode у mode_manager
        self.mode_manager.___()
```

### Шаг 4: Обновите handle_mouse_motion

Рисование мышью должно работать **только в режиме MAP_EDIT**:

```python
    def handle_mouse_motion(self, mouse_x, mouse_y):
        """
        Обработать движение мыши (рисование/стирание)

        Args:
            mouse_x: координата X мыши
            mouse_y: координата Y мыши
        """
        # TODO: Проверьте, что мы в режиме редактирования карты
        # Если нет - выходим из функции
        if not self.mode_manager.___():
            return

        # Рисование при зажатой левой кнопке
        if self.left_mouse_pressed:
            cell = self.grid.get_cell_at_position(mouse_x, mouse_y)
            if cell is not None:
                col, row = cell
                if cell != self.last_drawn_cell:
                    self.grid.fill_cell(col, row)
                    self.history.add_action({'type': 'fill', 'cell': (col, row)})
                    self.last_drawn_cell = cell

        # Стирание при зажатой правой кнопке
        if self.right_mouse_pressed:
            cell = self.grid.get_cell_at_position(mouse_x, mouse_y)
            if cell is not None:
                col, row = cell
                if cell != self.last_erased_cell:
                    if self.grid.is_cell_filled(col, row):
                        self.grid.clear_cell(col, row)
                        self.history.add_action({'type': 'erase', 'cell': (col, row)})
                    self.last_erased_cell = cell
```

**Сохраните файл.**

---

## 📝 Задание 3.4: Обновляем main.py

Подключим ModeManager к программе.

**Откройте `main.py` и внесите изменения:**

### Шаг 1: Импортируйте ModeManager

```python
from grid import Grid
from history import History
from renderer import Renderer
from input_manager import InputManager
from mode_manager import ModeManager  # <-- ДОБАВЛЕНО
from robot import Robot                # <-- ДОБАВЛЕНО
```

### Шаг 2: Создайте объекты

```python
    # Создаём объекты
    grid = Grid(WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT, offset_x=0)
    history = History()
    renderer = Renderer(screen)
    mode_manager = ModeManager()  # <-- ДОБАВЛЕНО

    # Создаём робота в центре карты
    robot = Robot(
        x=GRID_COLS / 2.0,
        y=GRID_ROWS / 2.0,
        angle=0.0,
        radius=1.0
    )

    # Создаём менеджер ввода (теперь с mode_manager)
    input_manager = InputManager(grid, history, running, mode_manager)  # <-- ИЗМЕНЕНО
```

### Шаг 3: Условная отрисовка робота

В игровом цикле добавьте условие:

```python
    # Игровой цикл
    while running[0]:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running[0] = False
            else:
                input_manager.handle_event(event)

        # Получаем позицию мыши
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # TODO: Обновляем робота только в режиме ROBOT
        if mode_manager.___():
            robot.set_velocities(linear=5.0, angular=1.0)  # временно - по кругу
            robot.update(dt=0.016)
            robot.clamp_position(robot.radius, grid.cols - robot.radius,
                                robot.radius, grid.rows - robot.radius)

        # TODO: Определяем клетку под курсором только в режиме MAP_EDIT
        hover_cell = None
        if mode_manager.___():
            hover_cell = grid.get_cell_at_position(mouse_x, mouse_y)
            input_manager.handle_mouse_motion(mouse_x, mouse_y)

        # Отрисовка
        renderer.draw_grid(grid, hover_cell=hover_cell)

        # TODO: Рисуем робота только в режиме ROBOT
        if mode_manager.___():
            renderer.draw_robot(robot, grid)

        # Обновление экрана
        pygame.display.flip()
        clock.tick(60)
```

**Сохраните файл.**

---

## ✅ Тестирование режимов

**Запустите программу:**

```bash
python main.py
```

**Проверка:**

1. **Начальный режим (MAP_EDIT):**
   - Мышь рисует препятствия ✅
   - Робота не видно ✅

2. **Нажмите TAB:**
   - В консоли: "Режим: РОБОТ (управление WASD)"
   - Мышь больше не рисует ✅
   - Робот появился и едет по кругу ✅

3. **Нажмите TAB ещё раз:**
   - В консоли: "Режим: РЕДАКТОР КАРТЫ"
   - Мышь снова рисует ✅
   - Робот исчез ✅

**Отлично! Режимы работают! 🎉**

---

## 🎓 Что мы узнали?

1. ✅ **Паттерн State Machine** — программа с разными режимами работы
2. ✅ **Enum в Python** — именованные константы для режимов
3. ✅ **Условная логика** — разное поведение в разных режимах
4. ✅ **Переключение состояний** — метод `toggle_mode()`
5. ✅ **Проверка состояния** — методы `is_map_mode()`, `is_robot_mode()`
6. ✅ **Интеграция** — все компоненты работают вместе

---

## 🚀 Следующий шаг

Режимы работают, но робот пока едет сам по себе. Пора дать игроку управление!

**Дальше:** Добавим управление роботом клавишами WASD!
