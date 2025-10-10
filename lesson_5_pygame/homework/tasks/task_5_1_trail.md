# 🌟 Задание 5.1: Траектория движения робота (25 мин)

**Повторяем:** Списки, деки, прозрачность, продвинутая графика.

Сейчас робот движется, но не видно, где он был. Добавим след — линию, которая показывает траекторию движения!

---

## 🧠 Теория: Хранение истории движения

### Как сохранить траекторию?

Нужно **запоминать** все позиции, где был робот:

```python
trail = []  # Пустой список

# Каждый кадр добавляем текущую позицию
trail.append((robot_x, robot_y))
```

### Проблема: бесконечный рост

Если добавлять каждый кадр (60 раз в секунду), через минуту будет 3600 точек!

**Решения:**
1. Ограничить длину списка (хранить только последние N точек)
2. Добавлять не каждый кадр, а через интервал

### Deque — очередь с ограничением

```python
from collections import deque

trail = deque(maxlen=100)  # Максимум 100 точек
trail.append((x, y))  # Автоматически удаляет старые
```

**Преимущества deque:**
- Автоматически удаляет старые элементы
- Быстрее обычного списка для добавления/удаления
- `maxlen` — встроенное ограничение размера

### Рисование линии по точкам

```python
pygame.draw.lines(screen, color, closed, points, width)
```

Параметры:
- `screen` — где рисовать
- `color` — цвет линии
- `closed` — замкнутая линия? (False для траектории)
- `points` — список точек `[(x1, y1), (x2, y2), ...]`
- `width` — толщина линии

**Важно:** Нужно минимум 2 точки!

---

## 📝 Задача

Создайте систему траектории:
1. Робот оставляет след при движении
2. След ограничен 150 точками (старые точки исчезают)
3. Клавиша **C** (Clear) очищает траекторию
4. ⭐ **Бонус:** Плавное затухание следа (старые участки бледнее)

---

## 🔧 Пошаговая инструкция

### Шаг 1: Импорт deque
```python
from collections import deque
```

Добавьте в начало файла, после `import math`.

---

### Шаг 2: Создайте deque для траектории
```python
trail = deque(maxlen=150)
```

Пишется **до** игрового цикла, вместе с другими переменными.

**Почему 150?**
- При 60 FPS это 2.5 секунды истории
- Достаточно длинный след, но не перегружает
- Можно экспериментировать: 50 (короткий), 300 (длинный)

---

### Шаг 3: Сохранение текущей позиции
```python
# В игровом цикле, ПОСЛЕ изменения координат
trail.append((robot_x, robot_y))
```

**Где писать:** После всех `if keys[pygame.K_w]:` и поворотов, но до преобразования координат.

**Почему именно там?**
- Нужно сохранять позицию ПОСЛЕ движения
- Сохраняем математические координаты (не экранные!)

---

### Шаг 4: Функция для рисования траектории
```python
def draw_trail(screen, trail):
    """Рисует траекторию движения"""
    if len(trail) < 2:
        return  # Нужно минимум 2 точки для линии
```

Создайте новую функцию после `draw_robot` и до игрового цикла.

**Проверка длины важна!** `pygame.draw.lines()` упадет с ошибкой, если точек меньше 2.

---

### Шаг 5: Преобразование координат для траектории
```python
    screen_points = []
    for x, y in trail:
        screen_x = int(x + WIDTH/2)
        screen_y = int(HEIGHT/2 - y)
        screen_points.append((screen_x, screen_y))
```

Проходим по всем точкам траектории и преобразуем математические координаты в экранные.

**Важно:** Преобразуем ВСЕ точки, не только последнюю!

---

### Шаг 6: Рисование линии
```python
    if len(screen_points) >= 2:
        pygame.draw.lines(screen, (100, 100, 255), False, screen_points, 2)
```

Параметры:
- `(100, 100, 255)` — светло-синий цвет
- `False` — не замыкать линию
- `screen_points` — преобразованные точки
- `2` — толщина 2 пикселя

---

### Шаг 7: Вызов функции в цикле
```python
screen.fill(WHITE)

# СНАЧАЛА траектория (внизу)
draw_trail(screen, trail)

# ПОТОМ робот (сверху)
draw_robot(screen, robot_x, robot_y, robot_direction, 15)
```

**Порядок важен!** След должен быть под роботом, не наоборот.

---

### Шаг 8: Очистка траектории клавишей C
```python
if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_r:
        robot_x = 0
        robot_y = 0
        robot_direction = 0
    
    if event.key == pygame.K_c:
        trail.clear()  # Очистить всю траекторию
```

`clear()` — метод deque, удаляет все элементы.

---

### Шаг 9: Обновить подсказки
```python
info_texts = [
    f"Позиция: ({x:.1f}, {y:.1f})",
    f"Направление: {direction:.1f}°",
    f"След: {len(trail)} точек",  # Новая строка!
    "",
    "Управление:",
    "W A S D - движение",
    "Q E - поворот",
    "R - сброс в центр",
    "C - очистить след"  # Новая строка!
]
```

Функцию `draw_info` нужно обновить, чтобы принимать `trail`:
```python
def draw_info(screen, x, y, direction, trail, font):
```

