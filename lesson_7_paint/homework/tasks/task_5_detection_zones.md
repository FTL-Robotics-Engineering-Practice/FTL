# 👁️ Блок 5: Зоны обнаружения препятствий

## 🎯 Цель

Робот умеет ездить, но **проезжает сквозь препятствия** как призрак! 👻

Чтобы остановить его перед препятствием, роботу нужно "видеть" окружение. Создадим **зоны обнаружения**:

1. **Зона обнаружения** (радиус 2×radius) — все клетки вокруг робота
2. **Передний сектор** (±45° впереди) — клетки, в которые робот может врезаться при движении вперёд

---

## 🧠 Теория: Расстояние между точками

Чтобы найти клетки в радиусе от робота, используем **формулу Евклидова расстояния**:

```
distance = √((x₂ - x₁)² + (y₂ - y₁)²)
```

В Python:

```python
import math

# Позиция робота
robot_x = 10.5
robot_y = 15.3

# Центр клетки (col, row)
cell_x = 12.0 + 0.5  # col + 0.5 (центр клетки)
cell_y = 16.0 + 0.5  # row + 0.5

# Вычисляем расстояние
dx = cell_x - robot_x
dy = cell_y - robot_y
distance = math.sqrt(dx*dx + dy*dy)

# Если distance <= detection_radius, клетка в зоне обнаружения
```

**Почему `col + 0.5`?**
- Клетка с индексом (12, 16) занимает квадрат от (12.0, 16.0) до (13.0, 17.0)
- Центр клетки: (12.5, 16.5)
- Мы измеряем расстояние до центра клетки

---

## 🧠 Теория: Углы и сектора

Чтобы определить **передний сектор** (±45° впереди), нужно:

1. Вычислить угол от робота до клетки: `cell_angle = atan2(dy, dx)`
2. Вычислить разницу между углом робота и углом клетки: `angle_diff = cell_angle - robot.angle`
3. Нормализовать `angle_diff` в диапазон [-π, π]
4. Если `|angle_diff| <= 45°` (0.785 радиан), клетка в переднем секторе

```
         Передний сектор (90°)
              ±45° от angle

         \         |         /
          \        |        /
           \   робот →     /
            \      •      /
             \           /
              \         /
```

---

## 📝 Задание 5.1: Метод get_detection_zone_cells

Добавим методы для получения клеток в зонах обнаружения.

**Откройте `robot.py` и добавьте в конец класса Robot:**

```python
    def get_detection_zone_cells(self, grid):
        """
        Получить все клетки в зоне обнаружения (радиус 2*radius от робота)

        Args:
            grid: объект Grid

        Returns:
            set клеток (col, row) в зоне обнаружения
        """
        cells = set()

        # TODO: Вычислите радиус зоны обнаружения (2 * self.radius)
        detection_radius = 2 * self.___

        # TODO: Вычислите границы квадрата для проверки
        # Мы проверяем квадрат вокруг робота, а потом фильтруем по расстоянию
        min_col = int(self.x - detection_radius)
        max_col = int(self.x + detection_radius) + 1
        min_row = int(self.y - ___)
        max_row = int(self.y + ___) + 1

        # Проверяем каждую клетку в квадрате
        for col in range(min_col, max_col):
            for row in range(min_row, max_row):
                # TODO: Проверяем границы сетки
                if 0 <= col < grid.___ and 0 <= row < grid.___:
                    # Вычисляем расстояние от центра робота до центра клетки
                    # Центр клетки: (col + 0.5, row + 0.5)
                    dx = (col + 0.5) - self.___
                    dy = (row + 0.5) - self.___

                    # TODO: Вычислите расстояние по формуле Евклида
                    # distance = √(dx² + dy²)
                    import math
                    distance = math.sqrt(dx*dx + dy*dy)

                    # TODO: Если клетка в радиусе обнаружения - добавляем
                    if distance <= ___:  # detection_radius
                        cells.add((col, row))

        return cells

    def get_forward_sector_cells(self, grid):
        """
        Получить клетки в секторе ±45° впереди робота (в зоне обнаружения)

        Args:
            grid: объект Grid

        Returns:
            set клеток (col, row) в переднем секторе
        """
        cells = set()
        detection_radius = 2 * self.radius

        # TODO: Определите угол сектора (±45° = 90° всего)
        # 45° в радианах = π/4 ≈ 0.785
        import math
        sector_angle = math.radians(___)  # 45

        # Вычисляем границы квадрата для проверки
        min_col = int(self.x - detection_radius)
        max_col = int(self.x + detection_radius) + 1
        min_row = int(self.y - detection_radius)
        max_row = int(self.y + detection_radius) + 1

        # Проверяем каждую клетку в квадрате
        for col in range(min_col, max_col):
            for row in range(min_row, max_row):
                # Проверяем границы сетки
                if 0 <= col < grid.cols and 0 <= row < grid.rows:
                    # Вектор от робота до клетки
                    dx = (col + 0.5) - self.x
                    dy = (row + 0.5) - self.y
                    distance = math.sqrt(dx*dx + dy*dy)

                    # Клетка должна быть в радиусе обнаружения
                    if distance <= detection_radius and distance > 0.1:
                        # TODO: Вычислите угол от робота до клетки
                        # atan2(dy, dx) возвращает угол в радианах
                        cell_angle = math.___(dy, dx)

                        # TODO: Вычислите разницу углов
                        angle_diff = cell_angle - self.___

                        # Нормализуем угол в диапазон [-π, π]
                        while angle_diff > math.pi:
                            angle_diff -= 2 * math.pi
                        while angle_diff < -math.pi:
                            angle_diff += 2 * math.pi

                        # TODO: Проверьте, попадает ли клетка в сектор ±45°
                        if abs(angle_diff) <= ___:  # sector_angle
                            cells.add((col, row))

        return cells
```

