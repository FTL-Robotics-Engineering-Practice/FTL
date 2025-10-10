# 🎯 Задание 4.3: Повороты и движение по направлению (20 мин)

**Повторяем:** Тригонометрия, векторное движение.

Финальный штрих! Добавим повороты клавишами Q и E, и изменим управление так, чтобы W двигал **по направлению** робота, как в настоящих играх!

---

## 🧠 Теория: Движение по направлению

### Старое управление (как танк сверху)
```python
if keys[pygame.K_w]:
    robot_y += move_speed  # Всегда вверх
```
W всегда двигает вверх, независимо от направления.

### Новое управление (как в играх)
```python
if keys[pygame.K_w]:
    robot_x += math.cos(angle) * move_speed  # По направлению!
    robot_y += math.sin(angle) * move_speed
```
W двигает **по направлению**, куда смотрит робот.

### Векторное движение

**Вектор** — направление и длина.

Если робот смотрит под углом α, то:
- Компонента X: `cos(α) * скорость`
- Компонента Y: `sin(α) * скорость`

```
       ↑ dy = sin(α) * speed
       |
       |
       +----→ dx = cos(α) * speed
      
      Робот движется по диагонали
```

### 4 направления движения

- **W (вперед):** двигаться в направлении `direction`
- **S (назад):** двигаться в направлении `direction + 180°`
- **A (влево боком):** двигаться в направлении `direction + 90°`
- **D (вправо боком):** двигаться в направлении `direction - 90°`

---

## 📝 Задача

1. Добавьте повороты: **Q** = влево, **E** = вправо
2. Измените движение WASD так, чтобы оно учитывало направление робота

---

## 🔧 Пошаговая инструкция

### Шаг 1: Скорость поворота
```python
turn_speed = 3
```

Скорость поворота в градусах за кадр. Пишется рядом с `move_speed`.

---

### Шаг 2: Поворот влево (Q)
```python
if keys[pygame.K_q]:
    robot_direction += turn_speed
    robot_direction %= 360
```

**Логика:**
- `+=` увеличивает угол (поворот против часовой стрелки)
- `%= 360` нормализует угол (450° → 90°)

---

### Шаг 3: Поворот вправо (E)
```python
if keys[pygame.K_e]:
    robot_direction -= turn_speed
    robot_direction %= 360
```

`-=` уменьшает угол (поворот по часовой стрелке).

---

### Шаг 4: Движение вперед (W)

**Удалите старый код:**
```python
# if keys[pygame.K_w]:  ← УДАЛИТЬ
#     robot_y += move_speed  ← УДАЛИТЬ
```

**Добавьте новый:**
```python
if keys[pygame.K_w]:
    angle = math.radians(robot_direction)
    robot_x += math.cos(angle) * move_speed
    robot_y += math.sin(angle) * move_speed
```

**Разбор:**
1. Переводим направление в радианы
2. `cos(angle)` дает смещение по X
3. `sin(angle)` дает смещение по Y
4. Умножаем на скорость

---

### Шаг 5: Движение назад (S)
```python
if keys[pygame.K_s]:
    angle = math.radians(robot_direction)
    robot_x -= math.cos(angle) * move_speed
    robot_y -= math.sin(angle) * move_speed
```

Просто минус — движение в противоположном направлении.

---

### Шаг 6: Движение влево боком (A)
```python
if keys[pygame.K_a]:
    angle = math.radians(robot_direction + 90)
    robot_x += math.cos(angle) * move_speed
    robot_y += math.sin(angle) * move_speed
```

**Почему +90°?**
Поворот направления на 90° влево = перпендикулярное движение.

---

### Шаг 7: Движение вправо боком (D)
```python
if keys[pygame.K_d]:
    angle = math.radians(robot_direction - 90)
    robot_x += math.cos(angle) * move_speed
    robot_y += math.sin(angle) * move_speed
```

Поворот на -90° = движение вправо перпендикулярно.

---

### Шаг 8: Обновите инструкции
```python
def draw_info(screen, x, y, direction, font):
    info_texts = [
        f"Позиция: ({x:.1f}, {y:.1f})",
        f"Направление: {direction:.1f}°",
        "",
        "Управление:",
        "W A S D - движение",
        "Q E - поворот",  # Новая строка!
        "R - сброс в центр"
    ]
    # ...
```

---

## 🚀 Ячейка для вашего кода