И вызов:
```python
draw_info(screen, robot_x, robot_y, robot_direction, trail, font)
```

---

## 🚀 Ячейка для вашего кода

```python
import pygame
import math
from collections import deque  # TODO: Не забудьте импорт!

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)

font = pygame.font.Font(None, 24)

# TODO: Обновите draw_info - добавьте параметр trail
def draw_info(screen, x, y, direction, trail, font):
    info_texts = [
        f"Позиция: ({x:.1f}, {y:.1f})",
        f"Направление: {direction:.1f}°",
        f"След: {len(trail)} точек",
        "",
        "Управление:",
        "W A S D - движение",
        "Q E - поворот",
        "R - сброс в центр",
        "C - очистить след"
    ]
    
    y_offset = 10
    for text in info_texts:
        surface = font.render(text, True, BLACK)
        screen.blit(surface, (10, y_offset))
        y_offset += 25

def draw_robot(screen, x, y, direction, radius):
    # ... ваш код из задания 4.2 ...

# TODO: Создайте функцию draw_trail(screen, trail)
def draw_trail(screen, trail):
    """Рисует траекторию движения"""
    # TODO: Проверьте, что len(trail) >= 2
    
    # TODO: Преобразуйте все точки в экранные координаты
    screen_points = []
    # for x, y in trail:
    #     ...
    
    # TODO: Нарисуйте линии
    # if len(screen_points) >= 2:
    #     pygame.draw.lines(...)

robot_x = 0
robot_y = 0
robot_direction = 0
move_speed = 3
turn_speed = 3

# TODO: Создайте deque для траектории
trail = deque(maxlen=150)

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
            
            # TODO: Добавьте обработку клавиши C
            # if event.key == pygame.K_c:
            #     trail.clear()
    
    keys = pygame.key.get_pressed()
    
    # Повороты
    if keys[pygame.K_q]:
        robot_direction += turn_speed
        robot_direction %= 360
    if keys[pygame.K_e]:
        robot_direction -= turn_speed
        robot_direction %= 360
    
    # Движение
    if keys[pygame.K_w]:
        angle = math.radians(robot_direction)
        robot_x += math.cos(angle) * move_speed
        robot_y += math.sin(angle) * move_speed
    
    if keys[pygame.K_s]:
        angle = math.radians(robot_direction)
        robot_x -= math.cos(angle) * move_speed
        robot_y -= math.sin(angle) * move_speed
    
    if keys[pygame.K_a]:
        angle = math.radians(robot_direction + 90)
        robot_x += math.cos(angle) * move_speed
        robot_y += math.sin(angle) * move_speed
    
    if keys[pygame.K_d]:
        angle = math.radians(robot_direction - 90)
        robot_x += math.cos(angle) * move_speed
        robot_y += math.sin(angle) * move_speed
    
    # TODO: Сохраните текущую позицию в trail
    # trail.append((robot_x, robot_y))
    
    screen.fill(WHITE)
    
    # TODO: Нарисуйте траекторию ПЕРЕД роботом
    # draw_trail(screen, trail)
    
    draw_robot(screen, robot_x, robot_y, robot_direction, 15)
    draw_info(screen, robot_x, robot_y, robot_direction, trail, font)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

---

## ✅ Ячейка для проверки

Вы должны увидеть:
- Синюю линию, следующую за роботом
- Линия ограничена длиной (старые участки исчезают)
- Счетчик точек в интерфейсе (обновляется)
- Клавиша C полностью очищает след
- При сбросе R траектория НЕ очищается (робот телепортируется)

**Эксперименты:**
1. Поездите по кругу → увидите круглый след
2. Подождите, не двигаясь → старые точки исчезнут, останется только текущая
3. Измените `maxlen=50` → короткий след
4. Измените `maxlen=300` → длинный след

---

## ⭐ Задание со звездочкой: Затухание следа

Сейчас весь след одинаковый. Сделаем так, чтобы старые участки были **бледнее**!

### Теория: Альфа-канал и Surface

Для прозрачности нужно:
1. Создать временную Surface
2. Установить альфа-канал
3. Рисовать на ней
4. Blit на основной экран

```python
temp_surface = pygame.Surface((WIDTH, HEIGHT))
temp_surface.set_colorkey((0, 0, 0))  # Черный = прозрачный
temp_surface.set_alpha(128)  # Полупрозрачность
```

### Способ 1: Несколько сегментов с разной прозрачностью

Разделим траекторию на сегменты:
- Новейший 20% → непрозрачный
- Средний 40% → полупрозрачный
- Старый 40% → очень бледный

```python
def draw_trail(screen, trail):
    if len(trail) < 2:
        return
    
    screen_points = []
    for x, y in trail:
        screen_x = int(x + WIDTH/2)
        screen_y = int(HEIGHT/2 - y)
        screen_points.append((screen_x, screen_y))
    
    if len(screen_points) < 2:
        return
    
    total = len(screen_points)
    
    # Делим на 3 сегмента
    third = total // 3
    
    # Старая часть (0 - 1/3) - очень бледная
    if third >= 2:
        segment = screen_points[:third]
        pygame.draw.lines(screen, (180, 180, 230), False, segment, 1)
    
    # Средняя часть (1/3 - 2/3) - средняя
    if total > third * 2 and third >= 1:
        segment = screen_points[third:third*2]
        if len(segment) >= 2:
            pygame.draw.lines(screen, (130, 130, 240), False, segment, 2)
    
    # Новая часть (2/3 - конец) - яркая
    if total > third * 2:
        segment = screen_points[third*2:]
        if len(segment) >= 2:
            pygame.draw.lines(screen, (80, 80, 255), False, segment, 3)
