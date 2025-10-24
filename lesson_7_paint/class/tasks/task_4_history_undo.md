# ⏪ Блок 4: История и отмена (25-30 мин)

## 🎯 Зачем нужна история?

Представьте: вы нарисовали сложную карту, случайно провели линию не там... и приходится долго стирать!

**Решение:** Кнопка "Отменить" (как Ctrl+Z в Word, Photoshop, и других программах).

Но как это реализовать?

---

## 🧠 Теория: Как работает отмена?

### Принцип:

1. **Запоминаем каждое действие** пользователя в список
2. **При отмене** берём последнее действие и выполняем **обратное**

### Пример:

```
Действия пользователя:
1. Заполнил клетку (5, 10) → запомнили: {'type': 'fill', 'cell': (5, 10)}
2. Заполнил клетку (6, 10) → запомнили: {'type': 'fill', 'cell': (6, 10)}
3. Стёр клетку (5, 10) → запомнили: {'type': 'erase', 'cell': (5, 10)}

Нажали "Отменить":
- Берём последнее: {'type': 'erase', 'cell': (5, 10)}
- Обратное действие: заполнить клетку (5, 10) обратно!

Нажали "Отменить" ещё раз:
- Берём последнее: {'type': 'fill', 'cell': (6, 10)}
- Обратное действие: очистить клетку (6, 10)
```

### Структура действия:

```python
action = {
    'type': 'fill',      # или 'erase'
    'cell': (col, row)   # какая клетка
}
```

---

## 📝 Задание 4.1: Класс History (15 мин)

Создадим класс для хранения и управления историей действий.

**Скопируйте в новую ячейку:**

```python
class History:
    """Класс для управления историей действий с поддержкой отмены"""

    def __init__(self):
        """Инициализация истории"""
        # TODO: Создайте пустой список для хранения действий
        self.actions = ___

    def add_action(self, action):
        """
        Добавить действие в историю

        Args:
            action: словарь с описанием действия
                   {'type': 'fill' или 'erase', 'cell': (col, row)}
        """
        # TODO: Добавьте действие в конец списка
        # Подсказка: используйте .append()
        self.actions.___(___)

    def undo(self):
        """
        Отменить последнее действие

        Returns:
            Последнее действие из истории или None, если история пуста
        """
        # TODO: Проверьте, что история не пуста
        if len(self.actions) == ___:
            return None

        # TODO: Удалите и верните последнее действие
        # Подсказка: используйте .pop() - удаляет последний элемент и возвращает его
        return self.actions.___()

    def clear(self):
        """Очистить всю историю"""
        # TODO: Очистите список
        # Подсказка: используйте .clear()
        self.actions.___()

    def get_size(self):
        """Получить количество действий в истории"""
        return len(___)
```

---

## ✅ Тест класса History

**Скопируйте в новую ячейку:**

```python
# Создаём историю
history = History()

print(f"Начальный размер истории: {history.get_size()}")

# Добавляем действия
history.add_action({'type': 'fill', 'cell': (5, 5)})
history.add_action({'type': 'fill', 'cell': (6, 6)})
history.add_action({'type': 'erase', 'cell': (5, 5)})

print(f"\nПосле добавления 3 действий: {history.get_size()}")

# Отменяем последнее действие
action = history.undo()
print(f"\nОтменили действие: {action}")
print(f"Размер истории после отмены: {history.get_size()}")

# Отменяем ещё раз
action = history.undo()
print(f"\nОтменили действие: {action}")
print(f"Размер истории: {history.get_size()}")

# Отменяем последнее
action = history.undo()
print(f"\nОтменили действие: {action}")
print(f"Размер истории: {history.get_size()}")

# Пытаемся отменить, когда история пуста
action = history.undo()
print(f"\nПопытка отмены при пустой истории: {action}")

# Очистка
history.add_action({'type': 'fill', 'cell': (1, 1)})
print(f"\nДобавили действие, размер: {history.get_size()}")
history.clear()
print(f"После clear(): {history.get_size()}")
```