**Сохраните файл.**

---

## 📝 Задание 5.2: Визуализация зон

Добавим отрисовку зон обнаружения, чтобы видеть, что "видит" робот.

**Откройте `renderer.py` и добавьте метод:**

```python
    def draw_detection_zones(self, robot, grid):
        """
        Отрисовать зоны обнаружения робота

        Args:
            robot: объект Robot
            grid: объект Grid
        """
        # Получаем клетки в зонах
        detection_cells = robot.get_detection_zone_cells(grid)
        forward_cells = robot.get_forward_sector_cells(grid)

        # TODO: Рисуем зону обнаружения (светло-синий)
        for col, row in detection_cells:
            x = col * grid.cell_width + grid.offset_x
            y = row * grid.cell_height

            # Создаём полупрозрачную поверхность
            surface = pygame.Surface((grid.cell_width, grid.cell_height))
            surface.set_alpha(___)  # 50 - полупрозрачность
            surface.fill((100, 150, 255))  # светло-синий
            self.screen.blit(surface, (x, y))

        # TODO: Рисуем передний сектор (жёлтый) поверх зоны обнаружения
        for col, row in ___:  # forward_cells
            x = col * grid.cell_width + grid.offset_x
            y = row * grid.cell_height

            # Проверяем, заполнена ли клетка препятствием
            if grid.is_cell_filled(col, row):
                # Препятствие впереди - красный!
                color = (255, 100, 100)
            else:
                # Пусто - жёлтый
                color = (255, 255, 100)

            surface = pygame.Surface((grid.cell_width, grid.cell_height))
            surface.set_alpha(100)
            surface.fill(___)  # color
            self.screen.blit(surface, (x, y))
```

**Сохраните файл.**

---

## 📝 Задание 5.3: Интегрируем в main.py

**Откройте `main.py` и обновите отрисовку:**

Найдите блок отрисовки робота и добавьте вызов draw_detection_zones:

```python
        # Рисуем робота только в режиме ROBOT
        if mode_manager.is_robot_mode():
            # TODO: Сначала рисуем зоны обнаружения (под роботом)
            renderer.___(robot, grid)

            # Потом рисуем робота поверх зон
            renderer.draw_robot(robot, grid)
```

**Сохраните файл.**

---

## ✅ Тестирование зон обнаружения

**Запустите программу:**

```bash
python main.py
```

### Тест 1: Рисуем препятствия

1. **Режим MAP_EDIT** (начальный)
2. Нарисуйте стену из препятствий

### Тест 2: Проверяем зоны

1. **TAB** → переключаем на режим ROBOT
2. Управляйте роботом (WASD)
3. **Наблюдайте:**
   - **Светло-синяя область** вокруг робота — зона обнаружения (радиус 2) ✅
   - **Жёлтый сектор** впереди — передний сектор (±45°) ✅
   - **Красные клетки** в переднем секторе — препятствия! ✅