```

### Способ 2: Плавное затухание (сложнее, но красивее)

Рисуем много маленьких линий с разной прозрачностью:

```python
def draw_trail_fade(screen, trail):
    """Рисует траекторию с плавным затуханием"""
    if len(trail) < 2:
        return
    
    screen_points = []
    for x, y in trail:
        screen_x = int(x + WIDTH/2)
        screen_y = int(HEIGHT/2 - y)
        screen_points.append((screen_x, screen_y))
    
    if len(screen_points) < 2:
        return
    
    # Рисуем отдельные сегменты с разной яркостью
    total = len(screen_points)
    
    for i in range(total - 1):
        # Коэффициент затухания: от 0 (старое) до 1 (новое)
        fade = i / max(total - 1, 1)
        
        # Цвет: от бледного (200) до яркого (50)
        brightness = int(200 - fade * 150)  # 200 -> 50
        color = (brightness, brightness, 255)
        
        # Толщина: от 1 до 3
        width = 1 + int(fade * 2)
        
        # Рисуем один сегмент
        start = screen_points[i]
        end = screen_points[i + 1]
        pygame.draw.line(screen, color, start, end, width)
```

### Инструкция для звездочки

1. Замените функцию `draw_trail` на одну из версий выше
2. Выберите:
   - **Способ 1** — проще, 3 уровня прозрачности
   - **Способ 2** — сложнее, плавное затухание
3. Поэкспериментируйте с цветами и толщиной

---

## 💡 Дополнительные улучшения

### 1. След только при движении
```python
# Сохраняем позицию только если были изменения
if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
    trail.append((robot_x, robot_y))
```

### 2. Разные цвета для разных скоростей
```python
# Вычисляем скорость движения
if len(trail) >= 2:
    prev_x, prev_y = trail[-2]
    dist = math.sqrt((robot_x - prev_x)**2 + (robot_y - prev_y)**2)
    # Меняем цвет в зависимости от dist
```

### 3. Пунктирная линия
```python
# Добавляем только каждую 5-ю точку
if len(trail) % 5 == 0:
    trail.append((robot_x, robot_y))
```

### 4. След исчезает при сбросе R
```python
if event.key == pygame.K_r:
    robot_x = 0
    robot_y = 0
    robot_direction = 0
    trail.clear()  # Добавить эту строку
```

---

## 🎨 Красивые эффекты

### Градиентный след (Rainbow trail)
```python
def draw_trail_rainbow(screen, trail):
    # ... преобразование координат ...
    
    for i in range(len(screen_points) - 1):
        # HSV → RGB для радужного эффекта
        hue = (i / len(screen_points)) * 360
        # Упрощенно: используем разные цвета
        colors = [
            (255, 100, 100),  # Красный
            (255, 200, 100),  # Оранжевый
            (255, 255, 100),  # Желтый
            (100, 255, 100),  # Зеленый
            (100, 100, 255),  # Синий
        ]
        color_idx = (i * len(colors)) // len(screen_points)
        color = colors[color_idx]
        
        pygame.draw.line(screen, color, screen_points[i], screen_points[i+1], 2)
```

### Частицы вместо линии
```python
# Вместо линии — рисуем маленькие круги
for i, (screen_x, screen_y) in enumerate(screen_points):
    fade = i / max(len(screen_points), 1)
    radius = 1 + int(fade * 3)
    pygame.draw.circle(screen, (100, 100, 255), (screen_x, screen_y), radius)
```

---

## 🏆 Итоги

**Что вы изучили:**
✅ `collections.deque` для ограниченной истории  
✅ `pygame.draw.lines()` для полилиний  
✅ Преобразование списка координат  
✅ Управление памятью (ограничение размера)  
✅ ⭐ Затухание и плавные переходы  

**Сложность:**
- Базовая версия: средняя (⭐⭐⭐)
- Со звездочкой: высокая (⭐⭐⭐⭐)

---

## 🔍 Отладка

**След не рисуется?**
- Проверьте `len(trail) >= 2`
- Выведите `print(len(trail))` — добавляются ли точки?
- Проверьте порядок вызовов: сначала trail, потом robot

**След прерывистый?**
- Возможно, `trail.append()` вызывается не каждый кадр
- Переместите append в конец цикла, без условий

**След странной формы?**
- Проверьте преобразование координат (математические → экранные)
- Убедитесь, что используете правильные формулы

**Затухание не работает?**
- Убедитесь, что рисуете сегменты от старых к новым
- Проверьте вычисление `fade` (должно быть от 0 до 1)

