# 🧭 Задание 4.1: Добавить направление (10 мин)

**Повторяем:** Переменные, обновление функций.

Сейчас робот — просто круг. У него нет "лица" или направления взгляда. Давайте добавим переменную для направления и начнем отображать её!

---

## 🧠 Теория: Направление в градусах

### Система измерения углов

В нашей программе направление измеряется в **градусах**:

```
        90° (север, вверх)
         |
         |
180° ----+---- 0° (восток, вправо)
         |
         |
        270° (юг, вниз)
```

**Важно:**
- 0° = направление вправо (восток)
- 90° = направление вверх (север)
- 180° = направление влево (запад)
- 270° = направление вниз (юг)

Углы увеличиваются **против часовой стрелки** (математическая конвенция).

### Связь с классом Robot

Вспомните из Занятия 4:
```python
robot.direction = 0   # направление вправо
robot.direction = 90  # направление вверх
```

Мы используем ту же систему!

---

## 📝 Задача

Добавьте переменную `robot_direction` и выводите её значение в интерфейсе.

---

## 🔧 Пошаговая инструкция

### Шаг 1: Создайте переменную направления
```python
robot_direction = 0
```

Начальное направление: 0 градусов (вправо).

Пишется **до** игрового цикла, вместе с `robot_x` и `robot_y`.

---

### Шаг 2: Обнуление направления при сбросе
```python
if event.key == pygame.K_r:
    robot_x = 0
    robot_y = 0
    robot_direction = 0  # Добавить эту строку!
```

Когда сбрасываем позицию, сбрасываем и направление.

---

### Шаг 3: Обновите функцию draw_info

Изменим сигнатуру функции:
```python
def draw_info(screen, x, y, direction, font):
```

Добавили параметр `direction`.

---

### Шаг 4: Добавьте направление в список текста
```python
    info_texts = [
        f"Позиция: ({x:.1f}, {y:.1f})",
        f"Направление: {direction:.1f}°",  # Новая строка!
        "",
        "Управление:",
        "W A S D - движение",
        "R - сброс в центр"
    ]
```

Символ градуса: `°` (можно скопировать или написать просто "град").

**Форматирование:**
- `{direction:.1f}` — показать с 1 знаком после запятой
- `°` — символ градуса

---

### Шаг 5: Обновите вызов функции
```python
draw_info(screen, robot_x, robot_y, robot_direction, font)
```

Теперь передаем 4 параметра вместо 3.

---

## 🚀 Ячейка для вашего кода

```python
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)

font = pygame.font.Font(None, 24)

# TODO: Обновите функцию - добавьте параметр direction
def draw_info(screen, x, y, font):
    info_texts = [
        f"Позиция: ({x:.1f}, {y:.1f})",
        # TODO: Добавьте строку с направлением
        "",
        "Управление:",
        "W A S D - движение",
        "R - сброс в центр"
    ]
    
    y_offset = 10
    for text in info_texts:
        surface = font.render(text, True, BLACK)
        screen.blit(surface, (10, y_offset))
        y_offset += 25

robot_x = 0
robot_y = 0
# TODO: Добавьте robot_direction = 0
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
                # TODO: Сбросьте robot_direction
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w]:
        robot_y += move_speed
    if keys[pygame.K_s]:
        robot_y -= move_speed
    if keys[pygame.K_a]:
        robot_x -= move_speed
    if keys[pygame.K_d]:
        robot_x += move_speed
    
    screen_x = int(robot_x + WIDTH/2)
    screen_y = int(HEIGHT/2 - robot_y)
    
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLUE, (screen_x, screen_y), 15)
    
    # TODO: Обновите вызов - передайте robot_direction
    draw_info(screen, robot_x, robot_y, font)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

---

## ✅ Ячейка для проверки

Вы должны увидеть:
- Строку "Направление: 0.0°" под позицией
- При нажатии R направление сбрасывается в 0

Пока робот всегда смотрит вправо (0°). В следующих заданиях мы добавим поворот!

---

## 💡 Зачем это нужно?

Сейчас `robot_direction` ещё не влияет на движение. Но:

1. **В следующем задании** мы нарисуем треугольник, показывающий направление
2. **В задании после** мы изменим управление: W будет двигать **по направлению**, а не всегда вверх
3. Это подготовка к интеграции с классом `Robot` из Занятия 4

---

## 🔍 Градусы и радианы

В Pygame и математических функциях часто используют **радианы**:
- 360° = 2π радиан
- 180° = π радиан
- 90° = π/2 радиан

Преобразование:
```python
import math

radians = math.radians(degrees)  # градусы → радианы
degrees = math.degrees(radians)  # радианы → градусы
```

**Когда что использовать:**
- **Хранить** направление удобнее в градусах (понятнее человеку)
- **Вычислять** sin/cos нужно в радианах (требование Python)

**Пример:**
```python
robot_direction = 45  # Храним в градусах

# Для вычислений переводим в радианы
angle_rad = math.radians(robot_direction)
dx = math.cos(angle_rad)
dy = math.sin(angle_rad)
```

---

## 🎯 Нормализация углов

Углы можно "нормализовать" — привести к диапазону [0, 360):

```python
robot_direction = robot_direction % 360
```

Примеры:
- `450 % 360` = 90°
- `-90 % 360` = 270°
- `720 % 360` = 0°

Это понадобится, когда добавим повороты!