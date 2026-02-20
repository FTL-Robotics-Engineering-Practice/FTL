# Блок 4.1: Навигация к цели (дополнительный)

## 📖 Текстовая ячейка (интро)

### 🎯 Роботы учатся находить путь

До сих пор наши роботы двигались по заранее заданным командам. Но настоящие роботы должны уметь **сами планировать маршрут** к цели!

### 🧠 Алгоритм планирования пути

**Простая стратегия:**
1. Сначала выравниваемся по **X** (горизонтали)
2. Потом выравниваемся по **Y** (вертикали)  
3. Приходим в цель!

**Пример:** из (0, 0) в (3, 2)
- Шаги: `right, right, right, up, up`
- Результат: (0,0) → (1,0) → (2,0) → (3,0) → (3,1) → (3,2) ✅

### 📐 Математика навигации

Чтобы попасть из (x₁, y₁) в (x₂, y₂):
- **Δx = x₂ - x₁** (сколько шагов по X)
- **Δy = y₂ - y₁** (сколько шагов по Y)

**Направления:**
- Если Δx > 0 → идем `right`
- Если Δx < 0 → идем `left`  
- Если Δy > 0 → идем `up`
- Если Δy < 0 → идем `down`

### 🗺️ Генерация команд

Робот должен **сам создать список команд** для достижения цели:

```python
def move_to_target(self, target_x, target_y):
    commands = []
    # Генерируем команды для X
    # Генерируем команды для Y  
    # Выполняем все команды
```

### 🎮 Практическое применение

- **GPS навигация** - точно так же работает!
- **Роботы-пылесосы** планируют маршрут по комнате
- **Беспилотники** летят к координатам

---

## 💻 Код для ученика

