# Задание 5: Отображение целевого угла и ошибки

## Описание

Нужно дополнить информационную панель, чтобы выводить:
1. Угол от робота до препятствий
2. Целевой угол (куда робот хочет повернуть)
3. Ошибку (разницу между текущим и целевым углом)

Это поможет визуально отслеживать работу П-регулятора.

## Что нужно добавить

В методе `draw_info_panel()` класса `Renderer` нужно добавить вывод трёх значений:

```
УГОЛ ДО ПРЕПЯТСТВИЙ:
{angle_diff}°

ЦЕЛЬ:
{target_angle}°

ОШИБКА:
{error}°
```

## Где вставлять код

В файле `renderer.py`, в методе `draw_info_panel()`, после вывода угла робота и **перед** выводом скоростей.

Найдите место:

```python
# Угол
angle_deg = math.degrees(robot.angle) % 360
draw_text("УГОЛ:", color=self.YELLOW)
draw_text(f"{angle_deg:.1f}°")
draw_text("")  # Пустая строка

# TODO: Вывести информацию о целевом угле и ошибке (если есть sight и препятствия)

# Скорости
draw_text("СКОРОСТИ:", color=self.YELLOW)
# ...
```

## Доступные переменные

В методе `draw_info_panel()` доступны:
- `robot` - объект Robot
- `sight` - объект Sight (может быть None)
- `brain` - объект Brain
- Функция `draw_text(text, color, font)` для вывода

## Логика решения

### 1. Проверить наличие препятствий

```python
if sight is not None and sight.center_of_mass:
    # Есть препятствия - можно вычислять углы
```

### 2. Получить координаты центра масс

```python
cx, cy = sight.center_of_mass
```

### 3. Вычислить вектор от робота к препятствию

```python
dx = cx - robot.x
dy = cy - robot.y
```

### 4. Вычислить угол к препятствию

```python
target_angle = math.atan2(dy, dx)
```

### 5. Вычислить разницу углов

```python
angle_diff = target_angle - robot.angle
```

### 6. Нормализовать в диапазон [-π, π]

```python
while angle_diff > math.pi:
    angle_diff -= 2 * math.pi
while angle_diff < -math.pi:
    angle_diff += 2 * math.pi
```

### 7. Преобразовать в градусы

```python
angle_diff_deg = math.degrees(angle_diff)
```

### 8. Получить целевой угол из brain

```python
target_angle_deg = math.degrees(brain.target_angle)
```

### 9. Вычислить ошибку

```python
error = angle_diff_deg - target_angle_deg
```

### 10. Вывести информацию

```python
draw_text("УГОЛ ДО ПРЕПЯТСТВИЙ:", color=self.YELLOW)
draw_text(f"{angle_diff_deg:.1f}°")

draw_text("ЦЕЛЬ:", color=self.YELLOW)
draw_text(f"{target_angle_deg:.1f}°")

draw_text("ОШИБКА:", color=self.YELLOW)
draw_text(f"{error:.1f}°")

draw_text("")  # Пустая строка
```

## Изменение сигнатуры метода

Обратите внимание, что метод `draw_info_panel()` теперь принимает параметр `brain`:

```python
def draw_info_panel(self, robot, mode_manager, brain, grid=None, points=None, sight=None):
```

Этот параметр нужно добавить везде, где вызывается этот метод (в `main.py`).

## Полная структура кода

```python
def draw_info_panel(self, robot, mode_manager, brain, grid=None, points=None, sight=None):
    """Отрисовать информационную панель"""
    
    # ... код фона и draw_text ...
    
    # Режим
    mode_name = mode_manager.get_mode_name()
    draw_text(mode_name, color=self.YELLOW)
    draw_text("")

    # Позиция
    draw_text("ПОЗИЦИЯ:", color=self.YELLOW)
    draw_text(f"X: {robot.x:.1f} px")
    draw_text(f"Y: {robot.y:.1f} px")
    draw_text("")

    # Угол
    angle_deg = math.degrees(robot.angle) % 360
    draw_text("УГОЛ:", color=self.YELLOW)
    draw_text(f"{angle_deg:.1f}°")
    draw_text("")

    # TODO: Угол до препятствий, целевой угол и ошибка
    # if sight is not None and sight.center_of_mass:
    #     cx, cy = sight.center_of_mass
    #     dx = cx - robot.x
    #     dy = cy - robot.y
    #     target_angle = math.atan2(dy, dx)
    #     angle_diff = target_angle - robot.angle
    #     
    #     # Нормализовать
    #     while angle_diff > math.pi:
    #         angle_diff -= 2 * math.pi
    #     while angle_diff < -math.pi:
    #         angle_diff += 2 * math.pi
    #     
    #     angle_diff_deg = math.degrees(angle_diff)
    #     
    #     draw_text("УГОЛ ДО ПРЕПЯТСТВИЙ:", color=self.YELLOW)
    #     draw_text(f"{angle_diff_deg:.1f}°")
    #     draw_text("ЦЕЛЬ:", color=self.YELLOW)
    #     draw_text(f"{math.degrees(brain.target_angle):.1f}°")
    #     draw_text("ОШИБКА:", color=self.YELLOW)
    #     error = angle_diff_deg - math.degrees(brain.target_angle)
    #     draw_text(f"{error:.1f}°")
    #     draw_text("")

    # Скорости
    draw_text("СКОРОСТИ:", color=self.YELLOW)
    draw_text(f"Линейная: {robot.linear_velocity:.1f}")
    draw_text(f"Угловая: {robot.angular_velocity:.2f}")
    draw_text("")
    
    # ... остальной код ...
```

## Проверка

После реализации:
1. Запустите программу: `python code/main.py`
2. Нарисуйте препятствия
3. Переключитесь в режим робота (TAB)
4. В панели должны появиться три новых поля:
   - **УГОЛ ДО ПРЕПЯТСТВИЙ**: текущий угол к центру масс
   - **ЦЕЛЬ**: куда робот хочет повернуть (±90°)
   - **ОШИБКА**: насколько робот отклонился от цели

## Интерпретация значений

### Угол до препятствий:
- **+90°**: препятствие ровно слева
- **-90°**: препятствие ровно справа
- **0°**: препятствие прямо впереди
- **±180°**: препятствие позади

### Цель:
- **+90°**: робот хочет повернуть налево
- **-90°**: робот хочет повернуть направо

### Ошибка:
- **> 0**: робот перекрутил (повернул слишком сильно)
- **< 0**: робот недокрутил (нужно еще повернуть)
- **≈ 0**: цель достигнута, препятствие сбоку

## Наблюдение за работой регулятора

Понаблюдайте, как меняются значения при работе робота:

1. Робот видит препятствие (угол до препятствий ≠ 0)
2. Определяет цель (±90°)
3. Начинает поворачивать (ошибка уменьшается)
4. Достигает цели (ошибка → 0, препятствие сбоку)
5. Движется вперед, огибая препятствие

Это и есть работа П-регулятора в реальном времени!