### Тест 3: Поворот

1. Поворачивайте робота (A/D)
2. Передний сектор (жёлтый) **поворачивается вместе с роботом** ✅
3. Зона обнаружения (синяя) остаётся круглой ✅

### Тест 4: Препятствия

1. Подъезжайте к стене
2. Когда стена попадает в передний сектор → **клетки краснеют** ✅
3. Робот пока **проезжает сквозь стену** (это нормально, исправим в следующем блоке)

**Отлично! Зоны работают! 🎉**

---

## 📝 Задание 5.4: БОНУС - Тестовый скрипт (опционально)

Создадим тест для проверки зон обнаружения.

**Создайте `test_detection_zones.py`:**

```python
"""Тест зон обнаружения робота"""
from robot import Robot
from grid import Grid

# Создаём сетку и робота
grid = Grid(800, 600, 10, 12, offset_x=0)
robot = Robot(x=10.0, y=10.0, angle=0.0, radius=1.0)

# Добавляем препятствия
grid.fill_cell(13, 10)  # Впереди
grid.fill_cell(13, 11)
grid.fill_cell(14, 10)

print("=== ТЕСТ 1: Зона обнаружения ===")
detection_cells = robot.get_detection_zone_cells(grid)
print(f"Клеток в зоне обнаружения: {len(detection_cells)}")
print(f"Ожидалось: ~12-16 клеток (круг радиуса 2)")

print("\n=== ТЕСТ 2: Передний сектор ===")
forward_cells = robot.get_forward_sector_cells(grid)
print(f"Клеток в переднем секторе: {len(forward_cells)}")
print(f"Ожидалось: ~4-6 клеток (сектор 90° впереди)")

print("\n=== ТЕСТ 3: Препятствия в переднем секторе ===")
obstacles_in_front = 0
for col, row in forward_cells:
    if grid.is_cell_filled(col, row):
        obstacles_in_front += 1
        print(f"  Препятствие в клетке ({col}, {row})")

print(f"\nВсего препятствий впереди: {obstacles_in_front}")
print(f"Ожидалось: 3 (мы добавили 3 клетки впереди)")

print("\n=== ТЕСТ 4: Поворот робота ===")
import math
robot.angle = math.pi / 2  # 90° - смотрим вверх

forward_cells_up = robot.get_forward_sector_cells(grid)
print(f"После поворота на 90°: {len(forward_cells_up)} клеток в переднем секторе")

obstacles_up = sum(1 for col, row in forward_cells_up if grid.is_cell_filled(col, row))
print(f"Препятствий впереди после поворота: {obstacles_up}")
print(f"Ожидалось: 0-1 (препятствия справа, не впереди)")

print("\n✅ Все тесты пройдены!")
```

**Запустите:**

```bash
python test_detection_zones.py
```

---

## 🎓 Что мы узнали?

1. ✅ **Формула Евклидова расстояния** — `√(dx² + dy²)`
2. ✅ **Зона обнаружения** — круг радиуса 2×radius вокруг робота
3. ✅ **Угол до клетки** — `atan2(dy, dx)`
4. ✅ **Разница углов** — `cell_angle - robot.angle`
5. ✅ **Нормализация угла** — приведение в диапазон [-π, π]
6. ✅ **Передний сектор** — клетки в пределах ±45° от направления робота
7. ✅ **Визуальная отладка** — полупрозрачные цветные зоны
8. ✅ **Цветовая индикация** — красный = препятствие впереди

---

## 💡 Как это работает?

```
Каждый кадр:

1. robot.get_detection_zone_cells(grid)
   → Проверяем все клетки в квадрате вокруг робота
   → Вычисляем расстояние до каждой
   → Если distance <= 2*radius → добавляем в set

2. robot.get_forward_sector_cells(grid)
   → Проверяем клетки в зоне обнаружения
   → Вычисляем угол до каждой клетки
   → Если |угол - robot.angle| <= 45° → добавляем в set

3. renderer.draw_detection_zones()
   → Рисуем синие клетки (зона обнаружения)
   → Рисуем жёлтые/красные клетки (передний сектор)
   → Красный цвет = препятствие в клетке
```

---

## 🚀 Следующий шаг

Робот "видит" препятствия! Теперь самое время **научить его останавливаться** перед ними.

**Дальше:** Добавим проверку столкновений — если в переднем секторе есть препятствие, запретим движение вперёд!
