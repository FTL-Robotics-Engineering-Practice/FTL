# Блок 4.4: Границы мира (дополнительный)

## 📖 Текстовая ячейка (интро)

### 🌍 Реальные роботы имеют ограничения

В реальном мире роботы не могут двигаться бесконечно! Они ограничены:
- 🏠 **Стенами комнаты** 
- 🚧 **Препятствиями**
- 📏 **Размерами рабочей области**
- ⚠️ **Опасными зонами**

### 🗺️ Система границ

Мы создадим **виртуальный мир** с четкими границами:
- **Минимальные координаты**: (0, 0) - левый нижний угол
- **Максимальные координаты**: (width-1, height-1) - правый верхний угол
- **Проверка перед движением**: робот не может выйти за границы

### 🚨 Обработка попыток нарушения

Когда робот пытается выйти за границы:
1. **Предупреждение** - сообщить о попытке
2. **Блокировка** - не выполнять движение
3. **Логирование** - записать попытку нарушения
4. **Альтернатива** - предложить безопасное направление

### 🎯 Умная навигация

Продвинутые роботы должны:
- **Планировать безопасные маршруты**
- **Избегать границ заранее**
- **Находить обходные пути**
- **Адаптироваться к размеру мира**

### 🧪 Тестирование границ

Мы протестируем:
- Попытки выхода в каждом направлении
- Движение по периметру мира
- Навигацию в ограниченном пространстве
- Поведение при "загнанности в угол"

---

## 💻 Код для ученика