```python
# Блок 4.1: Навигация к цели - роботы планируют маршрут!
# Учим роботов находить путь самостоятельно

import matplotlib.pyplot as plt
import math

class NavigatorRobot:
    """Робот-навигатор, который умеет планировать маршруты"""
    
    def __init__(self, name, start_x=0, start_y=0, color="blue"):
        self.name = name
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.color = color
        self.steps_made = 0
        self.path = [(start_x, start_y)]
        self.targets_reached = 0
        print(f"🧭 {name} готов к навигации из ({start_x}, {start_y})")
    
    def move_up(self):
        self.y += 1
        self.steps_made += 1
        self.path.append((self.x, self.y))
    
    def move_down(self):
        self.y -= 1
        self.steps_made += 1
        self.path.append((self.x, self.y))
    
    def move_left(self):
        self.x -= 1
        self.steps_made += 1
        self.path.append((self.x, self.y))
    
    def move_right(self):
        self.x += 1
        self.steps_made += 1
        self.path.append((self.x, self.y))
    
    def execute_command(self, command):
        """Выполняет одну команду"""
        if command == "up":
            self.move_up()
        elif command == "down":
            self.move_down()
        elif command == "left":
            self.move_left()
        elif command == "right":
            self.move_right()
    
    def calculate_distance(self, target_x, target_y):
        """Вычисляет расстояние до цели"""
        # TODO: Используйте формулу расстояния
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(___ * ___ + ___ * ___)
        return distance
    
    def generate_path_commands(self, target_x, target_y):
        """Генерирует список команд для достижения цели"""
        commands = []
        
        # TODO: Вычислите сколько шагов нужно по каждой оси
        dx = ___ - self.x  # сколько по X
        dy = ___ - self.y  # сколько по Y
        
        print(f"📐 {self.name}: нужно пройти Δx={dx}, Δy={dy}")
        
        # TODO: Генерируем команды для движения по X
        if dx > 0:  # нужно идти вправо
            commands.extend(["___"] * ___)  # добавляем команды "right"
        elif dx < 0:  # нужно идти влево
            commands.extend(["___"] * abs(___))  # добавляем команды "left"
        
        # TODO: Генерируем команды для движения по Y
        if dy > 0:  # нужно идти вверх
            commands.extend(["___"] * ___)
        elif dy < 0:  # нужно идти вниз  
            commands.extend(["___"] * abs(___))
        
        return commands
    
    def move_to_target(self, target_x, target_y):
        """Главный метод: планирует и выполняет маршрут к цели"""
        print(f"\n🎯 {self.name} планирует маршрут из ({self.x}, {self.y}) в ({target_x}, {target_y})")
        
        # Вычисляем расстояние
        distance = self.calculate_distance(target_x, target_y)
        print(f"📏 Расстояние до цели: {distance:.2f}")
        
        # Генерируем команды
        commands = self.generate_path_commands(target_x, target_y)
        print(f"🗺️ План маршрута: {commands}")
        print(f"📊 Общее количество шагов: {len(commands)}")
        
        # Выполняем команды
        print(f"🚶 Начинаем движение...")
        for i, command in enumerate(commands):
            self.execute_command(command)
            print(f"   Шаг {i+1}: {command} → ({self.x}, {self.y})")
        
        # Проверяем успех
        if self.x == target_x and self.y == target_y:
            self.targets_reached += 1
            print(f"✅ {self.name} достиг цели ({target_x}, {target_y})!")
        else:
            print(f"❌ {self.name} промахнулся! Цель: ({target_x}, {target_y}), факт: ({self.x}, {self.y})")
        
        return self.x == target_x and self.y == target_y
    
    def show_info(self):
        """Информация о навигаторе"""
        print(f"🧭 {self.name}:")
        print(f"   📍 Текущая позиция: ({self.x}, {self.y})")
        print(f"   🏠 Стартовая позиция: ({self.start_x}, {self.start_y})")
        print(f"   👣 Шагов сделано: {self.steps_made}")
        print(f"   🎯 Целей достигнуто: {self.targets_reached}")
    
    def draw(self, targets=None):
        """Рисует робота, его путь и цели"""
        # Путь робота
        if len(self.path) > 1:
            x_coords = [p[0] for p in self.path]
            y_coords = [p[1] for p in self.path]
            plt.plot(x_coords, y_coords, 
                    color=self.color, 
                    linewidth=2, 
                    alpha=0.7,
                    label=f'{self.name} путь')
        
        # Стартовая позиция
        plt.scatter(self.start_x, self.start_y, 
                   color=self.color, 
                   s=150, 
                   marker='^', 
                   alpha=0.8,
                   label=f'{self.name} старт')
        
        # Текущая позиция
        plt.scatter(self.x, self.y, 
                   color=self.color, 
                   s=200, 
                   marker='o',
                   alpha=0.9,
                   label=f'{self.name}')
        
        # Цели (если переданы)
        if targets:
            for i, (tx, ty) in enumerate(targets):
                plt.scatter(tx, ty, 
                           color='red', 
                           s=150, 
                           marker='*',
                           alpha=0.8)
                plt.annotate(f'Цель {i+1}', (tx, ty), 
                           xytext=(5, 5), 
                           textcoords='offset points')

# ТЕСТ 1: Простая навигация
print("🧪 ТЕСТ 1: Простая навигация к одной цели")

# TODO: Создайте навигатора
navigator = NavigatorRobot("___", ___, ___, "blue")

# TODO: Отправьте его к цели (5, 3)
target_x, target_y = 5, 3
success = navigator.move_to_target(___, ___)

navigator.show_info()
print(f"Результат: {'✅ Успех' if success else '❌ Неудача'}")

# ТЕСТ 2: Множественные цели
print("\n🧪 ТЕСТ 2: Путешествие по множественным целям")

# TODO: Создайте нового робота-путешественника
traveler = NavigatorRobot("___", ___, ___, "green")

# Список целей для посещения
destinations = [(3, 4), (7, 2), (1, 6), (8, 8)]

print(f"🗺️ {traveler.name} должен посетить {len(destinations)} мест:")
for i, (x, y) in enumerate(destinations):
    print(f"   {i+1}. ({x}, {y})")

# TODO: Посетите все цели по очереди
successful_trips = 0
for i, (target_x, target_y) in enumerate(destinations):
    print(f"\n--- ПОЕЗДКА {i+1} К ({target_x}, {target_y}) ---")
    success = traveler.move_to_target(___, ___)
    if success:
        successful_trips += 1

traveler.show_info()
print(f"\n📊 Статистика путешествий:")
print(f"   🎯 Целей назначено: {len(destinations)}")
print(f"   ✅ Целей достигнуто: {successful_trips}")
print(f"   📈 Процент успеха: {successful_trips/len(destinations)*100:.1f}%")

# ТЕСТ 3: Навигация в разные стороны
print("\n🧪 ТЕСТ 3: Навигация во все стороны света")

# TODO: Создайте робота-исследователя
explorer = NavigatorRobot("___", ___, ___, "red")

# Цели во всех направлениях от центра
directions_targets = [
    (10, 5),  # восток
    (5, 10),  # север  
    (0, 5),   # запад
    (5, 0),   # юг
    (5, 5)    # возврат в центр
]

direction_names = ["Восток", "Север", "Запад", "Юг", "Центр"]

for i, ((target_x, target_y), direction) in enumerate(zip(directions_targets, direction_names)):
    print(f"\n--- ИССЛЕДОВАНИЕ: {direction.upper()} ({target_x}, {target_y}) ---")
    explorer.move_to_target(target_x, target_y)

explorer.show_info()

# ТЕСТ 4: Визуализация всех маршрутов
print("\n🧪 ТЕСТ 4: Визуализация навигации")

robots = [navigator, traveler, explorer]

plt.figure(figsize=(12, 10))

# Рисуем всех роботов
for robot in robots:
    if robot == traveler:
        robot.draw(targets=destinations)
    elif robot == explorer:
        robot.draw(targets=directions_targets)
    else:
        robot.draw(targets=[(5, 3)])

plt.grid(True, alpha=0.3)
plt.xlim(-1, 12)
plt.ylim(-1, 12)
plt.title("🧭 Навигационные маршруты роботов")
plt.xlabel("X координата")
plt.ylabel("Y координата")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Итоговая статистика
print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА НАВИГАЦИИ:")
total_steps = sum(robot.steps_made for robot in robots)
total_targets = sum(robot.targets_reached for robot in robots)

print(f"   🤖 Роботов-навигаторов: {len(robots)}")
print(f"   👣 Общее количество шагов: {total_steps}")
print(f"   🎯 Общее количество целей: {total_targets}")
print(f"   📊 Среднее шагов на цель: {total_steps/total_targets:.1f}")

# Самый эффективный навигатор
most_efficient = min(robots, key=lambda r: r.steps_made/max(r.targets_reached, 1))
print(f"   🏆 Самый эффективный: {most_efficient.name} ({most_efficient.steps_made/max(most_efficient.targets_reached, 1):.1f} шагов/цель)")

print(f"\n🎉 Навигационная система успешно протестирована!")
```

