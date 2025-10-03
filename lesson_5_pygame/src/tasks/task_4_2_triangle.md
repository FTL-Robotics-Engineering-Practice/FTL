# 🔺 Задание 4.2: Треугольник направления (30 мин)

**Повторяем:** Тригонометрия, рисование многоугольников, функции.

Сейчас робот — просто круг без направления. Нарисуем треугольник внутри круга, который показывает, куда робот смотрит!

---

## 🧠 Теория: Рисование треугольника с поворотом

### Как нарисовать треугольник?

```python
pygame.draw.polygon(screen, color, points)
```

`points` — список из 3 точек (вершин треугольника):
```python
points = [(x1, y1), (x2, y2), (x3, y3)]
```

### Как повернуть треугольник?

Нужно **вычислить координаты** трех вершин, используя тригонометрию.

**Треугольник имеет:**
1. **Вершину** (острый конец) — показывает направление
2. **Две задние точки** (основание)

```
       * (вершина)
      / \
     /   \
    *-----* (основание)
```

### Математика поворота точки

Чтобы повернуть точку вокруг центра на угол α:

```python
angle = math.radians(direction)

new_x = center_x + distance * math.cos(angle)
new_y = center_y - distance * math.sin(angle)
```

**Почему минус перед sin?**
В Pygame Y растет вниз, а мы хотим, чтобы положительные углы были вверх.

---

## 📝 Задача

Создайте функцию `draw_robot(screen, x, y, direction, radius)`, которая:
1. Рисует синий круг (тело робота)
2. Рисует белый треугольник внутри (направление)
3. Треугольник поворачивается в соответствии с `direction`

---

## 🔧 Пошаговая инструкция

### Шаг 1: Создайте функцию
```python
def draw_robot(screen, x, y, direction, radius):
    """Рисует робота с направлением"""
```

Параметры:
- `x, y` — математические координаты
- `direction` — направление в градусах
- `radius` — радиус круга

Пишется **до** игрового цикла, после функции `draw_info`.

---

### Шаг 2: Преобразование координат
```python
    screen_x = int(x + WIDTH/2)
    screen_y = int(HEIGHT/2 - y)
```

Преобразуем математические координаты в экранные (внутри функции!).

---

### Шаг 3: Рисование круга (тела)
```python
    pygame.draw.circle(screen, BLUE, (screen_x, screen_y), radius)
```

Тело робота — синий круг.

---

### Шаг 4: Подготовка угла для тригонометрии
```python
    angle = math.radians(direction)
```

Переводим градусы в радианы (для функций sin/cos).

**Не забудьте импорт в начале файла:**
```python
import math
```

---

### Шаг 5: Вершина треугольника (острый конец)

Вершина находится на расстоянии `radius * 1.5` от центра:

```python
    tip_x = screen_x + math.cos(angle) * radius * 1.5
    tip_y = screen_y - math.sin(angle) * radius * 1.5
```

**Почему 1.5?**
- Радиус круга = `radius`
- Хотим, чтобы острие выходило немного за круг
- `1.5 * radius` — хорошая длина

**Почему минус перед sin?**
- `math.sin()` положителен для углов вверх
- Но в Pygame Y растет вниз
- Минус инвертирует это

---

### Шаг 6: Левая задняя точка

Задние точки расположены под углами ±140° относительно направления:

```python
    left_angle = angle + math.radians(140)
    left_x = screen_x + math.cos(left_angle) * radius * 0.8
    left_y = screen_y - math.sin(left_angle) * radius * 0.8
```

**Почему +140°?**
- Треугольник имеет углы примерно 100° в вершине и 40° в основании
- 140° отклонение влево от направления

**Почему 0.8?**
- Короче вершины (`0.8 < 1.5`)
- Задние точки ближе к центру

---

### Шаг 7: Правая задняя точка
```python
    right_angle = angle - math.radians(140)
    right_x = screen_x + math.cos(right_angle) * radius * 0.8
    right_y = screen_y - math.sin(right_angle) * radius * 0.8
```

Симметрично левой, но минус (отклонение вправо).

---