```python
import pygame
import math

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)

font = pygame.font.Font(None, 24)

# TODO: Обновите draw_info - добавьте строку "Q E - поворот"
def draw_info(screen, x, y, direction, font):
    # ...

def draw_robot(screen, x, y, direction, radius):
    # ... ваш код из предыдущего задания ...

robot_x = 0
robot_y = 0
robot_direction = 0
move_speed = 3
# TODO: Добавьте turn_speed = 3

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
    
    # TODO: Замените старое управление WASD на новое (с углами)
    # Движение вперед (W)
    if keys[pygame.K_w]:
        # angle = math.radians(robot_direction)
        # robot_x += ...
        # robot_y += ...
    
    # Движение назад (S)
    # ...
    
    # Движение влево (A)
    # ...
    
    # Движение вправо (D)
    # ...
    
    # TODO: Добавьте повороты Q и E
    # if keys[pygame.K_q]:
    #     robot_direction += turn_speed
    #     robot_direction %= 360
    
    screen.fill(WHITE)
    draw_robot(screen, robot_x, robot_y, robot_direction, 15)
    draw_info(screen, robot_x, robot_y, robot_direction, font)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

---

## ✅ Ячейка для проверки

Проверьте управление:

1. **Повороты:**
   - Зажмите Q → робот поворачивается влево (треугольник вращается)
   - Зажмите E → робот поворачивается вправо
   - Направление изменяется в тексте

2. **Движение:**
   - W → робот едет **по направлению** треугольника
   - S → робот едет назад
   - A → робот едет влево боком (перпендикулярно)
   - D → робот едет вправо боком

3. **Комбинации:**
   - Зажмите Q+W → робот едет вперед и поворачивает (дуга)
   - Попробуйте разные комбинации!

---

## 🎮 Игровое управление

Теперь управление похоже на игры:
- **Танки, машины:** W/S = вперед/назад, Q/E = поворот
- **Космические корабли:** то же самое!
- **Роботы:** именно так!

---

## 💡 Физика движения

### Прямое движение
```
Начало: direction = 0° (вправо)
W → едет вправо

После поворота: direction = 90° (вверх)
W → едет вверх!
```

### Дуговое движение
```
Зажать W + Q одновременно:
- W двигает вперед
- Q поворачивает
- Результат: движение по дуге (как машина поворачивает)
```

---

## 🔬 Разбор математики

**Почему cos для X, sin для Y?**

Единичная окружность:
```
        (0, 1)
    90°   |
          |
180° -----+----- 0° (1, 0)
          |
          |
       270°
```

При угле α:
- X = cos(α)
- Y = sin(α)

Примеры:
- 0°: cos(0°)=1, sin(0°)=0 → движение (1, 0) = вправо
- 90°: cos(90°)=0, sin(90°)=1 → движение (0, 1) = вверх
- 180°: cos(180°)=-1, sin(180°)=0 → движение (-1, 0) = влево

---

## 🎯 Связь с классом Robot

Вспомните Занятие 4:
```python
class Robot:
    def move_forward(self, distance):
        rad = math.radians(self.direction)
        self.x += distance * math.cos(rad)
        self.y += distance * math.sin(rad)
```

**Мы сделали то же самое!** Только вручную в игровом цикле.

На следующем занятии интегрируем класс `Robot` в Pygame, и код станет короче и чище.

---

## 🏆 Поздравляю!

Вы создали полноценного управляемого робота в Pygame!

**Что получилось:**
✅ Окно с сеткой координат  
✅ Робот с видимым направлением  
✅ Математическая система координат  
✅ Управление WASD + QE  
✅ Движение по направлению  
✅ Информационный интерфейс  

**Следующий шаг:**
На Занятии 6 добавим:
- Следование за курсором мыши
- Траекторию движения
- Интеграцию с классом Robot из Занятия 4

---

## 🚀 Эксперименты

1. **Изменить скорости:**
   ```python
   move_speed = 5   # Быстрее
   turn_speed = 5   # Быстрее поворот
   ```

2. **Инерция:**
   ```python
   # Вместо прямого изменения координат, используйте скорости:
   velocity_x = 0
   velocity_y = 0
   
   # В управлении изменяйте скорости
   # В update применяйте скорости к позиции
   ```

3. **Ограничение области:**
   ```python
   # Не давать роботу уйти за границы:
   if abs(robot_x) > 350:
       robot_x = 350 if robot_x > 0 else -350
   ```