---

## ✅ Решение

```python
# Блок 4.1: Навигация к цели - роботы планируют маршрут! - РЕШЕНИЕ
# Учим роботов находить путь самостоятельно

import matplotlib.pyplot as plt
import math

class NavigatorRobot:
    """Робот-навигатор, который умеет планировать маршруты"""
    
    def __init__(self, name, start_x=0, start_y=0, color="blue"):
        self.name = name
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.color = color
        self.steps_made = 0
        self.path = [(start_x, start_y)]
        self.targets_reached = 0
        print(f"🧭 {name} готов к навигации из ({start_x}, {start_y})")
    
    def move_up(self):
        self.y += 1
        self.steps_made += 1
        self.path.append((self.x, self.y))
    
    def move_down(self):
        self.y -= 1
        self.steps_made += 1
        self.path.append((self.x, self.y))
    
    def move_left(self):
        self.x -= 1
        self.steps_made += 1
        self.path.append((self.x, self.y))
    
    def move_right(self):
        self.x += 1
        self.steps_made += 1
        self.path.append((self.x, self.y))
    
    def execute_command(self, command):
        """Выполняет одну команду"""
        if command == "up":
            self.move_up()
        elif command == "down":
            self.move_down()
        elif command == "left":
            self.move_left()
        elif command == "right":
            self.move_right()
    
    def calculate_distance(self, target_x, target_y):
        """Вычисляет расстояние до цели"""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        return distance
    
    def generate_path_commands(self, target_x, target_y):
        """Генерирует список команд для достижения цели"""
        commands = []
        
        # Вычисляем сколько шагов нужно по каждой оси
        dx = target_x - self.x
        dy = target_y - self.y
        
        print(f"📐 {self.name}: нужно пройти Δx={dx}, Δy={dy}")
        
        # Генерируем команды для движения по X
        if dx > 0:  # нужно идти вправо
            commands.extend(["right"] * dx)
        elif dx < 0:  # нужно идти влево
            commands.extend(["left"] * abs(dx))
        
        # Генерируем команды для движения по Y
        if dy > 0:  # нужно идти вверх
            commands.extend(["up"] * dy)
        elif dy < 0:  # нужно идти вниз  
            commands.extend(["down"] * abs(dy))
        
        return commands
    
    def move_to_target(self, target_x, target_y):
        """Главный метод: планирует и выполняет маршрут к цели"""
        print(f"\n🎯 {self.name} планирует маршрут из ({self.x}, {self.y}) в ({target_x}, {target_y})")
        
        # Вычисляем расстояние
        distance = self.calculate_distance(target_x, target_y)
        print(f"📏 Расстояние до цели: {distance:.2f}")
        
        # Генерируем команды
        commands = self.generate_path_commands(target_x, target_y)
        print(f"🗺️ План маршрута: {commands}")
        print(f"📊 Общее количество шагов: {len(commands)}")
        
        # Выполняем команды
        print(f"🚶 Начинаем движение...")
        for i, command in enumerate(commands):
            self.execute_command(command)
            if i < 5 or i == len(commands) - 1:  # показываем только первые 5 и последний
                print(f"   Шаг {i+1}: {command} → ({self.x}, {self.y})")
            elif i == 5:
                print(f"   ... (ещё {len(commands) - 6} шагов) ...")
        
        # Проверяем успех
        if self.x == target_x and self.y == target_y:
            self.targets_reached += 1
            print(f"✅ {self.name} достиг цели ({target_x}, {target_y})!")
        else:
            print(f"❌ {self.name} промахнулся! Цель: ({target_x}, {target_y}), факт: ({self.x}, {self.y})")
        
        return self.x == target_x and self.y == target_y
    
    def show_info(self):
        """Информация о навигаторе"""
        print(f"🧭 {self.name}:")
        print(f"   📍 Текущая позиция: ({self.x}, {self.y})")
        print(f"   🏠 Стартовая позиция: ({self.start_x}, {self.start_y})")
        print(f"   👣 Шагов сделано: {self.steps_made}")
        print(f"   🎯 Целей достигнуто: {self.targets_reached}")
    
    def draw(self, targets=None):
        """Рисует робота, его путь и цели"""
        # Путь робота
        if len(self.path) > 1:
            x_coords = [p[0] for p in self.path]
            y_coords = [p[1] for p in self.path]
            plt.plot(x_coords, y_coords, 
                    color=self.color, 
                    linewidth=2, 
                    alpha=0.7,
                    label=f'{self.name} путь')
        
        # Стартовая позиция
        plt.scatter(self.start_x, self.start_y, 
                   color=self.color, 
                   s=150, 
                   marker='^', 
                   alpha=0.8,
                   label=f'{self.name} старт')
        
        # Текущая позиция
        plt.scatter(self.x, self.y, 
                   color=self.color, 
                   s=200, 
                   marker='o',
                   alpha=0.9,
                   label=f'{self.name}')
        
        # Цели (если переданы)
        if targets:
            for i, (tx, ty) in enumerate(targets):
                plt.scatter(tx, ty, 
                           color='red', 
                           s=150, 
                           marker='*',
                           alpha=0.8)
                plt.annotate(f'Цель {i+1}', (tx, ty), 
                           xytext=(5, 5), 
                           textcoords='offset points')

# ТЕСТ 1: Простая навигация
print("🧪 ТЕСТ 1: Простая навигация к одной цели")

navigator = NavigatorRobot("Навигатор", 0, 0, "blue")

target_x, target_y = 5, 3
success = navigator.move_to_target(target_x, target_y)

navigator.show_info()
print(f"Результат: {'✅ Успех' if success else '❌ Неудача'}")

# ТЕСТ 2: Множественные цели
print("\n🧪 ТЕСТ 2: Путешествие по множественным целям")

traveler = NavigatorRobot("Путешественник", 0, 0, "green")

destinations = [(3, 4), (7, 2), (1, 6), (8, 8)]

print(f"🗺️ {traveler.name} должен посетить {len(destinations)} мест:")
for i, (x, y) in enumerate(destinations):
    print(f"   {i+1}. ({x}, {y})")

successful_trips = 0
for i, (target_x, target_y) in enumerate(destinations):
    print(f"\n--- ПОЕЗДКА {i+1} К ({target_x}, {target_y}) ---")
    success = traveler.move_to_target(target_x, target_y)
    if success:
        successful_trips += 1

traveler.show_info()
print(f"\n📊 Статистика путешествий:")
print(f"   🎯 Целей назначено: {len(destinations)}")
print(f"   ✅ Целей достигнуто: {successful_trips}")
print(f"   📈 Процент успеха: {successful_trips/len(destinations)*100:.1f}%")

# ТЕСТ 3: Навигация в разные стороны
print("\n🧪 ТЕСТ 3: Навигация во все стороны света")

explorer = NavigatorRobot("Исследователь", 5, 5, "red")

directions_targets = [
    (10, 5),  # восток
    (5, 10),  # север  
    (0, 5),   # запад
    (5, 0),   # юг
    (5, 5)    # возврат в центр
]

direction_names = ["Восток", "Север", "Запад", "Юг", "Центр"]

for i, ((target_x, target_y), direction) in enumerate(zip(directions_targets, direction_names)):
    print(f"\n--- ИССЛЕДОВАНИЕ: {direction.upper()} ({target_x}, {target_y}) ---")
    explorer.move_to_target(target_x, target_y)

explorer.show_info()

# ТЕСТ 4: Визуализация всех маршрутов
print("\n🧪 ТЕСТ 4: Визуализация навигации")

robots = [navigator, traveler, explorer]

plt.figure(figsize=(12, 10))

# Рисуем всех роботов
for robot in robots:
    if robot == traveler:
        robot.draw(targets=destinations)
    elif robot == explorer:
        robot.draw(targets=directions_targets)
    else:
        robot.draw(targets=[(5, 3)])

plt.grid(True, alpha=0.3)
plt.xlim(-1, 12)
plt.ylim(-1, 12)
plt.title("🧭 Навигационные маршруты роботов")
plt.xlabel("X координата")
plt.ylabel("Y координата")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Дополнительный тест: оптимизация маршрута
print(f"\n🚀 БОНУС: Анализ эффективности алгоритма")

# Сравним наш алгоритм с оптимальным расстоянием
for robot in robots:
    if robot.targets_reached > 0:
        avg_steps_per_target = robot.steps_made / robot.targets_reached
        print(f"📊 {robot.name}:")
        print(f"   Среднее шагов на цель: {avg_steps_per_target:.1f}")
        print(f"   Эффективность: {'Отлично' if avg_steps_per_target < 10 else 'Хорошо' if avg_steps_per_target < 15 else 'Можно лучше'}")

# Итоговая статистика
print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА НАВИГАЦИИ:")
total_steps = sum(robot.steps_made for robot in robots)
total_targets = sum(robot.targets_reached for robot in robots)

print(f"   🤖 Роботов-навигаторов: {len(robots)}")
print(f"   👣 Общее количество шагов: {total_steps}")
print(f"   🎯 Общее количество целей: {total_targets}")
print(f"   📊 Среднее шагов на цель: {total_steps/total_targets:.1f}")

# Самый эффективный навигатор
most_efficient = min(robots, key=lambda r: r.steps_made/max(r.targets_reached, 1))
print(f"   🏆 Самый эффективный: {most_efficient.name} ({most_efficient.steps_made/max(most_efficient.targets_reached, 1):.1f} шагов/цель)")

print(f"\n🎉 Навигационная система успешно протестирована!")
print(f"💡 Примечание: в реальности используются более сложные алгоритмы (A*, Dijkstra)")
```