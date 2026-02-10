# 🧹 Блок 3: Стирание + подсветка (20 мин)

## 🖱️ Задание 3.1: Правая кнопка мыши - стирание (10 мин)

Умеем рисовать - отлично! Но если ошиблись, нужно уметь стирать.

Используем **правую кнопку мыши** для стирания (как ластик).

**Копируем предыдущий код и добавляем стирание:**

```python
# Создаём новую сетку
grid = Grid(WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT)

# Флаги состояния мыши
left_mouse_pressed = False
last_drawn_cell = None

# TODO: Добавьте флаги для правой кнопки
right_mouse_pressed = ___  # False
last_erased_cell = ___     # None

# Игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Нажатие кнопки мыши
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка
                left_mouse_pressed = True
                last_drawn_cell = None

            # TODO: Обработка правой кнопки (button == 3)
            elif event.button == ___:
                right_mouse_pressed = ___
                last_erased_cell = ___

        # Отпускание кнопки мыши
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Левая кнопка
                left_mouse_pressed = False
                last_drawn_cell = None

            # TODO: Обработка правой кнопки
            elif event.button == ___:
                right_mouse_pressed = ___
                last_erased_cell = ___

    # Получаем текущую позицию мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Рисование при зажатой левой кнопке
    if left_mouse_pressed:
        cell = grid.get_cell_at_position(mouse_x, mouse_y)
        if cell is not None:
            col, row = cell
            if cell != last_drawn_cell:
                grid.fill_cell(col, row)
                last_drawn_cell = cell

    # TODO: Стирание при зажатой правой кнопке
    if ___:  # right_mouse_pressed
        cell = grid.get_cell_at_position(mouse_x, mouse_y)
        if cell is not None:
            col, row = cell
            # Стираем только если это новая клетка
            if cell != ___:  # last_erased_cell
                # TODO: Очистите клетку
                grid.___(col, row)
                # TODO: Запомните последнюю стертую клетку
                last_erased_cell = ___

    # Рисуем сетку
    draw_grid(screen, grid)

    # Обновляем экран
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

**Проверка:**
- Левая кнопка мыши - рисуем
- Правая кнопка мыши - стираем
- Можно зажимать обе кнопки одновременно!

**Отлично! Теперь полноценный редактор! 🎨**

---

## ✨ Задание 3.2: Подсветка клетки под курсором (10 мин)

Добавим визуальную обратную связь - будем подсвечивать клетку под курсором.

### Шаг 1: Обновляем функцию draw_grid

**Замените функцию draw_grid на эту версию:**

```python
def draw_grid(screen, grid, hover_cell=None):
    """
    Отрисовать сетку на экране

    Args:
        screen: поверхность pygame для рисования
        grid: объект Grid с данными сетки
        hover_cell: клетка под курсором (col, row) или None
    """
    # Очистить экран
    screen.fill(WHITE)

    # Нарисовать все заполненные клетки
    for col, row in grid.filled_cells:
        x = col * grid.cell_width
        y = row * grid.cell_height
        pygame.draw.rect(screen, DARK_GRAY, (x, y, grid.cell_width, grid.cell_height))

    # TODO: Нарисовать подсветку клетки под курсором
    if hover_cell is not None:
        col, row = hover_cell

        # Подсвечиваем только если клетка НЕ заполнена
        if not grid.is_cell_filled(col, row):
            x = col * grid.cell_width
            y = row * grid.cell_height

            # TODO: Нарисуйте прямоугольник голубого цвета
            # Цвет: BLUE
            pygame.draw.rect(___, ___, (x, y, grid.cell_width, grid.cell_height))

    # Нарисовать линии сетки
    for col in range(grid.cols + 1):
        x = col * grid.cell_width
        pygame.draw.line(screen, GRAY, (x, 0), (x, grid.height), 1)

    for row in range(grid.rows + 1):
        y = row * grid.cell_height
        pygame.draw.line(screen, GRAY, (0, y), (grid.width, y), 1)
```

### Шаг 2: Обновляем игровой цикл

**Используйте этот полный код:**

```python
# Создаём новую сетку
grid = Grid(WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT)

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

    # Получаем текущую позицию мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # TODO: Определяем клетку под курсором для подсветки
    hover_cell = grid.get_cell_at_position(___, ___)

    # Рисование
    if left_mouse_pressed:
        cell = grid.get_cell_at_position(mouse_x, mouse_y)
        if cell is not None:
            col, row = cell
            if cell != last_drawn_cell:
                grid.fill_cell(col, row)
                last_drawn_cell = cell

    # Стирание
    if right_mouse_pressed:
        cell = grid.get_cell_at_position(mouse_x, mouse_y)
        if cell is not None:
            col, row = cell
            if cell != last_erased_cell:
                grid.clear_cell(col, row)
                last_erased_cell = cell

    # TODO: Рисуем сетку с подсветкой
    draw_grid(screen, grid, hover_cell=___)

    # Обновляем экран
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

**Проверка:**
- Водите курсором по экрану
- Пустые клетки должны подсвечиваться голубым
- Заполненные клетки НЕ подсвечиваются
- При рисовании/стирании подсветка работает корректно

---

## 🎉 MVP ГОТОВ!

**Поздравляю! Вы создали полноценный редактор препятствий!**

### Что умеет наш редактор:

- ✅ Рисовать препятствия левой кнопкой мыши
- ✅ Стирать препятствия правой кнопкой мыши
- ✅ Подсвечивать клетку под курсором
- ✅ Непрерывное рисование/стирание при зажатой кнопке

### Попробуйте:

1. Нарисуйте лабиринт
2. Нарисуйте стены по краям
3. Создайте препятствия в виде букв

---

## 🎓 Что мы узнали?

1. ✅ **Обработка обеих кнопок мыши** - левая и правая
2. ✅ **Визуальная обратная связь** - подсветка курсора
3. ✅ **Условная отрисовка** - подсвечиваем только пустые клетки
4. ✅ **Полный цикл редактирования** - рисование + стирание

---

## 🚀 Следующий шаг

Редактор работает отлично! Но есть проблема: если случайно нарисовали не то, приходится долго стирать.

**Было бы здорово иметь кнопку "Отменить" (как Ctrl+Z в других программах)!**

**Дальше:** Добавим систему истории действий с возможностью отмены!