**Ожидаемый вывод:**
```
Начальный размер истории: 0

После добавления 3 действий: 3

Отменили действие: {'type': 'erase', 'cell': (5, 5)}
Размер истории после отмены: 2

Отменили действие: {'type': 'fill', 'cell': (6, 6)}
Размер истории: 1

Отменили действие: {'type': 'fill', 'cell': (5, 5)}
Размер истории: 0

Попытка отмены при пустой истории: None

Добавили действие, размер: 1
После clear(): 0
```

---

## 🎮 Задание 4.2: Интеграция истории в редактор (10-15 мин)

Теперь добавим History в наш редактор и реализуем отмену!

**Скопируйте полный код редактора с историей:**

```python
# Создаём новую сетку и историю
grid = Grid(WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT)
history = History()

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

        # TODO: Обработка клавиши Z для отмены
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                # Получаем последнее действие из истории
                action = history.undo()

                if action is not None:
                    col, row = action['cell']

                    # TODO: Выполняем обратное действие
                    if action['type'] == 'fill':
                        # Отменяем заполнение - очищаем клетку
                        grid.___(col, row)
                        print(f"Отменено заполнение клетки ({col}, {row})")

                    elif action['type'] == 'erase':
                        # TODO: Отменяем стирание - заполняем клетку обратно
                        grid.___(col, row)
                        print(f"Отменено стирание клетки ({col}, {row})")
                else:
                    print("История пуста, нечего отменять")

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
                # TODO: Заполняем клетку
                grid.fill_cell(col, row)

                # TODO: Добавляем действие в историю
                history.add_action({
                    'type': ___,     # 'fill'
                    'cell': (___, ___)
                })

                last_drawn_cell = cell

    # Стирание
    if right_mouse_pressed:
        cell = grid.get_cell_at_position(mouse_x, mouse_y)
        if cell is not None:
            col, row = cell
            if cell != last_erased_cell:
                # Проверяем, что клетка действительно заполнена
                if grid.is_cell_filled(col, row):
                    # TODO: Очищаем клетку
                    grid.clear_cell(col, row)

                    # TODO: Добавляем действие стирания в историю
                    history.add_action({
                        'type': ___,     # 'erase'
                        'cell': (___, ___)
                    })

                last_erased_cell = cell

    # Рисуем сетку
    draw_grid(screen, grid, hover_cell)

    # Обновляем экран
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

---

## ✅ Тестирование отмены

**Попробуйте:**

1. Нарисуйте несколько клеток левой кнопкой
2. Нажмите **Z** несколько раз - клетки должны исчезать по одной!
3. Нарисуйте клетки, сотрите некоторые
4. Нажимайте **Z** - стирание тоже отменяется (клетки появляются обратно)!

**В консоли вы увидите сообщения:**
```
Отменено заполнение клетки (10, 15)
Отменено заполнение клетки (11, 15)
Отменено стирание клетки (10, 14)
...
```

---

## 🎉 Отлично работает!

Теперь у нас есть:
- ✅ Рисование мышью
- ✅ Стирание мышью
- ✅ Подсветка клетки
- ✅ **Отмена действий (Z)**

---

## 🎓 Что мы узнали?

1. ✅ **Паттерн "История"** - сохранение и отмена действий
2. ✅ **Обратные операции** - fill ↔ erase
3. ✅ **Список как стек** - добавляем в конец, берём с конца (pop)
4. ✅ **Интеграция компонентов** - Grid + History работают вместе

---

## 💡 Улучшения (опционально)

**Можете попробовать добавить:**

- Клавиша **C** - очистить всю карту и историю
- Показывать размер истории на экране
- Ограничение истории (например, последние 100 действий)

---

## 🚀 Следующий шаг

Отлично! Редактор работает прекрасно!

Но сейчас весь код в одной большой ячейке. Это неудобно:
- Сложно тестировать отдельные части
- Трудно расширять функционал
- Нельзя переиспользовать код

**Дальше:** Разобьём код на модули (отдельные файлы) для лучшей организации!