### Шаг 8: Рисование треугольника
```python
    pygame.draw.polygon(screen, WHITE, [
        (tip_x, tip_y),
        (left_x, left_y),
        (right_x, right_y)
    ])
```

Рисуем белый треугольник через три точки.

---

### Шаг 9: Контур круга
```python
    pygame.draw.circle(screen, BLACK, (screen_x, screen_y), radius, 2)
```

Черный контур толщиной 2 пикселя. Рисуется **поверх** всего (последним).

Параметр `2` в конце — это толщина линии. Без него круг был бы залит.

---

### Шаг 10: Вызов функции в цикле

**Удалите** старую строку:
```python
# pygame.draw.circle(screen, BLUE, (screen_x, screen_y), 15)  ← УДАЛИТЬ
```

**Добавьте** новый вызов:
```python
draw_robot(screen, robot_x, robot_y, robot_direction, 15)
```

---

## 🚀 Ячейка для вашего кода

```python
import pygame
import math  # Не забудьте импорт!

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)

font = pygame.font.Font(None, 24)

def draw_info(screen, x, y, direction, font):
    # ... ваш код из предыдущего задания ...

# TODO: Создайте функцию draw_robot(screen, x, y, direction, radius)
def draw_robot(screen, x, y, direction, radius):
    """Рисует робота с направлением"""
    # TODO: Преобразуйте координаты
    
    # TODO: Нарисуйте круг
    
    # TODO: Вычислите angle = math.radians(direction)
    
    # TODO: Вычислите координаты вершины треугольника
    
    # TODO: Вычислите координаты левой задней точки
    
    # TODO: Вычислите координаты правой задней точки
    
    # TODO: Нарисуйте треугольник через pygame.draw.polygon()
    
    # TODO: Нарисуйте контур круга

robot_x = 0
robot_y = 0
robot_direction = 0
move_speed = 3

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                robot_x = 0
                robot_y = 0
                robot_direction = 0
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w]:
        robot_y += move_speed
    if keys[pygame.K_s]:
        robot_y -= move_speed
    if keys[pygame.K_a]:
        robot_x -= move_speed
    if keys[pygame.K_d]:
        robot_x += move_speed
    
    screen.fill(WHITE)
    
    # TODO: Вызовите draw_robot() вместо draw.circle()
    
    draw_info(screen, robot_x, robot_y, robot_direction, font)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

---

## ✅ Ячейка для проверки

Вы должны увидеть:
- Синий круг с белым треугольником внутри
- Треугольник указывает **вправо** (направление = 0°)
- Черный контур вокруг круга

**Проверка направления:**
Пока робот всегда смотрит вправо. Для проверки **временно** измените:
```python
robot_direction = 90  # Должен смотреть вверх
robot_direction = 180  # Должен смотреть влево
robot_direction = 270  # Должен смотреть вниз
```

После проверки верните `robot_direction = 0`.

---

## 💡 Визуальная отладка

**Треугольник кривой?**

Нарисуйте точки для отладки:
```python
    # После вычисления координат, перед polygon:
    pygame.draw.circle(screen, RED, (int(tip_x), int(tip_y)), 3)
    pygame.draw.circle(screen, GREEN, (int(left_x), int(left_y)), 3)
    pygame.draw.circle(screen, GREEN, (int(right_x), int(right_y)), 3)
```

Вы увидите, где находятся вершины треугольника.

---

## 🎨 Эксперименты с формой

Измените параметры для других форм:

1. **Длинный острый треугольник:**
   ```python
   tip_x = screen_x + math.cos(angle) * radius * 2.0  # Длиннее
   left_angle = angle + math.radians(160)  # Уже
   ```

2. **Короткий широкий треугольник:**
   ```python
   tip_x = screen_x + math.cos(angle) * radius * 1.2  # Короче
   left_angle = angle + math.radians(120)  # Шире
   ```

3. **Стрелка вместо треугольника:**
   Используйте 4 точки вместо 3

---

## 🧮 Почему эти углы?

Треугольник имеет:
- Угол при вершине: 360° - 140° - 140° = 80°
- Углы при основании: по 50° каждый

Это красивая форма, похожая на стрелку!

Можете экспериментировать с углами 130°, 150° для других форм.