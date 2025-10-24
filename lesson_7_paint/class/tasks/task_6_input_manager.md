# 🎮 Блок 6: InputManager с клавиатурой (20-30 мин)

## 🎯 Проблема текущего подхода

Сейчас в main.py вся логика управления:
- Обработка мыши
- Обработка клавиш
- Флаги состояния
- Вызовы методов grid и history

**Что не так:**
- main.py слишком большой и сложный
- Трудно добавить новые команды
- Логика управления смешана с игровым циклом

**Решение:** Создадим класс InputManager, который будет управлять ВСЕМ вводом!

---

## 🧠 Идея: Привязка клавиш

Вместо кучи `if event.key == pygame.K_z:` создадим **систему привязок клавиш**:

```python
# Привяжем клавишу к функции
input_manager.bind_key(pygame.K_z, "отменить", функция_отмены)
input_manager.bind_key(pygame.K_c, "очистить всё", функция_очистки)
input_manager.bind_key(pygame.K_h, "справка", функция_справки)
```

Теперь легко добавлять новые команды!

---

## 📝 Задание 6.1: Создаём input_manager.py (15 мин)

**Создайте файл `input_manager.py` и скопируйте:**

```python
"""Модуль для управления вводом с клавиатуры и мыши"""
import pygame

class InputManager:
    """Класс для управления всем вводом (мышь + клавиатура)"""

    def __init__(self, grid, history, running_flag):
        """
        Инициализация менеджера ввода

        Args:
            grid: объект Grid
            history: объект History
            running_flag: список [True/False] для управления циклом
        """
        self.grid = grid
        self.history = history
        self.running_flag = running_flag

        # Флаги состояния мыши
        self.left_mouse_pressed = False
        self.right_mouse_pressed = False
        self.last_drawn_cell = None
        self.last_erased_cell = None

        # TODO: Словарь привязок клавиш
        # Структура: {код_клавиши: {'description': описание, 'function': функция}}
        self.key_bindings = {}

        # Настраиваем привязки клавиш
        self._setup_default_bindings()

    def bind_key(self, key, description, function):
        """
        Привязать клавишу к функции

        Args:
            key: код клавиши pygame (pygame.K_z, pygame.K_c и т.д.)
            description: описание действия (строка)
            function: функция, которую нужно вызвать
        """
        # TODO: Сохраните привязку в словарь
        self.key_bindings[___] = {
            'description': ___,
            'function': ___
        }

    def _setup_default_bindings(self):
        """Настроить привязки клавиш по умолчанию"""
        # TODO: Привяжите клавиши к методам
        self.bind_key(pygame.K_ESCAPE, "выход", self._exit_program)
        self.bind_key(pygame.K_h, "показать справку", self._show_help)
        self.bind_key(pygame.K_z, "отменить последнее действие", self._undo_action)
        self.bind_key(pygame.K_c, "очистить всё", self._clear_all)

    def handle_event(self, event):
        """
        Обработать событие pygame

        Args:
            event: объект события pygame
        """
        # Обработка клавиш
        if event.type == pygame.KEYDOWN:
            # TODO: Проверьте, есть ли привязка для этой клавиши
            if event.key in self.___:
                # Вызываем привязанную функцию
                self.key_bindings[event.key]['___']()

        # Обработка мыши - нажатие
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_button_down(event.button)

        # Обработка мыши - отпускание
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_button_up(event.button)

    def handle_mouse_button_down(self, button):
        """Обработать нажатие кнопки мыши"""
        if button == 1:  # Левая кнопка
            self.left_mouse_pressed = True
            self.last_drawn_cell = None
        elif button == 3:  # Правая кнопка
            self.right_mouse_pressed = True
            self.last_erased_cell = None

    def handle_mouse_button_up(self, button):
        """Обработать отпускание кнопки мыши"""
        if button == 1:  # Левая кнопка
            self.left_mouse_pressed = False
            self.last_drawn_cell = None
        elif button == 3:  # Правая кнопка
            self.right_mouse_pressed = False
            self.last_erased_cell = None

    def handle_mouse_motion(self, mouse_x, mouse_y):
        """
        Обработать движение мыши (рисование/стирание)

        Args:
            mouse_x: координата X мыши
            mouse_y: координата Y мыши
        """
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

    # ===== Функции-обработчики команд =====

    def _exit_program(self):
        """Выход из программы"""
        # TODO: Установите флаг running в False
        self.running_flag[0] = ___
        print("Выход из программы")

    def _undo_action(self):
        """Отменить последнее действие"""
        action = self.history.undo()
        if action is not None:
            col, row = action['cell']

            if action['type'] == 'fill':
                # TODO: Отменяем заполнение - очищаем клетку
                self.grid.___(col, row)
                print(f"Отменено заполнение ({col}, {row})")

            elif action['type'] == 'erase':
                # TODO: Отменяем стирание - заполняем обратно
                self.grid.___(col, row)
                print(f"Отменено стирание ({col}, {row})")
        else:
            print("История пуста, нечего отменять")

    def _clear_all(self):
        """Очистить всю сетку и историю"""
        # TODO: Очистите сетку
        self.grid.___()
        # TODO: Очистите историю
        self.history.___()
        print("Сетка и история очищены")

    def _show_help(self):
        """Показать справку по управлению"""
        print("\n" + "="*50)
        print("УПРАВЛЕНИЕ:")
        print("="*50)

        # TODO: Выведите все привязки клавиш
        for key, binding in self.key_bindings.items():
            # Получаем название клавиши
            key_name = pygame.key.name(key).upper()
            description = binding['description']
            print(f"  {key_name} - {description}")

        print("="*50)
        print("МЫШЬ:")
        print("  ЛКМ (зажать) - рисовать препятствия")
        print("  ПКМ (зажать) - стирать препятствия")
        print("="*50)
        print(f"Клеток заполнено: {len(self.grid.filled_cells)}")
        print(f"Действий в истории: {self.history.get_size()}")
        print("="*50 + "\n")
```

