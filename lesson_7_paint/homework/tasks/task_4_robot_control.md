# 🎮 Блок 4: Управление роботом WASD

## 🎯 Цель

Робот едет по кругу — это хорошо для теста, но хочется управлять им самому!

Добавим **управление клавишами WASD**:
- **W** — ехать вперёд
- **S** — ехать назад
- **A** — поворачивать влево
- **D** — поворачивать вправо

Управление будет **плавным** — можно зажать несколько клавиш одновременно (например, W+D = ехать вперёд и поворачивать вправо).

---

## 🧠 Теория: События vs Состояние клавиш

### Подход 1: События (что мы использовали раньше)

```python
for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_z:
            print("Нажали Z один раз")
```

**Проблема:** Получаем событие только **в момент нажатия**. Если зажать W, получим одно событие, и робот сдвинется один раз.

### Подход 2: Состояние клавиш (для непрерывного управления)

```python
# В игровом цикле (каждый кадр):
pressed_keys = pygame.key.get_pressed()

if pressed_keys[pygame.K_w]:
    print("W зажата прямо сейчас")
```

**Преимущество:** Можем проверять **каждый кадр**, зажата ли клавиша. Если W зажата — робот едет вперёд каждый кадр.

### Наша стратегия

1. **События KEYDOWN/KEYUP** → сохраняем в словарь `pressed_keys`
2. **Каждый кадр** → проверяем словарь и устанавливаем скорости робота

```python
# Когда клавиша нажата
pressed_keys[pygame.K_w] = True

# Когда клавиша отпущена
pressed_keys[pygame.K_w] = False

# Каждый кадр
if pressed_keys[pygame.K_w]:
    robot.linear_velocity = 10.0  # едем вперёд
```

---

## 📝 Задание 4.1: Добавляем отслеживание клавиш в InputManager

Обновим InputManager для отслеживания нажатых клавиш.

**Откройте `input_manager.py` и внесите изменения:**

### Шаг 1: Добавьте robot и словарь pressed_keys в __init__

```python
    def __init__(self, grid, history, running_flag, mode_manager, robot):
        """
        Инициализация менеджера ввода

        Args:
            grid: объект Grid
            history: объект History
            running_flag: список [True/False] для управления циклом
            mode_manager: объект ModeManager
            robot: объект Robot  # <-- ДОБАВЛЕНО
        """
        self.grid = grid
        self.history = history
        self.running_flag = running_flag
        self.mode_manager = mode_manager
        self.robot = robot  # <-- ДОБАВЛЕНО

        # Флаги состояния мыши
        self.left_mouse_pressed = False
        self.right_mouse_pressed = False
        self.last_drawn_cell = None
        self.last_erased_cell = None

        # TODO: Словарь для отслеживания нажатых клавиш управления
        # Формат: {код_клавиши: True/False}
        self.pressed_keys = {
            pygame.K_w: ___,  # False
            pygame.K_s: ___,  # False
            pygame.K_a: ___,  # False
            pygame.K_d: ___   # False
        }

        # Словарь привязок клавиш
        self.key_bindings = {}

        # Настраиваем привязки клавиш
        self._setup_default_bindings()
```

### Шаг 2: Обновите handle_event для отслеживания WASD

Добавьте **перед** обработкой привязок клавиш:

```python
    def handle_event(self, event):
        """
        Обработать событие pygame

        Args:
            event: объект события pygame
        """
        # Обработка клавиш
        if event.type == pygame.KEYDOWN:
            # TODO: Если нажата клавиша управления роботом - сохраняем в словарь
            if event.key in self.pressed_keys:
                self.pressed_keys[event.___] = ___  # True

            # Проверяем, есть ли привязка для этой клавиши
            if event.key in self.key_bindings:
                self.key_bindings[event.key]['function']()

        # TODO: Обработка отпускания клавиш
        elif event.type == pygame.___:  # KEYUP
            # Если отпущена клавиша управления - сбрасываем в словаре
            if event.key in self.pressed_keys:
                self.pressed_keys[event.key] = ___  # False

        # Обработка мыши - нажатие
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_button_down(event.button)

        # Обработка мыши - отпускание
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_button_up(event.button)
```

### Шаг 3: Добавьте метод update_robot_velocities

В конец класса InputManager добавьте:

```python
    def update_robot_velocities(self):
        """
        Обновить скорости робота на основе нажатых клавиш

        Вызывается каждый кадр в игровом цикле
        """
        # Только в режиме робота
        if not self.mode_manager.is_robot_mode():
            return

        # TODO: Вычисляем линейную скорость
        linear_velocity = 0.0

        if self.pressed_keys[pygame.K_w]:
            # W - ехать вперёд (положительная скорость)
            linear_velocity += self.robot.___  # max_linear_velocity

        if self.pressed_keys[pygame.K___]:  # S
            # S - ехать назад (отрицательная скорость)
            linear_velocity -= self.robot.max_linear_velocity

        # TODO: Вычисляем угловую скорость
        angular_velocity = 0.0

        if self.pressed_keys[pygame.K___]:  # A
            # A - поворот влево (положительная угловая скорость)
            # В pygame: положительный угол = против часовой стрелки = влево
            angular_velocity += self.robot.___  # max_angular_velocity

        if self.pressed_keys[pygame.K___]:  # D
            # D - поворот вправо (отрицательная угловая скорость)
            angular_velocity -= self.robot.max_angular_velocity

        # TODO: Установите скорости робота
        self.robot.set_velocities(___, ___)
```