```python
# Блок 4.4: Границы мира - роботы учатся уважать пределы!
# Создаем безопасную рабочую область для роботов

import matplotlib.pyplot as plt
import matplotlib.patches as patches

class BoundedRobot:
    """Робот, который знает границы своего мира"""
    
    def __init__(self, name, start_x=0, start_y=0, world_width=10, world_height=8, color="blue"):
        self.name = name
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.color = color
        
        # Границы мира
        self.world_width = world_width
        self.world_height = world_height
        self.min_x = 0
        self.min_y = 0
        self.max_x = world_width - 1
        self.max_y = world_height - 1
        
        # Статистика
        self.steps_made = 0
        self.boundary_violations = 0
        self.path = [(start_x, start_y)]
        self.violation_attempts = []
        
        print(f"🌍 {name} создан в мире {world_width}x{world_height}, позиция ({start_x}, {start_y})")
        
        # Проверим, что стартовая позиция корректна
        if not self.is_position_valid(start_x, start_y):
            print(f"⚠️ ВНИМАНИЕ: {name} создан вне границ мира!")
    
    def is_position_valid(self, x, y):
        """Проверяет, находится ли позиция в границах мира"""
        # TODO: Реализуйте проверку границ
        return (self.min_x <= x <= self.max_x) and (self.min_y <= y <= self.max_y)
    
    def get_world_info(self):
        """Возвращает информацию о мире"""
        return {
            'width': self.world_width,
            'height': self.world_height,
            'min_coords': (self.min_x, self.min_y),
            'max_coords': (self.max_x, self.max_y),
            'total_cells': self.world_width * self.world_height
        }
    
    def safe_move(self, direction):
        """Безопасное движение с проверкой границ"""
        # Вычисляем новую позицию
        new_x, new_y = self.x, self.y
        
        # TODO: Вычислите новые координаты в зависимости от направления
        if direction == "up":
            new_y = self.y + ___
        elif direction == "down":
            new_y = self.y - ___
        elif direction == "left":
            new_x = self.x - ___
        elif direction == "right":
            new_x = self.x + ___
        else:
            print(f"❓ {self.name}: Неизвестное направление '{direction}'")
            return False
        
        # TODO: Проверьте, можно ли двигаться в новую позицию
        if self.is_position_valid(___, ___):
            # Движение разрешено
            self.x = new_x
            self.y = new_y
            self.steps_made += 1
            self.path.append((self.x, self.y))
            print(f"✅ {self.name} {direction} → ({self.x}, {self.y})")
            return True
        else:
            # Движение заблокировано
            self.boundary_violations += 1
            self.violation_attempts.append({
                'attempted_position': (new_x, new_y),
                'direction': direction,
                'current_position': (self.x, self.y)
            })
            print(f"🚫 {self.name}: Нельзя идти {direction}! Граница мира в ({new_x}, {new_y})")
            return False
    
    def explore_boundaries(self):
        """Исследует границы мира во всех направлениях"""
        print(f"\n🧭 {self.name} исследует границы мира...")
        
        directions = ["up", "down", "left", "right"]
        
        for direction in directions:
            print(f"\nПроба движения: {direction}")
            success = self.safe_move(direction)
            
            if not success:
                print(f"   Граница обнаружена в направлении {direction}")
            else:
                # Возвращаемся назад, если движение было успешным
                opposite = {"up": "down", "down": "up", "left": "right", "right": "left"}
                self.safe_move(opposite[direction])
                print(f"   Возвращаемся обратно")
    
    def walk_perimeter(self):
        """Обходит по периметру мира (если возможно)"""
        print(f"\n🔄 {self.name} пытается обойти по периметру...")
        
        # Идем в левый нижний угол
        while self.x > self.min_x:
            if not self.safe_move("left"):
                break
        while self.y > self.min_y:
            if not self.safe_move("down"):
                break
        
        print(f"Стартовая позиция для периметра: ({self.x}, {self.y})")
        
        # TODO: Реализуйте обход по периметру
        # 1. Идем вправо до границы
        while self.x < self.max_x:
            if not self.safe_move("___"):
                break
        
        # 2. Идем вверх до границы
        while self.y < self.max_y:
            if not self.safe_move("___"):
                break
        
        # 3. Идем влево до границы
        while self.x > self.min_x:
            if not self.safe_move("___"):
                break
        
        # 4. Идем вниз до границы
        while self.y > self.min_y:
            if not self.safe_move("___"):
                break
        
        print(f"✅ Обход периметра завершен!")
    
    def find_safe_direction(self):
        """Находит безопасное направление для движения"""
        safe_directions = []
        
        # TODO: Проверьте все направления и найдите безопасные
        directions = ["up", "down", "left", "right"]
        
        for direction in directions:
            # Вычисляем потенциальную новую позицию
            test_x, test_y = self.x, self.y
            
            if direction == "up":
                test_y += 1
            elif direction == "down":
                test_y -= 1
            elif direction == "left":
                test_x -= 1
            elif direction == "right":
                test_x += 1
            
            # Проверяем безопасность
            if self.is_position_valid(test_x, test_y):
                safe_directions.append(direction)
        
        return safe_directions
    
    def smart_navigate_to(self, target_x, target_y):
        """Умная навигация с учетом границ"""
        print(f"\n🎯 {self.name} навигирует к ({target_x}, {target_y})")
        
        # Проверяем, что цель в пределах мира
        if not self.is_position_valid(target_x, target_y):
            print(f"❌ Цель ({target_x}, {target_y}) вне границ мира!")
            return False
        
        max_attempts = 100  # защита от бесконечного цикла
        attempts = 0
        
        while (self.x != target_x or self.y != target_y) and attempts < max_attempts:
            attempts += 1
            
            # Определяем направление к цели
            if self.x < target_x:
                if self.safe_move("right"):
                    continue
            elif self.x > target_x:
                if self.safe_move("left"):
                    continue
            
            if self.y < target_y:
                if self.safe_move("up"):
                    continue
            elif self.y > target_y:
                if self.safe_move("down"):
                    continue
            
            # Если прямое движение невозможно, ищем обходной путь
            safe_dirs = self.find_safe_direction()
            if safe_dirs:
                print(f"🔄 Обходной маневр: {safe_dirs[0]}")
                self.safe_move(safe_dirs[0])
            else:
                print(f"🚫 {self.name} заблокирован! Нет доступных направлений.")
                break
        
        if self.x == target_x and self.y == target_y:
            print(f"✅ {self.name} достиг цели за {attempts} попыток!")
            return True
        else:
            print(f"❌ {self.name} не смог достичь цели за {max_attempts} попыток")
            return False
    
    def show_statistics(self):
        """Показывает статистику взаимодействия с границами"""
        world_info = self.get_world_info()
        
        print(f"\n📊 СТАТИСТИКА ГРАНИЦ - {self.name}:")
        print(f"   🌍 Размер мира: {world_info['width']}x{world_info['height']} ({world_info['total_cells']} клеток)")
        print(f"   📍 Текущая позиция: ({self.x}, {self.y})")
        print(f"   👣 Успешных шагов: {self.steps_made}")
        print(f"   🚫 Нарушений границ: {self.boundary_violations}")
        
        if self.boundary_violations > 0:
            print(f"   📋 Подробности нарушений:")
            for i, violation in enumerate(self.violation_attempts):
                print(f"      {i+1}. {violation['direction']} из {violation['current_position']} → {violation['attempted_position']}")
    
    def draw_world_and_path(self):
        """Рисует мир с границами и путь робота"""
        plt.figure(figsize=(10, 8))
        
        # Рисуем границы мира
        world_rect = patches.Rectangle(
            (self.min_x - 0.5, self.min_y - 0.5),
            self.world_width, self.world_height,
            linewidth=3, edgecolor='black', facecolor='lightgray', alpha=0.3
        )
        plt.gca().add_patch(world_rect)
        
        # Рисуем сетку
        for x in range(self.min_x, self.max_x + 2):
            plt.axvline(x - 0.5, color='gray', alpha=0.5, linewidth=0.5)
        for y in range(self.min_y, self.max_y + 2):
            plt.axhline(y - 0.5, color='gray', alpha=0.5, linewidth=0.5)
        
        # Путь робота
        if len(self.path) > 1:
            x_coords = [p[0] for p in self.path]
            y_coords = [p[1] for p in self.path]
            plt.plot(x_coords, y_coords, 
                    color=self.color, linewidth=2, alpha=0.8, label=f'Путь {self.name}')
        
        # Позиции
        plt.scatter(self.start_x, self.start_y, color='green', s=200, marker='^', label='Старт', zorder=5)
        plt.scatter(self.x, self.y, color=self.color, s=200, marker='o', label=f'{self.name}', zorder=5)
        
        # Попытки нарушения границ
        for violation in self.violation_attempts:
            vx, vy = violation['attempted_position']
            plt.scatter(vx, vy, color='red', s=100, marker='x', alpha=0.7, zorder=5)
        
        plt.xlim(self.min_x - 1, self.max_x + 1)
        plt.ylim(self.min_y - 1, self.max_y + 1)
        plt.title(f"Мир {self.name} ({self.world_width}x{self.world_height})")
        plt.xlabel("X координата")
        plt.ylabel("Y координата")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axis('equal')

# ТЕСТ 1: Исследование границ
print("🧪 ТЕСТ 1: Исследование границ мира")

# TODO: Создайте робота в маленьком мире
explorer = BoundedRobot("___", ___, ___, world_width=___, world_height=___, color="blue")

# Показать информацию о мире
world_info = explorer.get_world_info()
print(f"Мир: {world_info}")

# TODO: Исследуйте границы
explorer.___()

explorer.show_statistics()

# ТЕСТ 2: Обход по периметру
print("\n🧪 ТЕСТ 2: Обход по периметру")

# TODO: Создайте робота для обхода периметра
perimeter_walker = BoundedRobot("___", ___, ___, world_width=___, world_height=___, color="green")

# TODO: Обойдите по периметру
perimeter_walker.___()

perimeter_walker.show_statistics()

# ТЕСТ 3: Умная навигация
print("\n🧪 ТЕСТ 3: Умная навигация в ограниченном пространстве")

# TODO: Создайте робота-навигатора
navigator = BoundedRobot("___", ___, ___, world_width=___, world_height=___, color="red")

# Несколько целей для навигации
targets = [(7, 5), (1, 6), (8, 1), (4, 7)]

print(f"Цели для навигации: {targets}")

# TODO: Навигируйте ко всем целям
for i, (target_x, target_y) in enumerate(targets):
    print(f"\n--- ЦЕЛЬ {i+1}: ({target_x}, {target_y}) ---")
    success = navigator.smart_navigate_to(___, ___)
    if not success:
        print(f"Останавливаемся на неудачной цели")
        break

navigator.show_statistics()

# ТЕСТ 4: Экстремальные условия
print("\n🧪 ТЕСТ 4: Роботы в экстремально маленьком мире")

# TODO: Создайте робота в мире 3x3
tiny_robot = BoundedRobot("___", ___, ___, world_width=___, world_height=___, color="purple")

print("Тест движения в крошечном мире:")
# Попытки движения в разные стороны
directions = ["up", "right", "down", "left", "up", "up", "right", "right"]

for direction in directions:
    tiny_robot.safe_move(direction)

tiny_robot.show_statistics()

# ВИЗУАЛИЗАЦИЯ
print("\n🎨 ВИЗУАЛИЗАЦИЯ ГРАНИЦ МИРА:")

# Рисуем все миры
plt.figure(figsize=(15, 10))

plt.subplot(2, 2, 1)
explorer.draw_world_and_path()

plt.subplot(2, 2, 2)
perimeter_walker.draw_world_and_path()

plt.subplot(2, 2, 3)
navigator.draw_world_and_path()

plt.subplot(2, 2, 4)
tiny_robot.draw_world_and_path()

plt.tight_layout()
plt.show()

# Итоговая статистика
print(f"\n📈 ИТОГОВАЯ СТАТИСТИКА ГРАНИЦ:")
all_robots = [explorer, perimeter_walker, navigator, tiny_robot]

total_steps = sum(robot.steps_made for robot in all_robots)
total_violations = sum(robot.boundary_violations for robot in all_robots)

print(f"   🤖 Роботов протестировано: {len(all_robots)}")
print(f"   👣 Общее количество шагов: {total_steps}")
print(f"   🚫 Общее нарушений границ: {total_violations}")
print(f"   📊 Процент нарушений: {total_violations/(total_steps + total_violations)*100:.1f}%")

# Самый дисциплинированный робот
most_disciplined = min(all_robots, key=lambda r: r.boundary_violations)
print(f"   🏆 Самый дисциплинированный: {most_disciplined.name} ({most_disciplined.boundary_violations} нарушений)")

print(f"\n🎉 Система границ успешно внедрена!")
print(f"💡 Роботы теперь уважают пределы своего мира!")
```