**Сохраните файл.**

---

## 📝 Задание 6.2: Обновляем main.py (5-10 мин)

Теперь main.py станет намного проще!

**Замените содержимое `main.py` на это:**

```python
"""Главный файл программы - редактор препятствий"""
import pygame
import sys

from grid import Grid
from history import History
from renderer import Renderer
from input_manager import InputManager

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

    # Флаг работы (используем список, чтобы InputManager мог его изменять)
    running = [True]

    # TODO: Создайте объекты
    grid = Grid(WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT)
    history = History()
    renderer = Renderer(screen)
    input_manager = InputManager(___, ___, ___)

    print("Редактор препятствий запущен!")
    print("Нажмите H для справки по управлению")

    # Игровой цикл
    while running[0]:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running[0] = False
            else:
                # TODO: Передайте событие в InputManager
                input_manager.handle_event(___)

        # TODO: Получите позицию мыши и передайте в InputManager
        mouse_x, mouse_y = pygame.mouse.get_pos()
        input_manager.handle_mouse_motion(___, ___)

        # Определяем клетку под курсором для подсветки
        hover_cell = grid.get_cell_at_position(mouse_x, mouse_y)

        # Отрисовка
        renderer.draw_grid(grid, hover_cell=hover_cell)

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

**Запустите программу:**

```bash
python main.py
```

**Проверка новых команд:**

1. **H** - показать справку
   ```
   ==================================================
   УПРАВЛЕНИЕ:
   ==================================================
     ESCAPE - выход
     H - показать справку
     Z - отменить последнее действие
     C - очистить всё
   ==================================================
   МЫШЬ:
     ЛКМ (зажать) - рисовать препятствия
     ПКМ (зажать) - стирать препятствия
   ==================================================
   Клеток заполнено: 0
   Действий в истории: 0
   ==================================================
   ```

2. **C** - очистить всё (нарисуйте что-то, потом нажмите C)
3. **Z** - отмена работает?
4. **ESC** - выход из программы

---

## 🎉 Отлично работает!

Теперь у нас профессиональная архитектура:
- ✅ **grid.py** - хранит данные
- ✅ **history.py** - управляет историей
- ✅ **renderer.py** - отрисовывает всё
- ✅ **input_manager.py** - управляет всем вводом
- ✅ **main.py** - чистый игровой цикл

---

## 🎓 Что мы узнали?

1. ✅ **Паттерн "Менеджер ввода"** - централизация управления
2. ✅ **Привязка клавиш** - гибкая система команд
3. ✅ **Разделение ответственности** - каждый класс делает своё
4. ✅ **Чистый код** - main.py стал простым и понятным

---

## 💡 Преимущества InputManager:

| Было | Стало |
|------|-------|
| Куча if в main.py | Система привязок |
| Трудно добавить команду | Один вызов bind_key() |
| Логика размазана | Всё в одном месте |
| Нет справки | Справка генерируется автоматически |

---

## 🚀 Следующий шаг (БОНУС)

Редактор полностью готов и работает отлично!

Осталось одно улучшение: **сохранение и загрузка карт в файл**.

**Дальше (если успеем):** Добавим MapManager для работы с JSON файлами!