**Сохраните файл.**

---

## 📝 Задание 4.2: Обновляем main.py

Теперь нужно передать robot в InputManager и вызывать update_robot_velocities каждый кадр.

**Откройте `main.py`:**

### Шаг 1: Передайте robot в InputManager

```python
    # Создаём менеджер ввода (теперь с robot)
    input_manager = InputManager(grid, history, running, mode_manager, robot)  # <-- ДОБАВЛЕНО robot
```

### Шаг 2: Вызывайте update_robot_velocities каждый кадр

В игровом цикле **перед** обновлением робота:

```python
    # Игровой цикл
    while running[0]:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running[0] = False
            else:
                input_manager.handle_event(event)

        # Получаем позицию мыши
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # TODO: Обновляем скорости робота на основе нажатых клавиш
        input_manager.___()

        # Обновляем робота только в режиме ROBOT
        if mode_manager.is_robot_mode():
            # УДАЛИТЕ ЭТИ СТРОКИ (временное управление):
            # robot.set_velocities(linear=5.0, angular=1.0)

            # Оставьте только:
            robot.update(dt=0.016)  # ~60 FPS
            robot.clamp_position(robot.radius, grid.cols - robot.radius,
                                robot.radius, grid.rows - robot.radius)

        # ... остальной код без изменений
```

**Сохраните файл.**

---

## ✅ Тестирование управления

**Запустите программу:**

```bash
python main.py
```

### Тест 1: Режим MAP_EDIT (начальный)

- Мышь рисует препятствия ✅
- WASD не работают (робота нет) ✅

### Тест 2: Переключение на режим ROBOT

1. Нажмите **TAB** → "Режим: РОБОТ (управление WASD)"
2. Нарисуйте несколько препятствий для ориентира

### Тест 3: Управление роботом

1. **W** — робот едет вперёд ✅
2. **S** — робот едет назад ✅
3. **A** — робот поворачивается влево (против часовой стрелки) ✅
4. **D** — робот поворачивается вправо (по часовой стрелке) ✅

### Тест 4: Комбинации клавиш

1. **W + D** — едет вперёд и поворачивает вправо (дуга) ✅
2. **S + A** — едет назад и поворачивает влево ✅

### Тест 5: Границы карты

- Робот не выходит за края карты ✅

**Отлично! Управление работает! 🎉**

---

## 📝 Задание 4.3: БОНУС - Настройка скоростей (опционально)

Если робот едет слишком быстро или медленно, можно настроить скорости.

**В `main.py` при создании робота:**

```python
# Создаём робота с настроенными скоростями
robot = Robot(
    x=GRID_COLS / 2.0,
    y=GRID_ROWS / 2.0,
    angle=0.0,
    max_linear_velocity=10,  # Попробуйте 5, 10, 15
    max_angular_velocity=5,  # Попробуйте 3, 5, 7
    radius=1.0
)
```

**Поэкспериментируйте:**
- `max_linear_velocity=5` — робот медленный
- `max_linear_velocity=20` — робот быстрый
- `max_angular_velocity=3` — поворот медленный
- `max_angular_velocity=10` — поворот быстрый

---

## 🎓 Что мы узнали?

1. ✅ **События vs Состояние** — для непрерывного управления используем состояние клавиш
2. ✅ **Словарь pressed_keys** — отслеживание нажатых клавиш WASD
3. ✅ **KEYDOWN/KEYUP** — обновление словаря при нажатии/отпускании
4. ✅ **update_robot_velocities()** — преобразование клавиш в скорости
5. ✅ **Комбинации клавиш** — можно зажать W+D одновременно
6. ✅ **Положительные/отрицательные скорости:**
   - W (вперёд): `+max_linear_velocity`
   - S (назад): `-max_linear_velocity`
   - A (влево): `+max_angular_velocity`
   - D (вправо): `-max_angular_velocity`

---

## 💡 Как это работает?

```
Каждый кадр (60 раз в секунду):

1. Обрабатываем события KEYDOWN/KEYUP
   → Обновляем pressed_keys

2. Вызываем update_robot_velocities()
   → Проверяем pressed_keys
   → Вычисляем linear_velocity и angular_velocity
   → Устанавливаем robot.set_velocities()

3. Вызываем robot.update(dt=0.016)
   → Робот обновляет свою позицию на основе скоростей
   → x += linear_velocity * cos(angle) * dt
   → y += linear_velocity * sin(angle) * dt
   → angle += angular_velocity * dt

4. Рисуем робота на экране
```

---

## 🚀 Следующий шаг

Управление работает отлично! Но робот **проезжает сквозь препятствия** 😱

**Дальше:** Добавим зоны обнаружения, чтобы робот "видел" препятствия вокруг себя!
