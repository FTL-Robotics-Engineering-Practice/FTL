# Задание 4: Отрисовка зоны видимости

## Описание

Нужно реализовать методы `draw_sight_zone()` и `draw_sight_line()` в классе `Renderer` для визуализации области видения робота.

## Часть 1: draw_sight_zone()

Метод должен:
1. Рисовать все видимые клетки полупрозрачным синим
2. Клетки с препятствиями - более яркими и непрозрачными
3. Пустые клетки - более тусклыми и прозрачными
4. Рисовать центр масс препятствий красной точкой

### Доступные переменные:
- `sight` - объект Sight
- `grid` - объект Grid
- `self.screen` - экран pygame

### Логика решения:

1. **Перебрать все видимые клетки:**
   - `for col, row in sight.visible_cells:`

2. **Для каждой клетки:**
   
   a) **Вычислить позицию:**
   - `x = col * grid.cell_width + grid.offset_x`
   - `y = row * grid.cell_height`
   
   b) **Определить цвет и прозрачность:**
   - Если клетка в `sight.obstacle_cells`:
     - `color = (100, 150, 255)` - светло-синий
     - `alpha = 150` - более непрозрачный
   - Иначе:
     - `color = (70, 70, 150)` - тусклый синий
     - `alpha = 30` - прозрачный
   
   c) **Нарисовать полупрозрачный квадрат:**
   ```python
   surface = pygame.Surface((grid.cell_width, grid.cell_height))
   surface.set_alpha(alpha)
   surface.fill(color)
   self.screen.blit(surface, (x, y))
   ```

3. **Нарисовать центр масс:**
   - Если `sight.center_of_mass` не None:
     - Получить координаты `cx, cy = sight.center_of_mass`
     - Нарисовать круг: `pygame.draw.circle(self.screen, (255, 0, 0), (int(cx), int(cy)), 5)`

## Часть 2: draw_sight_line()

Метод должен рисовать линию от робота до центра масс препятствий.

### Доступные переменные:
- `robot` - объект Robot
- `sight` - объект Sight
- `self.screen` - экран pygame

### Логика решения:

1. **Проверить наличие центра масс:**
   - Если `sight.center_of_mass`:

2. **Получить координаты:**
   - `cx, cy = sight.center_of_mass`

3. **Нарисовать линию:**
   ```python
   pygame.draw.line(
       self.screen,
       (255, 0, 0),  # Красный
       (int(robot.x), int(robot.y)),
       (int(cx), int(cy)),
       2  # Толщина линии
   )
   ```

## Структура кода

```python
def draw_sight_zone(self, sight, grid):
    # TODO: Рисуем все видимые клетки
    for col, row in ...:
        x = ...
        y = ...

        # TODO: Определить цвет
        if (col, row) in sight.obstacle_cells:
            color = ...
            alpha = ...
        else:
            color = ...
            alpha = ...

        # Полупрозрачная заливка
        surface = pygame.Surface((grid.cell_width, grid.cell_height))
        surface.set_alpha(alpha)
        surface.fill(color)
        self.screen.blit(surface, (x, y))

    # TODO: Рисуем центр масс
    if ...:
        cx, cy = ...
        pygame.draw.circle(...)

def draw_sight_line(self, robot, sight):
    # TODO: Рисуем линию до центра масс
    if ...:
        cx, cy = ...
        pygame.draw.line(...)
```

## Проверка

Запустите программу. Вы должны увидеть:
- Голубую полупрозрачную зону видимости вокруг робота
- Препятствия в зоне выделены более ярким синим
- Красная точка - центр масс препятствий
- Красная линия от робота до центра масс
