# 📊 Задание 3.3: Улучшенный интерфейс (15 мин)

**Повторяем:** Функции, списки, циклы.

Сейчас вывод текста занимает много строк кода. Давайте создадим функцию для красивого отображения информации!

---

## 🧠 Теория: Функции для организации кода

### Зачем нужны функции?

**Без функции (много повторений):**
```python
text1 = font.render("Строка 1", True, BLACK)
screen.blit(text1, (10, 10))

text2 = font.render("Строка 2", True, BLACK)
screen.blit(text2, (10, 35))

text3 = font.render("Строка 3", True, BLACK)
screen.blit(text3, (10, 60))
```

**С функцией (чисто и понятно):**
```python
draw_info(screen, robot_x, robot_y, font)
```

### Функции с параметрами

```python
def draw_info(screen, x, y, font):
    # screen, x, y, font - параметры функции
    # Можем использовать их внутри
```

Функция принимает данные и работает с ними.

---

## 📝 Задача

Создайте функцию `draw_info(screen, x, y, font)`, которая красиво выводит всю информацию о роботе:
- Позицию
- Пустую строку (для разделения)
- Заголовок "Управление:"
- Инструкции по управлению

---

## 🔧 Пошаговая инструкция

### Шаг 1: Создание функции
```python
def draw_info(screen, x, y, font):
```

Функция принимает 4 параметра:
- `screen` — где рисовать
- `x, y` — координаты робота
- `font` — объект шрифта

**Где писать:** После создания шрифта, до игрового цикла.

---

### Шаг 2: Список строк для вывода
```python
    info_texts = [
        f"Позиция: ({x:.1f}, {y:.1f})",
        "",
        "Управление:",
        "W A S D - движение",
        "R - сброс в центр"
    ]
```

Создаем **список** строк. Каждый элемент — отдельная строка текста.

**Обратите внимание:**
- Первая строка использует f-string для подстановки координат
- Пустая строка `""` создает отступ
- `.1f` форматирует число: 1 знак после запятой

---

### Шаг 3: Переменная для вертикальной позиции
```python
    y_offset = 10
```

Начинаем рисовать с Y-координаты 10 (отступ от верха экрана).

---

### Шаг 4: Цикл для вывода всех строк
```python
    for text in info_texts:
```

Проходим по каждой строке из списка.

---

### Шаг 5: Рендер и отображение строки
```python
        surface = font.render(text, True, BLACK)
        screen.blit(surface, (10, y_offset))
```

Для каждой строки:
1. Создаем картинку с текстом
2. Рисуем её в позиции `(10, y_offset)`

---

### Шаг 6: Сдвиг вниз
```python
        y_offset += 25
```

Увеличиваем `y_offset` на 25 пикселей → следующая строка будет ниже.

**Почему 25?**
- Высота строки примерно 20 пикселей (при размере шрифта 24)
- +5 пикселей отступ между строками
- Итого: 25 пикселей

---

### Шаг 7: Вызов функции в цикле
```python
draw_info(screen, robot_x, robot_y, font)
```

Вместо всех `text1`, `text2`, `text3` теперь один вызов функции!

Пишется в игровом цикле после рисования круга, до `pygame.display.flip()`.

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

# TODO: Создайте функцию draw_info(screen, x, y, font)
def draw_info(screen, x, y, font):
    """Рисует информацию на экране"""
    # TODO: Создайте список info_texts
    
    # TODO: Создайте переменную y_offset = 10
    
    # TODO: Цикл for text in info_texts:
    #     Создайте surface через font.render()
    #     Выведите через screen.blit()
    #     Увеличьте y_offset

robot_x = 0
robot_y = 0
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
    
    # TODO: Вызовите draw_info() вместо отдельных text1, text2, text3
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

---

## ✅ Ячейка для проверки

Вы должны увидеть:
- Позицию робота (обновляется при движении)
- Пустую строку
- Заголовок "Управление:"
- Инструкции по управлению (2 строки)

Все строки должны быть ровно выровнены по левому краю.

---

## 💡 Преимущества функции

**Легко добавлять информацию:**
```python
info_texts = [
    f"Позиция: ({x:.1f}, {y:.1f})",
    f"Скорость: {move_speed}",  # Новая строка!
    "",
    "Управление:",
    # ...
]
```

**Легко менять стиль:**
```python
y_offset += 30  # Больше отступ между строками
```

**Можно использовать повторно:**
```python
draw_info(screen, robot1.x, robot1.y, font)  # Для первого робота
draw_info(screen, robot2.x, robot2.y, font)  # Для второго робота
```

---

## 🎨 Улучшения интерфейса (по желанию)

### 1. Рамка вокруг текста
```python
def draw_info(screen, x, y, font):
    # ... ваш код ...
    
    # После вывода всех строк:
    pygame.draw.rect(screen, BLACK, (5, 5, 200, y_offset), 2)
    # Рисует прямоугольник вокруг текста
```

### 2. Разные цвета для разных строк
```python
info_texts = [
    (f"Позиция: ({x:.1f}, {y:.1f})", BLACK),
    ("", BLACK),
    ("Управление:", BLUE),  # Заголовок синим
    ("W A S D - движение", BLACK),
    ("R - сброс в центр", BLACK)
]

for text, color in info_texts:
    surface = font.render(text, True, color)
    # ...
```

### 3. Больший шрифт для заголовков
```python
font_title = pygame.font.Font(None, 32)
font_normal = pygame.font.Font(None, 24)

# В функции выбираем шрифт в зависимости от текста
```

---

## 🔍 Docstring для функции

Хорошая практика — добавлять описание функции:

```python
def draw_info(screen, x, y, font):
    """
    Рисует информацию о роботе на экране.
    
    Параметры:
        screen: Поверхность Pygame для рисования
        x: X-координата робота (математическая)
        y: Y-координата робота (математическая)
        font: Объект шрифта Pygame
    """
    # ...
```

Это помогает другим (и вам через месяц) понять, что делает функция!