# 🎨 Блок 2: Рисование и отрисовка (25 мин)

## 📝 Задание 2.1: Рисуем сетку на экране (10 мин)

Сейчас у нас есть Grid, который хранит заполненные клетки, но мы их не видим!

Создадим функцию для отрисовки сетки.

**Скопируйте в новую ячейку:**

```python
def draw_grid(screen, grid):
    """
    Отрисовать сетку на экране

    Args:
        screen: поверхность pygame для рисования
        grid: объект Grid с данными сетки
    """
    # Шаг 1: Очистить экран белым цветом
    screen.fill(WHITE)

    # Шаг 2: Нарисовать все заполненные клетки
    for col, row in grid.filled_cells:
        # Вычисляем координаты левого верхнего угла клетки
        x = col * grid.cell_width
        y = row * grid.cell_height

        # TODO: Нарисуйте прямоугольник для заполненной клетки
        # Подсказка: pygame.draw.rect(surface, color, (x, y, width, height))
        # Цвет: DARK_GRAY
        pygame.draw.rect(___, ___, (x, y, grid.cell_width, grid.cell_height))

    # Шаг 3: Нарисовать вертикальные линии сетки
    for col in range(grid.cols + 1):
        x = col * grid.cell_width
        # TODO: Нарисуйте вертикальную линию
        # Подсказка: pygame.draw.line(surface, color, start_pos, end_pos, width)
        # Линия от (x, 0) до (x, grid.height), цвет GRAY, толщина 1
        pygame.draw.line(___, GRAY, (___, ___), (___, ___), 1)

    # Шаг 4: Нарисовать горизонтальные линии сетки
    for row in range(grid.rows + 1):
        # TODO: Вычислите y координату
        y = row * ___
        # TODO: Нарисуйте горизонтальную линию
        # Линия от (0, y) до (grid.width, y)
        pygame.draw.line(___, GRAY, (0, ___), (___, ___), 1)
```

---

## ✅ Тест отрисовки

**Скопируйте в новую ячейку:**

```python
# Создаём сетку и заполняем несколько клеток для теста
grid = Grid(WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT)
grid.fill_cell(10, 10)
grid.fill_cell(11, 10)
grid.fill_cell(12, 10)
grid.fill_cell(10, 11)
grid.fill_cell(10, 12)

# Простой игровой цикл для проверки
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Рисуем сетку
    draw_grid(screen, grid)

    # Обновляем экран
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

**Что вы должны увидеть:**
- Белый фон
- Серые линии сетки (очень мелкая сетка)
- Несколько темно-серых клеток в виде крестика

**Закройте окно, чтобы продолжить.**

---

## 🖱️ Задание 2.2: Клик мыши - заполнение клетки (10 мин)

Теперь добавим возможность заполнять клетки кликом мыши!

**Скопируйте в новую ячейку:**

```python
# Создаём новую сетку (пустую)
grid = Grid(WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT)

# Игровой цикл с обработкой мыши
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # TODO: Обработка клика мыши
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Получаем координаты клика
            mouse_x, mouse_y = event.pos

            # Получаем клетку под курсором
            cell = grid.get_cell_at_position(mouse_x, mouse_y)

            # Если клик внутри сетки
            if cell is not None:
                col, row = cell

                # TODO: Проверьте, какая кнопка мыши нажата
                # event.button == 1 - левая кнопка
                if event.button == ___:
                    # TODO: Заполните клетку
                    grid.___(___, ___)
                    print(f"Заполнена клетка ({col}, {row})")

    # Рисуем сетку
    draw_grid(screen, grid)

    # Обновляем экран
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

**Проверка:**
- Кликайте левой кнопкой мыши по окну
- Клетки должны заполняться темно-серым цветом
- В консоли должны появляться сообщения о заполнении

**Это уже работает! 🎉**

**Закройте окно, чтобы продолжить.**

---

## 🖌️ Задание 2.3: Непрерывное рисование (5 мин)

Сейчас мы можем рисовать только кликами. Но хочется зажать кнопку мыши и водить курсором, как в Paint!

**Проблема:** Нужно отслеживать, зажата ли кнопка мыши.

**Решение:** Используем флаги состояния.

**Скопируйте в новую ячейку:**

```python
# Создаём новую сетку
grid = Grid(WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT)

# TODO: Флаги состояния мыши
left_mouse_pressed = False  # Зажата ли левая кнопка?
last_drawn_cell = None      # Последняя нарисованная клетка

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
                # TODO: Установите флаг, что кнопка зажата
                left_mouse_pressed = ___
                # TODO: Сбросьте last_drawn_cell
                last_drawn_cell = ___

        # Отпускание кнопки мыши
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Левая кнопка
                # TODO: Сбросьте флаг
                left_mouse_pressed = ___
                last_drawn_cell = None

    # TODO: Рисование при движении мыши (вне обработки событий!)
    # Получаем текущую позицию мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Если левая кнопка зажата
    if left_mouse_pressed:
        # Получаем клетку под курсором
        cell = grid.get_cell_at_position(mouse_x, mouse_y)

        if cell is not None:
            col, row = cell

            # TODO: Рисуем только если это НОВАЯ клетка
            # Это предотвращает многократное заполнение одной клетки
            if cell != ___:
                grid.fill_cell(col, row)
                # TODO: Запоминаем последнюю нарисованную клетку
                last_drawn_cell = ___

    # Рисуем сетку
    draw_grid(screen, grid)

    # Обновляем экран
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

**Проверка:**
- Зажмите левую кнопку мыши и водите курсором
- Должны рисоваться непрерывные линии!
- Отпустите кнопку - рисование прекращается

**Отлично работает! 🎨**

---

## 🎓 Что мы узнали?

1. ✅ **Отрисовка сетки** - линии и заполненные клетки
2. ✅ **Обработка событий мыши** - MOUSEBUTTONDOWN, MOUSEBUTTONUP
3. ✅ **Состояние мыши** - флаги для отслеживания зажатых кнопок
4. ✅ **Предотвращение дубликатов** - рисуем только новые клетки

---

## 🚀 Следующий шаг

Теперь мы умеем рисовать! Но если ошибётся, как стереть?

**Дальше:** Добавим стирание правой кнопкой мыши и подсветку клетки под курсором!
