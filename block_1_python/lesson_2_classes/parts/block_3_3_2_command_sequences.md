# Блок 3.3.2: Последовательности команд (4 мин)

## 📖 Текстовая ячейка (интро)

### 📋 Последовательности команд

Теперь, когда робот понимает отдельные команды, давайте научим его выполнять **списки команд**! Это как дать роботу план действий.

### 🎯 Квадрат из команд

Мы создадим квадрат, используя последовательность команд:
```python
square_commands = ["right", "right", "up", "up", "left", "left", "down", "down"]
robot.execute_sequence(square_commands)
```

### 🔄 Как работает execute_sequence()

Метод проходит по списку команд и выполняет каждую:
1. Берет команду из списка
2. Вызывает `execute_command()`
3. Переходит к следующей команде
4. Повторяет до конца списка

---

## 💻 Код для ученика

```python
# Блок 3.3.2: Последовательности команд
# Робот выполняет списки команд!

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
        
        # TODO: Выполните все команды из списка
        for i, command in enumerate(commands):
            print(f"  Команда {i+1}/{len(commands)}: {command}")
            self.___(___)  # вызовите execute_command
        
        print(f"✅ {self.name} выполнил все команды!")
    
    def show_info(self):
        """Подробная информация о роботе"""
        print(f"📊 {self.name}:")
        print(f"   📍 Позиция: ({self.x}, {self.y})")
        print(f"   🏠 Дом: ({self.start_x}, {self.start_y})")
        print(f"   👣 Шагов: {self.steps_made}")
        print(f"   📜 Команд выполнено: {len(self.commands_executed)}")
        if self.commands_executed:
            print(f"   🔤 Последние команды: {self.commands_executed[-5:]}")

# ТЕСТ: Последовательности команд
print("🧪 ТЕСТ: Последовательности команд")

# TODO: Создайте робота для последовательностей
sequence_robot = AdvancedRobot("Последователь", ___, ___, "green")

# Создаем команды для квадрата
square_commands = ["right", "right", "up", "up", "left", "left", "down", "down"]

print(f"\nРисуем квадрат:")
sequence_robot.execute_sequence(___)  # square_commands

print(f"\nТелепортируемся и рисуем еще один квадрат:")
sequence_robot.x, sequence_robot.y = 10, 10  # телепорт
sequence_robot.execute_sequence(___)  # square_commands

sequence_robot.show_info()

print(f"\n🎉 Робот умеет выполнять последовательности команд!")
```
