# Блок 3.3.1: Переводчик команд (8 мин)

## 📖 Текстовая ячейка (интро)

### 🗣️ Переводчик команд

До сих пор мы вызывали методы напрямую: `robot.move_right()`. Но настоящие роботы должны понимать **слова**! Нужен переводчик, который превращает слова в действия.

### 🎯 Четыре основных направления

Каждый робот должен уметь:
- **move_up()** - шаг вверх (Y увеличивается)
- **move_down()** - шаг вниз (Y уменьшается)  
- **move_left()** - шаг влево (X уменьшается)
- **move_right()** - шаг вправо (X увеличивается)

### 🔄 Как работает переводчик

```python
robot.execute_command("up")    # → robot.move_up()
robot.execute_command("right") # → robot.move_right()
```

### ⚠️ Обработка ошибок

Что если дать роботу неизвестную команду? Хороший робот должен:
1. Сообщить об ошибке
2. Продолжить работу  
3. Не сломаться

---

## 💻 Код для ученика

```python
# Блок 3.3.1: Переводчик команд
# Создаем робота, который понимает слова!

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
    
    # TODO: Создайте четыре метода движения
    def move_up(self):
        """Шаг вверх"""
        self.y += ___  # какую координату менять?
        self.steps_made += 1
        self.path.append((self.x, self.y))
        print(f"⬆️ {self.name} идет вверх → ({self.x}, {self.y})")
    
    def move_down(self):
        """Шаг вниз"""
        # TODO: Реализуйте движение вниз
        self.y -= ___
        self.steps_made += 1
        self.path.append((self.x, self.y))
        print(f"⬇️ {self.name} идет вниз → ({self.x}, {self.y})")
    
    def move_left(self):
        """Шаг влево"""
        # TODO: Реализуйте движение влево
        self.___ -= 1
        self.steps_made += 1
        self.path.append((self.x, self.y))
        print(f"⬅️ {self.name} идет влево → ({self.x}, {self.y})")
    
    def move_right(self):
        """Шаг вправо"""
        # TODO: Реализуйте движение вправо
        self.___ += ___
        self.steps_made += 1
        self.path.append((self.x, self.y))
        print(f"➡️ {self.name} идет вправо → ({self.x}, {self.y})")
    
    def execute_command(self, command):
        """Переводчик: превращает слова в действия"""
        # TODO: Реализуйте переводчик команд
        
        # Сохраняем команду в истории
        self.commands_executed.append(command)
        
        if command == "up":
            self.___()
        elif command == "down":
            self.___()
        elif command == "left":
            self.___()
        elif command == "right":
            self.___()
        else:
            # TODO: Обработайте неизвестную команду
            print(f"❓ {self.name}: Не знаю команду '{command}'!")
            print(f"   Доступные команды: up, down, left, right")
    
    def show_info(self):
        """Подробная информация о роботе"""
        print(f"📊 {self.name}:")
        print(f"   📍 Позиция: ({self.x}, {self.y})")
        print(f"   🏠 Дом: ({self.start_x}, {self.start_y})")
        print(f"   👣 Шагов: {self.steps_made}")
        print(f"   📜 Команд выполнено: {len(self.commands_executed)}")
        if self.commands_executed:
            print(f"   🔤 Последние команды: {self.commands_executed[-5:]}")

# ТЕСТ 1: Основные движения
print("🧪 ТЕСТ 1: Проверяем основные движения")

# TODO: Создайте робота для тестирования
test_robot = AdvancedRobot("Тестер", ___, ___, "red")

# Тестируем каждое направление
print("\nТестируем все направления:")
test_robot.move_up()
test_robot.move_right()
test_robot.move_down()
test_robot.move_left()

test_robot.show_info()

# ТЕСТ 2: Переводчик команд
print("\n🧪 ТЕСТ 2: Тестируем переводчик команд")

# TODO: Создайте робота-переводчика
translator_robot = AdvancedRobot("Переводчик", ___, ___, "blue")

# Тестируем команды словами
print("\nТестируем команды словами:")
translator_robot.execute_command("___")  # up
translator_robot.execute_command("___")  # right
translator_robot.execute_command("___")  # down
translator_robot.execute_command("___")  # left

# Тестируем неизвестную команду
translator_robot.execute_command("неизвестно")

translator_robot.show_info()

print(f"\n🎉 Переводчик команд работает! Робот понимает слова!")
```

---

## ✅ Решение

```python
# Блок 3.3.1: Переводчик команд - РЕШЕНИЕ
# Создаем робота, который понимает слова!

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
    
    def show_info(self):
        """Подробная информация о роботе"""
        print(f"📊 {self.name}:")
        print(f"   📍 Позиция: ({self.x}, {self.y})")
        print(f"   🏠 Дом: ({self.start_x}, {self.start_y})")
        print(f"   👣 Шагов: {self.steps_made}")
        print(f"   📜 Команд выполнено: {len(self.commands_executed)}")
        if self.commands_executed:
            print(f"   🔤 Последние команды: {self.commands_executed[-5:]}")

# ТЕСТ 1: Основные движения
print("🧪 ТЕСТ 1: Проверяем основные движения")

# Создаем робота для тестирования
test_robot = AdvancedRobot("Тестер", 0, 0, "red")

# Тестируем каждое направление
print("\nТестируем все направления:")
test_robot.move_up()
test_robot.move_right()
test_robot.move_down()
test_robot.move_left()

test_robot.show_info()

# ТЕСТ 2: Переводчик команд
print("\n🧪 ТЕСТ 2: Тестируем переводчик команд")

# Создаем робота-переводчика
translator_robot = AdvancedRobot("Переводчик", 5, 5, "blue")

# Тестируем команды словами
print("\nТестируем команды словами:")
translator_robot.execute_command("up")
translator_robot.execute_command("right")
translator_robot.execute_command("down")
translator_robot.execute_command("left")

# Тестируем неизвестную команду
translator_robot.execute_command("неизвестно")

translator_robot.show_info()

print(f"\n🎉 Переводчик команд работает! Робот понимает слова!")
```
