# Блок 3.3.3: Визуализация продвинутых роботов (3 мин)

## 📖 Текстовая ячейка (интро)

### 🎨 Рисуем пути роботов

Теперь, когда наши роботы умеют выполнять команды, давайте посмотрим на их **пути**! Мы научимся рисовать:
- Текущую позицию робота
- Весь путь, который он прошел
- Красивые подписи и легенды

### 📊 Метод draw()

Робот будет рисовать:
1. **Линию пути** - показывает весь маршрут
2. **Текущую позицию** - где робот находится сейчас
3. **Подпись** - имя и координаты

### 🎯 Визуализация множественных роботов

Мы создадим несколько роботов с разными цветами и посмотрим, как они работают вместе!

---

## 💻 Код для ученика

```python
# Блок 3.3.3: Визуализация продвинутых роботов
# Рисуем пути и позиции роботов!

import matplotlib.pyplot as plt

class AdvancedRobot:
    """Продвинутый робот с умными методами"""
    
    def __init__(self, name, start_x=0, start_y=0, color="blue"):
        self.name = name
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.color = color
        self.steps_made = 0
        self.path = [(start_x, start_y)]
        self.commands_executed = []  # история команд
        print(f"🤖 {name} готов к приему команд!")
    
    def move_up(self):
        """Шаг вверх"""
        self.y += 1
        self.steps_made += 1
        self.path.append((self.x, self.y))
        print(f"⬆️ {self.name} идет вверх → ({self.x}, {self.y})")
    
    def move_down(self):
        """Шаг вниз"""
        self.y -= 1
        self.steps_made += 1
        self.path.append((self.x, self.y))
        print(f"⬇️ {self.name} идет вниз → ({self.x}, {self.y})")
    
    def move_left(self):
        """Шаг влево"""
        self.x -= 1
        self.steps_made += 1
        self.path.append((self.x, self.y))
        print(f"⬅️ {self.name} идет влево → ({self.x}, {self.y})")
    
    def move_right(self):
        """Шаг вправо"""
        self.x += 1
        self.steps_made += 1
        self.path.append((self.x, self.y))
        print(f"➡️ {self.name} идет вправо → ({self.x}, {self.y})")
    
    def execute_command(self, command):
        """Переводчик: превращает слова в действия"""
        # Сохраняем команду в истории
        self.commands_executed.append(command)
        
        if command == "up":
            self.move_up()
        elif command == "down":
            self.move_down()
        elif command == "left":
            self.move_left()
        elif command == "right":
            self.move_right()
        else:
            print(f"❓ {self.name}: Не знаю команду '{command}'!")
            print(f"   Доступные команды: up, down, left, right")
    
    def execute_sequence(self, commands):
        """Выполняет список команд"""
        print(f"📋 {self.name} получил {len(commands)} команд: {commands}")
        
        # Выполняем все команды из списка
        for i, command in enumerate(commands):
            print(f"  Команда {i+1}/{len(commands)}: {command}")
            self.execute_command(command)
        
        print(f"✅ {self.name} выполнил все команды!")
    
    def draw(self):
        """Рисует робота и его путь"""
        # TODO: Нарисуйте путь робота
        if len(self.path) > 1:
            x_coords = [p[0] for p in self.path]
            y_coords = [p[1] for p in self.path]
            plt.plot(x_coords, y_coords, 
                    color=self.___, 
                    linewidth=2, 
                    alpha=0.6, 
                    linestyle='--')
        
        # TODO: Нарисуйте текущую позицию
        plt.scatter(self.___, self.___, 
                   color=self.___, 
                   s=200, 
                   alpha=0.9,
                   label=self.name)
        
        # TODO: Добавьте подпись
        plt.annotate(f'{self.name}\n({self.x},{self.y})', 
                    (self.___, self.___), 
                    xytext=(10, 10), 
                    textcoords='offset points',
                    fontsize=9)
    
    def show_info(self):
        """Подробная информация о роботе"""
        print(f"📊 {self.name}:")
        print(f"   📍 Позиция: ({self.x}, {self.y})")
        print(f"   🏠 Дом: ({self.start_x}, {self.start_y})")
        print(f"   👣 Шагов: {self.steps_made}")
        print(f"   📜 Команд выполнено: {len(self.commands_executed)}")
        if self.commands_executed:
            print(f"   🔤 Последние команды: {self.commands_executed[-5:]}")

# ТЕСТ: Визуализация всех роботов
print("🧪 ТЕСТ: Визуализация результатов")

# Создаем разных роботов
test_robot = AdvancedRobot("Тестер", 0, 0, "red")
translator_robot = AdvancedRobot("Переводчик", 5, 5, "blue")
sequence_robot = AdvancedRobot("Последователь", 10, 10, "green")

# Даем им разные задания
test_robot.move_up()
test_robot.move_right()

translator_robot.execute_command("up")
translator_robot.execute_command("right")

square_commands = ["right", "right", "up", "up", "left", "left", "down", "down"]
sequence_robot.execute_sequence(square_commands)

# Рисуем всех роботов
robots = [test_robot, translator_robot, sequence_robot]

plt.figure(figsize=(12, 8))

# TODO: Нарисуйте всех роботов в цикле
for robot in robots:
    robot.___()

plt.grid(True, alpha=0.3)
plt.xlim(-2, 15)
plt.ylim(-2, 15)
plt.title("🤖 Продвинутые роботы и их пути")
plt.xlabel("X координата")
plt.ylabel("Y координата")
plt.legend()
plt.show()

# Итоговая статистика
print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
total_steps = sum(robot.steps_made for robot in robots)
total_commands = sum(len(robot.commands_executed) for robot in robots)

print(f"   🤖 Роботов протестировано: {len(robots)}")
print(f"   👣 Общее количество шагов: {total_steps}")
print(f"   📜 Общее количество команд: {total_commands}")
print(f"   📊 Среднее шагов на робота: {total_steps/len(robots):.1f}")

print(f"\n🎉 Все тесты пройдены! Роботы стали умнее!")
```
