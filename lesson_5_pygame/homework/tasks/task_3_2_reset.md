# 🔄 Задание 3.2: Сброс позиции (10 мин)

**Повторяем:** События клавиатуры, KEYDOWN.

Иногда робот уезжает далеко за пределы экрана. Неудобно возвращать его обратно! Добавим кнопку для мгновенного возврата в центр.

---

## 🧠 Теория: Разница между get_pressed() и событиями

### Для плавного движения: get_pressed()
```python
keys = pygame.key.get_pressed()
if keys[pygame.K_w]:
    # Срабатывает КАЖДЫЙ КАДР пока зажата
```

### Для одиночного действия: события KEYDOWN
```python
for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            # Срабатывает ОДИН РАЗ при нажатии
```

**Когда что использовать?**
- **Движение** → `get_pressed()` (нужно удержание)
- **Сброс, прыжок, выстрел** → `KEYDOWN` (нужно одно нажатие)

---

## 📝 Задача

Добавьте обработку клавиши **R** (Reset). При нажатии робот должен мгновенно вернуться в центр координат (0, 0).

---

## 🔧 Пошаговая инструкция

### Шаг 1: Обработка события KEYDOWN
```python
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    
    if event.type == pygame.KEYDOWN:
```

Добавляем новую проверку **внутри** цикла обработки событий.

`pygame.KEYDOWN` — событие "клавиша была нажата".

---

### Шаг 2: Проверка конкретной клавиши
```python
        if event.key == pygame.K_r:
```

`event.key` — какая именно клавиша была нажата.

Важно: это **внутри** блока `if event.type == pygame.KEYDOWN:`, поэтому два уровня отступов!

---

### Шаг 3: Сброс координат
```python
            robot_x = 0
            robot_y = 0
```

Устанавливаем координаты в (0, 0) — центр в математической системе координат.

---

### Шаг 4: Обновить текст с подсказкой
```python
text3 = font.render("R - сброс в центр", True, BLACK)
screen.blit(text3, (10, 60))
```

Добавим третью строку текста с подсказкой.

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

robot_x = 0
robot_y = 0
move_speed = 3

running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # TODO: Добавьте обработку KEYDOWN
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_r:
        #         ...
    
    # Управление
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w]:
        robot_y += move_speed
    if keys[pygame.K_s]:
        robot_y -= move_speed
    if keys[pygame.K_a]:
        robot_x -= move_speed
    if keys[pygame.K_d]:
        robot_x += move_speed
    
    # Преобразование координат
    screen_x = int(robot_x + WIDTH/2)
    screen_y = int(HEIGHT/2 - robot_y)
    
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLUE, (screen_x, screen_y), 15)
    
    # Текст
    text1 = font.render(f"Позиция: ({robot_x:.1f}, {robot_y:.1f})", True, BLACK)
    text2 = font.render("Управление: W A S D", True, BLACK)
    # TODO: Добавьте text3 с подсказкой про R
    
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 35))
    # TODO: Выведите text3
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

---

## ✅ Ячейка для проверки

Проверьте работу:
1. Управляйте роботом WASD, уведите его от центра
2. Нажмите R → робот мгновенно вернулся в центр
3. Координаты стали (0.0, 0.0)
4. На экране появилась подсказка "R - сброс в центр"

**Важно:** Нажмите R **один раз**, а не удерживайте!

---

## 💡 Различия в поведении

**Если использовать get_pressed() для сброса (неправильно):**
```python
keys = pygame.key.get_pressed()
if keys[pygame.K_r]:
    robot_x = 0
    robot_y = 0
```

Проблема: если удерживать R, робот "залипнет" в центре — нельзя будет управлять!

**С событием KEYDOWN (правильно):**
```python
if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_r:
        robot_x = 0
        robot_y = 0
```

Сброс происходит один раз при нажатии, дальше можно двигаться.

---

## 🎯 Структура обработки событий

Правильная структура кода:

```python
while running:
    # 1. События (одиночные действия)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Сброс
            if event.key == pygame.K_SPACE:
                # Прыжок/выстрел
    
    # 2. Непрерывное управление (удержание клавиш)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        # Движение
    
    # 3. Рисование
    # ...
```

---

## 🔍 Дополнительные эксперименты

Добавьте еще клавиши:

1. **SPACE** — увеличить радиус круга
   ```python
   if event.key == pygame.K_SPACE:
       robot_radius += 5
   ```

2. **Стрелки** — альтернативное управление
   ```python
   if keys[pygame.K_UP]:
       robot_y += move_speed
   ```

3. **Числовые клавиши** — изменение скорости
   ```python
   if event.key == pygame.K_1:
       move_speed = 1
   if event.key == pygame.K_2:
       move_speed = 5
   ```