---

## ✅ Решение

```python
# Блок 4.4: Границы мира - роботы учатся уважать пределы! - РЕШЕНИЕ
# Создаем безопасную рабочую область для роботов

import matplotlib.pyplot as plt
import matplotlib.patches as patches

class BoundedRobot:
    """Робот, который знает границы своего мира"""
    
    def __init__(self, name, start_x=0, start_y=0, world_width=10, world_height=8, color="blue"):
        self.name = name
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.color = color
        
        # Границы мира
        self.world_width = world_width
        self.world_height = world_height
        self.min_x = 0
        self.min_y = 0
        self.max_x = world_width - 1
        self.max_y = world_height - 1
        
        # Статистика
        self.steps_made = 0
        self.boundary_violations = 0
        self.path = [(start_x, start_y)]
        self.violation_attempts = []
        
        print(f"🌍 {name} создан в мире {world_width}x{world_height}, позиция ({start_x}, {start_y})")
        
        # Проверим, что стартовая позиция корректна
        if not self.is_position_valid(start_x, start_y):
            print(f"⚠️ ВНИМАНИЕ: {name} создан вне границ мира!")
    
    def is_position_valid(self, x, y):
        """Проверяет, находится ли позиция в границах мира"""
        return (self.min_x <= x <= self.max_x) and (self.min_y <= y <= self.max_y)
    
    def get_world_info(self):
        """Возвращает информацию о мире"""
        return {
            'width': self.world_width,
            'height': self.world_height,
            'min_coords': (self.min_x, self.min_y),
            'max_coords': (self.max_x, self.max_y),
            'total_cells': self.world_width * self.world_height
        }
    
    def safe_move(self, direction):
        """Безопасное движение с проверкой границ"""
        # Вычисляем новую позицию
        new_x, new_y = self.x, self.y
        
        if direction == "up":
            new_y = self.y + 1
        elif direction == "down":
            new_y = self.y - 1
        elif direction == "left":
            new_x = self.x - 1
        elif direction == "right":
            new_x = self.x + 1
        else:
            print(f"❓ {self.name}: Неизвестное направление '{direction}'")
            return False
        
        # Проверяем, можно ли двигаться в новую позицию
        if self.is_position_valid(new_x, new_y):
            # Движение разрешено
            self.x = new_x
            self.y = new_y
            self.steps_made += 1
            self.path.append((self.x, self.y))
            print(f"✅ {self.name} {direction} → ({self.x}, {self.y})")
            return True
        else:
            # Движение заблокировано
            self.boundary_violations += 1
            self.violation_attempts.append({
                'attempted_position': (new_x, new_y),
                'direction': direction,
                'current_position': (self.x, self.y)
            })
            print(f"🚫 {self.name}: Нельзя идти {direction}! Граница мира в ({new_x}, {new_y})")
            return False
    
    def explore_boundaries(self):
        """Исследует границы мира во всех направлениях"""
        print(f"\n🧭 {self.name} исследует границы мира...")
        
        directions = ["up", "down", "left", "right"]
        
        for direction in directions:
            print(f"\nПроба движения: {direction}")
            success = self.safe_move(direction)
            
            if not success:
                print(f"   Граница обнаружена в направлении {direction}")
            else:
                # Возвращаемся назад, если движение было успешным
                opposite = {"up": "down", "down": "up", "left": "right", "right": "left"}
                self.safe_move(opposite[direction])
                print(f"   Возвращаемся обратно")
    
    def walk_perimeter(self):
        """Обходит по периметру мира (если возможно)"""
        print(f"\n🔄 {self.name} пытается обойти по периметру...")
        
        # Идем в левый нижний угол
        while self.x > self.min_x:
            if not self.safe_move("left"):
                break
        while self.y > self.min_y:
            if not self.safe_move("down"):
                break
        
        print(f"Стартовая позиция для периметра: ({self.x}, {self.y})")
        
        # 1. Идем вправо до границы
        while self.x < self.max_x:
            if not self.safe_move("right"):
                break
        
        # 2. Идем вверх до границы
        while self.y < self.max_y:
            if not self.safe_move("up"):
                break
        
        # 3. Идем влево до границы
        while self.x > self.min_x:
            if not self.safe_move("left"):
                break
        
        # 4. Идем вниз до границы
        while self.y > self.min_y:
            if not self.safe_move("down"):
                break
        
        print(f"✅ Обход периметра завершен!")
    
    def find_safe_direction(self):
        """Находит безопасное направление для движения"""
        safe_directions = []
        
        directions = ["up", "down", "left", "right"]
        
        for direction in directions:
            # Вычисляем потенциальную новую позицию
            test_x, test_y = self.x, self.y
            
            if direction == "up":
                test_y += 1
            elif direction == "down":
                test_y -= 1
            elif direction == "left":
                test_x -= 1
            elif direction == "right":
                test_x += 1
            
            # Проверяем безопасность
            if self.is_position_valid(test_x, test_y):
                safe_directions.append(direction)
        
        return safe_directions
    
    def smart_navigate_to(self, target_x, target_y):
        """Умная навигация с учетом границ"""
        print(f"\n🎯 {self.name} навигирует к ({target_x}, {target_y})")
        
        # Проверяем, что цель в пределах мира
        if not self.is_position_valid(target_x, target_y):
            print(f"❌ Цель ({target_x}, {target_y}) вне границ мира!")
            return False
        
        max_attempts = 100  # защита от бесконечного цикла
        attempts = 0
        
        while (self.x != target_x or self.y != target_y) and attempts < max_attempts:
            attempts += 1
            
            # Определяем направление к цели
            if self.x < target_x:
                if self.safe_move("right"):
                    continue
            elif self.x > target_x:
                if self.safe_move("left"):
                    continue
            
            if self.y < target_y:
                if self.safe_move("up"):
                    continue
            elif self.y > target_y:
                if self.safe_move("down"):
                    continue
            
            # Если прямое движение невозможно, ищем обходной путь
            safe_dirs = self.find_safe_direction()
            if safe_dirs:
                print(f"🔄 Обходной маневр: {safe_dirs[0]}")
                self.safe_move(safe_dirs[0])
            else:
                print(f"🚫 {self.name} заблокирован! Нет доступных направлений.")
                break
        
        if self.x == target_x and self.y == target_y:
            print(f"✅ {self.name} достиг цели за {attempts} попыток!")
            return True
        else:
            print(f"❌ {self.name} не смог достичь цели за {max_attempts} попыток")
            return False
    
    def show_statistics(self):
        """Показывает статистику взаимодействия с границами"""
        world_info = self.get_world_info()
        
        print(f"\n📊 СТАТИСТИКА ГРАНИЦ - {self.name}:")
        print(f"   🌍 Размер мира: {world_info['width']}x{world_info['height']} ({world_info['total_cells']} клеток)")
        print(f"   📍 Текущая позиция: ({self.x}, {self.y})")
        print(f"   👣 Успешных шагов: {self.steps_made}")
        print(f"   🚫 Нарушений границ: {self.boundary_violations}")
        
        if self.boundary_violations > 0:
            print(f"   📋 Подробности нарушений:")
            for i, violation in enumerate(self.violation_attempts):
                print(f"      {i+1}. {violation['direction']} из {violation['current_position']} → {violation['attempted_position']}")
    
    def draw_world_and_path(self):
        """Рисует мир с границами и путь робота"""
        # Рисуем границы мира
        world_rect = patches.Rectangle(
            (self.min_x - 0.5, self.min_y - 0.5),
            self.world_width, self.world_height,
            linewidth=3, edgecolor='black', facecolor='lightgray', alpha=0.3
        )
        plt.gca().add_patch(world_rect)
        
        # Рисуем сетку
        for x in range(self.min_x, self.max_x + 2):
            plt.axvline(x - 0.5, color='gray', alpha=0.5, linewidth=0.5)
        for y in range(self.min_y, self.max_y + 2):
            plt.axhline(y - 0.5, color='gray', alpha=0.5, linewidth=0.5)
        
        # Путь робота
        if len(self.path) > 1:
            x_coords = [p[0] for p in self.path]
            y_coords = [p[1] for p in self.path]
            plt.plot(x_coords, y_coords, 
                    color=self.color, linewidth=2, alpha=0.8, label=f'Путь {self.name}')
        
        # Позиции
        plt.scatter(self.start_x, self.start_y, color='green', s=200, marker='^', label='Старт', zorder=5)
        plt.scatter(self.x, self.y, color=self.color, s=200, marker='o', label=f'{self.name}', zorder=5)
        
        # Попытки нарушения границ
        for violation in self.violation_attempts:
            vx, vy = violation['attempted_position']
            plt.scatter(vx, vy, color='red', s=100, marker='x', alpha=0.7, zorder=5)
        
        plt.xlim(self.min_x - 1, self.max_x + 1)
        plt.ylim(self.min_y - 1, self.max_y + 1)
        plt.title(f"Мир {self.name} ({self.world_width}x{self.world_height})")
        plt.xlabel("X координата")
        plt.ylabel("Y координата")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axis('equal')

# ТЕСТ 1: Исследование границ
print("🧪 ТЕСТ 1: Исследование границ мира")

explorer = BoundedRobot("Исследователь", 2, 2, world_width=6, world_height=5, color="blue")

# Показать информацию о мире
world_info = explorer.get_world_info()
print(f"Мир: {world_info}")

explorer.explore_boundaries()
explorer.show_statistics()

# ТЕСТ 2: Обход по периметру
print("\n🧪 ТЕСТ 2: Обход по периметру")

perimeter_walker = BoundedRobot("Обходчик", 3, 3, world_width=8, world_height=6, color="green")

perimeter_walker.walk_perimeter()
perimeter_walker.show_statistics()

# ТЕСТ 3: Умная навигация
print("\n🧪 ТЕСТ 3: Умная навигация в ограниченном пространстве")

navigator = BoundedRobot("Навигатор", 1, 1, world_width=10, world_height=8, color="red")

# Несколько целей для навигации
targets = [(7, 5), (1, 6), (8, 1), (4, 7)]

print(f"Цели для навигации: {targets}")

for i, (target_x, target_y) in enumerate(targets):
    print(f"\n--- ЦЕЛЬ {i+1}: ({target_x}, {target_y}) ---")
    success = navigator.smart_navigate_to(target_x, target_y)
    if not success:
        print(f"Останавливаемся на неудачной цели")
        break

navigator.show_statistics()

# ТЕСТ 4: Экстремальные условия
print("\n🧪 ТЕСТ 4: Роботы в экстремально маленьком мире")

tiny_robot = BoundedRobot("Малыш", 1, 1, world_width=3, world_height=3, color="purple")

print("Тест движения в крошечном мире:")
# Попытки движения в разные стороны
directions = ["up", "right", "down", "left", "up", "up", "right", "right"]

for direction in directions:
    tiny_robot.safe_move(direction)

tiny_robot.show_statistics()

# ДОПОЛНИТЕЛЬНЫЙ ТЕСТ: Робот в углу
print("\n🧪 ДОПОЛНИТЕЛЬНЫЙ ТЕСТ: Робот заперт в углу")

corner_robot = BoundedRobot("Угловой", 0, 0, world_width=5, world_height=5, color="orange")

# Пытаемся выйти из угла
escape_attempts = ["left", "down", "up", "right", "up", "right"]
for direction in escape_attempts:
    corner_robot.safe_move(direction)

corner_robot.show_statistics()

# ВИЗУАЛИЗАЦИЯ
print("\n🎨 ВИЗУАЛИЗАЦИЯ ГРАНИЦ МИРА:")

plt.figure(figsize=(15, 10))

plt.subplot(2, 3, 1)
explorer.draw_world_and_path()

plt.subplot(2, 3, 2)
perimeter_walker.draw_world_and_path()

plt.subplot(2, 3, 3)
navigator.draw_world_and_path()

plt.subplot(2, 3, 4)
tiny_robot.draw_world_and_path()

plt.subplot(2, 3, 5)
corner_robot.draw_world_and_path()

# Сравнительная диаграмма нарушений
plt.subplot(2, 3, 6)
all_robots = [explorer, perimeter_walker, navigator, tiny_robot, corner_robot]
robot_names = [robot.name for robot in all_robots]
violations = [robot.boundary_violations for robot in all_robots]

plt.bar(robot_names, violations, color=['blue', 'green', 'red', 'purple', 'orange'])
plt.title("Нарушения границ по роботам")
plt.xlabel("Роботы")
plt.ylabel("Количество нарушений")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Итоговая статистика
print(f"\n📈 ИТОГОВАЯ СТАТИСТИКА ГРАНИЦ:")

total_steps = sum(robot.steps_made for robot in all_robots)
total_violations = sum(robot.boundary_violations for robot in all_robots)

print(f"   🤖 Роботов протестировано: {len(all_robots)}")
print(f"   👣 Общее количество шагов: {total_steps}")
print(f"   🚫 Общее нарушений границ: {total_violations}")
if total_steps + total_violations > 0:
    print(f"   📊 Процент нарушений: {total_violations/(total_steps + total_violations)*100:.1f}%")

# Самый дисциплинированный робот
most_disciplined = min(all_robots, key=lambda r: r.boundary_violations)
print(f"   🏆 Самый дисциплинированный: {most_disciplined.name} ({most_disciplined.boundary_violations} нарушений)")

# Самый активный робот
most_active = max(all_robots, key=lambda r: r.steps_made)
print(f"   🏃 Самый активный: {most_active.name} ({most_active.steps_made} шагов)")

print(f"\n🎉 Система границ успешно внедрена!")
print(f"💡 Роботы теперь уважают пределы своего мира!")
```