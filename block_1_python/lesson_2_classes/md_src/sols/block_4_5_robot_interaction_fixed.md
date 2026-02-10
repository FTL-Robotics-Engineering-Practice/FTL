# Блок 4.5: Взаимодействие роботов (дополнительный)

## 📖 Текстовая ячейка (интро)

### 🤝 Роботы учатся работать вместе

До сих пор каждый робот работал **самостоятельно**. Но в реальности роботы часто **взаимодействуют**:
- 🏭 **Фабричные роботы** координируют действия
- 🚗 **Беспилотники** обмениваются данными о дороге
- 🔍 **Роботы-исследователи** делятся найденной информацией
- 🏥 **Медицинские роботы** работают в команде

### 🎯 Задача встречи двух роботов

**Классическая задача робототехники**: два робота находятся в разных точках и должны **встретиться**. 

**Простое решение:**
1. Найти **среднюю точку** между роботами
2. Оба робота идут к этой точке
3. Встреча произойдет в центре!

### 🧮 Математика встречи

Для роботов в позициях (x₁, y₁) и (x₂, y₂):
- **Средняя точка**: ((x₁ + x₂) / 2, (y₁ + y₂) / 2)
- **Округление**: используем `int()` для получения целых координат
- **Альтернативы**: можно выбрать ближайшую к одному из роботов точку

### 👥 Менеджер роботов

Создадим **класс RobotManager**, который:
- Хранит список роботов
- Вычисляет точки встречи
- Координирует движения
- Отслеживает прогресс встречи

### 🎮 Расширенные сценарии

- **Встреча группы** - несколько роботов идут в центр
- **Эстафета** - роботы передают друг другу "эстафетную палочку"
- **Следование** - один робот преследует другого
- **Избегание** - роботы стараются не столкнуться

---

## 💻 Код для ученика

```python
# Блок 4.5: Взаимодействие роботов - учимся работать в команде!
# Создаем систему координации множественных роботов

import matplotlib.pyplot as plt
import math

class CollaborativeRobot:
    """Робот, который умеет взаимодействовать с другими роботами"""
    
    def __init__(self, name, start_x=0, start_y=0, color="blue"):
        self.name = name
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.color = color
        self.steps_made = 0
        self.path = [(start_x, start_y)]
        self.mission_completed = False
        self.meetings_count = 0
        
        print(f"🤖 {name} готов к командной работе в ({start_x}, {start_y})")
    
    def get_position(self):
        """Возвращает текущую позицию"""
        return (self.x, self.y)
    
    def distance_to(self, other_robot):
        """Вычисляет расстояние до другого робота"""
        # TODO: Реализуйте вычисление расстояния
        dx = self.x - other_robot.x
        dy = self.y - other_robot.y
        return math.sqrt(___ * ___ + ___ * ___)
    
    def move_towards(self, target_x, target_y):
        """Делает один шаг к целевой точке"""
        # TODO: Реализуйте умное движение к цели
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1
        
        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1
        
        self.steps_made += 1
        self.path.append((self.x, self.y))
        print(f"🚶 {self.name} идет к ({target_x}, {target_y}) → текущая ({self.x}, {self.y})")
    
    def navigate_to_point(self, target_x, target_y, max_steps=50):
        """Навигирует к определенной точке"""
        print(f"🎯 {self.name} навигирует к ({target_x}, {target_y})")
        
        steps_taken = 0
        
        while (self.x != target_x or self.y != target_y) and steps_taken < max_steps:
            self.move_towards(target_x, target_y)
            steps_taken += 1
        
        if self.x == target_x and self.y == target_y:
            print(f"✅ {self.name} достиг цели за {steps_taken} шагов!")
            return True
        else:
            print(f"⏰ {self.name} не достиг цели за {max_steps} шагов")
            return False
    
    def show_status(self):
        """Показывает статус робота"""
        print(f"📊 {self.name}: позиция ({self.x}, {self.y}), шагов: {self.steps_made}, встреч: {self.meetings_count}")

class RobotManager:
    """Менеджер для координации взаимодействия роботов"""
    
    def __init__(self):
        self.robots = []
        self.meetings_coordinated = 0
        self.group_missions = 0
        
        print("👥 Менеджер роботов инициализирован")
    
    def add_robot(self, robot):
        """Добавляет робота под управление"""
        self.robots.append(robot)
        print(f"📝 {robot.name} добавлен в команду (всего роботов: {len(self.robots)})")
    
    def find_center_point(self, robot1, robot2):
        """Находит центральную точку между двумя роботами"""
        # TODO: Вычислите среднюю точку между роботами
        center_x = (robot1.x + robot2.x) // ___  # целочисленное деление
        center_y = (robot1.y + robot2.y) // ___
        
        print(f"📐 Центр между {robot1.name} и {robot2.name}: ({center_x}, {center_y})")
        return center_x, center_y
    
    def coordinate_meeting(self, robot1, robot2):
        """Координирует встречу двух роботов"""
        print(f"\n🤝 КООРДИНАЦИЯ ВСТРЕЧИ: {robot1.name} и {robot2.name}")
        
        # Находим точку встречи
        meeting_x, meeting_y = self.find_center_point(robot1, robot2)
        
        print(f"📍 Точка встречи: ({meeting_x}, {meeting_y})")
        print(f"📏 Расстояние между роботами: {robot1.distance_to(robot2):.2f}")
        
        # Оба робота идут к точке встречи
        print(f"\n🚶 {robot1.name} начинает движение к встрече...")
        success1 = robot1.navigate_to_point(meeting_x, meeting_y)
        
        print(f"\n🚶 {robot2.name} начинает движение к встрече...")  
        success2 = robot2.navigate_to_point(meeting_x, meeting_y)
        
        # Проверяем успех встречи
        if success1 and success2:
            robot1.meetings_count += 1
            robot2.meetings_count += 1
            self.meetings_coordinated += 1
            print(f"🎉 ВСТРЕЧА УСПЕШНА! {robot1.name} и {robot2.name} встретились в ({meeting_x}, {meeting_y})")
            return True
        else:
            print(f"❌ Встреча не состоялась")
            return False
    
    def coordinate_group_meeting(self, robot_indices=None):
        """Координирует встречу группы роботов"""
        if robot_indices is None:
            selected_robots = self.robots
        else:
            selected_robots = [self.robots[i] for i in robot_indices if i < len(self.robots)]
        
        if len(selected_robots) < 2:
            print("❌ Недостаточно роботов для групповой встречи")
            return False
        
        print(f"\n👥 ГРУППОВАЯ ВСТРЕЧА: {[robot.name for robot in selected_robots]}")
        
        # TODO: Вычислите центр группы роботов
        total_x = sum(robot.x for robot in selected_robots)
        total_y = sum(robot.y for robot in selected_robots)
        
        center_x = total_x // len(___)  # среднее X
        center_y = total_y // len(___)  # среднее Y
        
        print(f"📍 Центр группы: ({center_x}, {center_y})")
        
        # Все роботы идут к центру
        all_arrived = True
        for robot in selected_robots:
            print(f"\n🚶 {robot.name} движется к групповому центру...")
            success = robot.navigate_to_point(center_x, center_y)
            if success:
                robot.meetings_count += 1
            else:
                all_arrived = False
        
        if all_arrived:
            self.group_missions += 1
            print(f"🎉 ГРУППОВАЯ ВСТРЕЧА УСПЕШНА! Все роботы в центре ({center_x}, {center_y})")
            return True
        else:
            print(f"❌ Не все роботы смогли добраться до центра")
            return False
    
    def create_robot_chain(self, spacing=2):
        """Выстраивает роботов в цепочку"""
        if len(self.robots) < 2:
            print("❌ Недостаточно роботов для цепочки")
            return
        
        print(f"\n⛓️ СОЗДАНИЕ ЦЕПОЧКИ РОБОТОВ (интервал: {spacing})")
        
        # Берем первого робота как опорную точку
        base_robot = self.robots[0]
        base_x, base_y = base_robot.x, base_robot.y
        
        # Выстраиваем остальных роботов в линию
        for i, robot in enumerate(self.robots[1:], 1):
            target_x = base_x + i * spacing
            target_y = base_y
            
            print(f"🔗 {robot.name} движется в позицию {i} цепочки: ({target_x}, {target_y})")
            robot.navigate_to_point(target_x, target_y)
        
        print("✅ Цепочка роботов сформирована!")
    
    def show_team_statistics(self):
        """Показывает статистику команды"""
        print(f"\n📊 СТАТИСТИКА КОМАНДЫ:")
        print(f"   👥 Роботов в команде: {len(self.robots)}")
        print(f"   🤝 Встреч координировано: {self.meetings_coordinated}")
        print(f"   👥 Групповых миссий: {self.group_missions}")
        
        total_steps = sum(robot.steps_made for robot in self.robots)
        total_meetings = sum(robot.meetings_count for robot in self.robots)
        
        print(f"   👣 Общее количество шагов: {total_steps}")
        print(f"   🎯 Общее количество встреч: {total_meetings}")
        
        if self.robots:
            avg_steps = total_steps / len(self.robots)
            print(f"   📊 Среднее шагов на робота: {avg_steps:.1f}")
    
    def draw_team_visualization(self):
        """Рисует визуализацию команды роботов"""
        if not self.robots:
            print("Нет роботов для визуализации")
            return
        
        # Рисуем пути всех роботов
        for robot in self.robots:
            if len(robot.path) > 1:
                x_coords = [p[0] for p in robot.path]
                y_coords = [p[1] for p in robot.path]
                plt.plot(x_coords, y_coords, 
                        color=robot.color, 
                        linewidth=2, 
                        alpha=0.7, 
                        label=f'{robot.name} путь')
        
        # Стартовые позиции
        for robot in self.robots:
            plt.scatter(robot.start_x, robot.start_y, 
                       color=robot.color, 
                       s=150, 
                       marker='^', 
                       alpha=0.8)
            plt.annotate(f'{robot.name} старт', 
                        (robot.start_x, robot.start_y), 
                        xytext=(5, 5), 
                        textcoords='offset points',
                        fontsize=8)
        
        # Текущие позиции
        for robot in self.robots:
            plt.scatter(robot.x, robot.y, 
                       color=robot.color, 
                       s=200, 
                       marker='o', 
                       alpha=0.9)
            plt.annotate(f'{robot.name}', 
                        (robot.x, robot.y), 
                        xytext=(5, -15), 
                        textcoords='offset points',
                        fontsize=10,
                        weight='bold')
        
        plt.title("Визуализация командной работы роботов")
        plt.xlabel("X координата")
        plt.ylabel("Y координата")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axis('equal')

# СЦЕНАРИЙ 1: Простая встреча двух роботов
print("🧪 СЦЕНАРИЙ 1: Встреча двух роботов")

# TODO: Создайте менеджера роботов
manager = RobotManager()

# TODO: Создайте двух роботов в разных позициях
robot_alpha = CollaborativeRobot("___", ___, ___, "red")
robot_beta = CollaborativeRobot("___", ___, ___, "blue")

# Добавляем роботов в команду
manager.add_robot(___)
manager.add_robot(___)

# Показать начальные позиции
print("\nНачальные позиции:")
robot_alpha.show_status()
robot_beta.show_status()

# TODO: Координируем встречу
meeting_success = manager.coordinate_meeting(___, ___)

print(f"\nРезультат встречи: {'✅ Успех' if meeting_success else '❌ Неудача'}")

# СЦЕНАРИЙ 2: Групповая встреча
print("\n🧪 СЦЕНАРИЙ 2: Групповая встреча")

# TODO: Добавим еще роботов в команду
robot_gamma = CollaborativeRobot("___", ___, ___, "green")
robot_delta = CollaborativeRobot("___", ___, ___, "orange")

manager.add_robot(robot_gamma)
manager.add_robot(robot_delta)

print("\nПозиции всех роботов перед групповой встречей:")
for robot in manager.robots:
    robot.show_status()

# TODO: Координируем групповую встречу
group_success = manager.coordinate_group_meeting()

print(f"\nРезультат групповой встречи: {'✅ Успех' if group_success else '❌ Неудача'}")

# СЦЕНАРИЙ 3: Формирование цепочки
print("\n🧪 СЦЕНАРИЙ 3: Формирование цепочки роботов")

# Создаем новых роботов для цепочки
chain_manager = RobotManager()

# TODO: Создайте 4 роботов для цепочки
chain_robots = [
    CollaborativeRobot("Звено-1", ___, ___, "purple"),
    CollaborativeRobot("Звено-2", ___, ___, "brown"),  
    CollaborativeRobot("Звено-3", ___, ___, "pink"),
    CollaborativeRobot("Звено-4", ___, ___, "gray")
]

for robot in chain_robots:
    chain_manager.add_robot(robot)

print("\nПозиции роботов до формирования цепочки:")
for robot in chain_robots:
    robot.show_status()

# TODO: Создаем цепочку
chain_manager.create_robot_chain(spacing=___)

print("\nПозиции роботов после формирования цепочки:")
for robot in chain_robots:
    robot.show_status()

# СЦЕНАРИЙ 4: Продвинутое взаимодействие
print("\n🧪 СЦЕНАРИЙ 4: Эстафета роботов")

# Создаем сценарий эстафеты
class RelayRobot(CollaborativeRobot):
    """Робот для эстафеты"""
    
    def __init__(self, name, start_x, start_y, color):
        super().__init__(name, start_x, start_y, color)
        self.has_baton = False
        self.relay_position = 0
    
    def receive_baton(self):
        """Получает эстафетную палочку"""
        self.has_baton = True
        print(f"🏃 {self.name} получил эстафетную палочку!")
    
    def pass_baton(self, next_robot):
        """Передает палочку следующему роботу"""
        if self.has_baton:
            self.has_baton = False
            next_robot.receive_baton()
            print(f"🤝 {self.name} передал палочку → {next_robot.name}")
            return True
        return False

# TODO: Создайте команду эстафеты
relay_team = [
    RelayRobot("Бегун-1", ___, ___, "red"),
    RelayRobot("Бегун-2", ___, ___, "blue"),
    RelayRobot("Бегун-3", ___, ___, "green")
]

# Стартуем эстафету
relay_team[0].receive_baton()

print("🏃 ЭСТАФЕТА НАЧАЛАСЬ!")

# Каждый робот бежит к следующему и передает палочку
for i in range(len(relay_team) - 1):
    current_runner = relay_team[i]
    next_runner = relay_team[i + 1]
    
    print(f"\n--- Этап {i+1}: {current_runner.name} → {next_runner.name} ---")
    
    # Бежим к следующему роботу
    success = current_runner.navigate_to_point(next_runner.x, next_runner.y)
    
    if success:
        # Передаем палочку
        current_runner.pass_baton(next_runner)
    else:
        print(f"❌ {current_runner.name} не смог добраться до {next_runner.name}")
        break

print("\n🏁 ЭСТАФЕТА ЗАВЕРШЕНА!")

# ВИЗУАЛИЗАЦИЯ ВСЕХ СЦЕНАРИЕВ
print("\n🎨 ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ:")

# График 1: Первая команда
plt.figure(figsize=(15, 10))

plt.subplot(2, 2, 1)
manager.draw_team_visualization()
plt.title("Сценарий 1-2: Встречи команды")

plt.subplot(2, 2, 2)
chain_manager.draw_team_visualization()
plt.title("Сценарий 3: Цепочка роботов")

# График 3: Эстафета
plt.subplot(2, 2, 3)
for robot in relay_team:
    if len(robot.path) > 1:
        x_coords = [p[0] for p in robot.path]
        y_coords = [p[1] for p in robot.path]
        plt.plot(x_coords, y_coords, color=robot.color, linewidth=3, label=robot.name)
    
    plt.scatter(robot.start_x, robot.start_y, color=robot.color, s=150, marker='^')
    plt.scatter(robot.x, robot.y, color=robot.color, s=200, marker='o')

plt.title("Сценарий 4: Эстафета роботов")
plt.legend()
plt.grid(True, alpha=0.3)

# График 4: Статистика
plt.subplot(2, 2, 4)
all_managers = [manager, chain_manager]
manager_names = ["Основная команда", "Цепочка"]
meetings = [mgr.meetings_coordinated + mgr.group_missions for mgr in all_managers]

plt.bar(manager_names, meetings, color=['blue', 'green'])
plt.title("Успешные взаимодействия")
plt.ylabel("Количество")

plt.tight_layout()
plt.show()

# Итоговая статистика
print(f"\n📈 ИТОГОВАЯ СТАТИСТИКА ВЗАИМОДЕЙСТВИЙ:")

print("\nСтатистика основной команды:")
manager.show_team_statistics()

print("\nСтатистика команды цепочки:")
chain_manager.show_team_statistics()

# Общая статистика по всем роботам
all_robots = manager.robots + chain_manager.robots + relay_team
total_interactions = sum(robot.meetings_count for robot in all_robots)
total_steps = sum(robot.steps_made for robot in all_robots)

print(f"\n🌟 ОБЩАЯ СТАТИСТИКА:")
print(f"   🤖 Всего роботов участвовало: {len(all_robots)}")
print(f"   🤝 Общее количество взаимодействий: {total_interactions}")
print(f"   👣 Общее количество шагов: {total_steps}")
print(f"   📊 Среднее взаимодействий на робота: {total_interactions/len(all_robots):.1f}")

print(f"\n🎉 Система взаимодействия роботов успешно протестирована!")
print(f"💡 Роботы научились работать в команде!")
```

---

## ✅ Решение

```python
# Блок 4.5: Взаимодействие роботов - учимся работать в команде! - РЕШЕНИЕ
# Создаем систему координации множественных роботов

import matplotlib.pyplot as plt
import math

class CollaborativeRobot:
    """Робот, который умеет взаимодействовать с другими роботами"""
    
    def __init__(self, name, start_x=0, start_y=0, color="blue"):
        self.name = name
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.color = color
        self.steps_made = 0
        self.path = [(start_x, start_y)]
        self.mission_completed = False
        self.meetings_count = 0
        
        print(f"🤖 {name} готов к командной работе в ({start_x}, {start_y})")
    
    def get_position(self):
        """Возвращает текущую позицию"""
        return (self.x, self.y)
    
    def distance_to(self, other_robot):
        """Вычисляет расстояние до другого робота"""
        dx = self.x - other_robot.x
        dy = self.y - other_robot.y
        return math.sqrt(dx * dx + dy * dy)
    
    def move_towards(self, target_x, target_y):
        """Делает один шаг к целевой точке"""
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1
        
        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1
        
        self.steps_made += 1
        self.path.append((self.x, self.y))
        print(f"🚶 {self.name} идет к ({target_x}, {target_y}) → текущая ({self.x}, {self.y})")
    
    def navigate_to_point(self, target_x, target_y, max_steps=50):
        """Навигирует к определенной точке"""
        print(f"🎯 {self.name} навигирует к ({target_x}, {target_y})")
        
        steps_taken = 0
        
        while (self.x != target_x or self.y != target_y) and steps_taken < max_steps:
            self.move_towards(target_x, target_y)
            steps_taken += 1
        
        if self.x == target_x and self.y == target_y:
            print(f"✅ {self.name} достиг цели за {steps_taken} шагов!")
            return True
        else:
            print(f"⏰ {self.name} не достиг цели за {max_steps} шагов")
            return False
    
    def show_status(self):
        """Показывает статус робота"""
        print(f"📊 {self.name}: позиция ({self.x}, {self.y}), шагов: {self.steps_made}, встреч: {self.meetings_count}")

class RobotManager:
    """Менеджер для координации взаимодействия роботов"""
    
    def __init__(self):
        self.robots = []
        self.meetings_coordinated = 0
        self.group_missions = 0
        
        print("👥 Менеджер роботов инициализирован")
    
    def add_robot(self, robot):
        """Добавляет робота под управление"""
        self.robots.append(robot)
        print(f"📝 {robot.name} добавлен в команду (всего роботов: {len(self.robots)})")
    
    def find_center_point(self, robot1, robot2):
        """Находит центральную точку между двумя роботами"""
        center_x = (robot1.x + robot2.x) // 2
        center_y = (robot1.y + robot2.y) // 2
        
        print(f"📐 Центр между {robot1.name} и {robot2.name}: ({center_x}, {center_y})")
        return center_x, center_y
    
    def coordinate_meeting(self, robot1, robot2):
        """Координирует встречу двух роботов"""
        print(f"\n🤝 КООРДИНАЦИЯ ВСТРЕЧИ: {robot1.name} и {robot2.name}")
        
        # Находим точку встречи
        meeting_x, meeting_y = self.find_center_point(robot1, robot2)
        
        print(f"📍 Точка встречи: ({meeting_x}, {meeting_y})")
        print(f"📏 Расстояние между роботами: {robot1.distance_to(robot2):.2f}")
        
        # Оба робота идут к точке встречи
        print(f"\n🚶 {robot1.name} начинает движение к встрече...")
        success1 = robot1.navigate_to_point(meeting_x, meeting_y)
        
        print(f"\n🚶 {robot2.name} начинает движение к встрече...")  
        success2 = robot2.navigate_to_point(meeting_x, meeting_y)
        
        # Проверяем успех встречи
        if success1 and success2:
            robot1.meetings_count += 1
            robot2.meetings_count += 1
            self.meetings_coordinated += 1
            print(f"🎉 ВСТРЕЧА УСПЕШНА! {robot1.name} и {robot2.name} встретились в ({meeting_x}, {meeting_y})")
            return True
        else:
            print(f"❌ Встреча не состоялась")
            return False
    
    def coordinate_group_meeting(self, robot_indices=None):
        """Координирует встречу группы роботов"""
        if robot_indices is None:
            selected_robots = self.robots
        else:
            selected_robots = [self.robots[i] for i in robot_indices if i < len(self.robots)]
        
        if len(selected_robots) < 2:
            print("❌ Недостаточно роботов для групповой встречи")
            return False
        
        print(f"\n👥 ГРУППОВАЯ ВСТРЕЧА: {[robot.name for robot in selected_robots]}")
        
        # Вычисляем центр группы роботов
        total_x = sum(robot.x for robot in selected_robots)
        total_y = sum(robot.y for robot in selected_robots)
        
        center_x = total_x // len(selected_robots)
        center_y = total_y // len(selected_robots)
        
        print(f"📍 Центр группы: ({center_x}, {center_y})")
        
        # Все роботы идут к центру
        all_arrived = True
        for robot in selected_robots:
            print(f"\n🚶 {robot.name} движется к групповому центру...")
            success = robot.navigate_to_point(center_x, center_y)
            if success:
                robot.meetings_count += 1
            else:
                all_arrived = False
        
        if all_arrived:
            self.group_missions += 1
            print(f"🎉 ГРУППОВАЯ ВСТРЕЧА УСПЕШНА! Все роботы в центре ({center_x}, {center_y})")
            return True
        else:
            print(f"❌ Не все роботы смогли добраться до центра")
            return False
    
    def create_robot_chain(self, spacing=2):
        """Выстраивает роботов в цепочку"""
        if len(self.robots) < 2:
            print("❌ Недостаточно роботов для цепочки")
            return
        
        print(f"\n⛓️ СОЗДАНИЕ ЦЕПОЧКИ РОБОТОВ (интервал: {spacing})")
        
        # Берем первого робота как опорную точку
        base_robot = self.robots[0]
        base_x, base_y = base_robot.x, base_robot.y
        
        # Выстраиваем остальных роботов в линию
        for i, robot in enumerate(self.robots[1:], 1):
            target_x = base_x + i * spacing
            target_y = base_y
            
            print(f"🔗 {robot.name} движется в позицию {i} цепочки: ({target_x}, {target_y})")
            robot.navigate_to_point(target_x, target_y)
        
        print("✅ Цепочка роботов сформирована!")
    
    def show_team_statistics(self):
        """Показывает статистику команды"""
        print(f"\n📊 СТАТИСТИКА КОМАНДЫ:")
        print(f"   👥 Роботов в команде: {len(self.robots)}")
        print(f"   🤝 Встреч координировано: {self.meetings_coordinated}")
        print(f"   👥 Групповых миссий: {self.group_missions}")
        
        total_steps = sum(robot.steps_made for robot in self.robots)
        total_meetings = sum(robot.meetings_count for robot in self.robots)
        
        print(f"   👣 Общее количество шагов: {total_steps}")
        print(f"   🎯 Общее количество встреч: {total_meetings}")
        
        if self.robots:
            avg_steps = total_steps / len(self.robots)
            print(f"   📊 Среднее шагов на робота: {avg_steps:.1f}")
    
    def draw_team_visualization(self):
        """Рисует визуализацию команды роботов"""
        if not self.robots:
            print("Нет роботов для визуализации")
            return
        
        # Рисуем пути всех роботов
        for robot in self.robots:
            if len(robot.path) > 1:
                x_coords = [p[0] for p in robot.path]
                y_coords = [p[1] for p in robot.path]
                plt.plot(x_coords, y_coords, 
                        color=robot.color, 
                        linewidth=2, 
                        alpha=0.7, 
                        label=f'{robot.name} путь')
        
        # Стартовые позиции
        for robot in self.robots:
            plt.scatter(robot.start_x, robot.start_y, 
                       color=robot.color, 
                       s=150, 
                       marker='^', 
                       alpha=0.8)
            plt.annotate(f'{robot.name} старт', 
                        (robot.start_x, robot.start_y), 
                        xytext=(5, 5), 
                        textcoords='offset points',
                        fontsize=8)
        
        # Текущие позиции
        for robot in self.robots:
            plt.scatter(robot.x, robot.y, 
                       color=robot.color, 
                       s=200, 
                       marker='o', 
                       alpha=0.9)
            plt.annotate(f'{robot.name}', 
                        (robot.x, robot.y), 
                        xytext=(5, -15), 
                        textcoords='offset points',
                        fontsize=10,
                        weight='bold')
        
        plt.title("Визуализация командной работы роботов")
        plt.xlabel("X координата")
        plt.ylabel("Y координата")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axis('equal')

# СЦЕНАРИЙ 1: Простая встреча двух роботов
print("🧪 СЦЕНАРИЙ 1: Встреча двух роботов")

manager = RobotManager()

robot_alpha = CollaborativeRobot("Альфа", 2, 8, "red")
robot_beta = CollaborativeRobot("Бета", 10, 2, "blue")

# Добавляем роботов в команду
manager.add_robot(robot_alpha)
manager.add_robot(robot_beta)

# Показать начальные позиции
print("\nНачальные позиции:")
robot_alpha.show_status()
robot_beta.show_status()

# Координируем встречу
meeting_success = manager.coordinate_meeting(robot_alpha, robot_beta)

print(f"\nРезультат встречи: {'✅ Успех' if meeting_success else '❌ Неудача'}")

# СЦЕНАРИЙ 2: Групповая встреча
print("\n🧪 СЦЕНАРИЙ 2: Групповая встреча")

# Добавим еще роботов в команду
robot_gamma = CollaborativeRobot("Гамма", 1, 1, "green")
robot_delta = CollaborativeRobot("Дельта", 12, 10, "orange")

manager.add_robot(robot_gamma)
manager.add_robot(robot_delta)

print("\nПозиции всех роботов перед групповой встречей:")
for robot in manager.robots:
    robot.show_status()

# Координируем групповую встречу
group_success = manager.coordinate_group_meeting()

print(f"\nРезультат групповой встречи: {'✅ Успех' if group_success else '❌ Неудача'}")

# СЦЕНАРИЙ 3: Формирование цепочки
print("\n🧪 СЦЕНАРИЙ 3: Формирование цепочки роботов")

# Создаем новых роботов для цепочки
chain_manager = RobotManager()

chain_robots = [
    CollaborativeRobot("Звено-1", 3, 7, "purple"),
    CollaborativeRobot("Звено-2", 8, 4, "brown"),  
    CollaborativeRobot("Звено-3", 1, 9, "pink"),
    CollaborativeRobot("Звено-4", 11, 2, "gray")
]

for robot in chain_robots:
    chain_manager.add_robot(robot)

print("\nПозиции роботов до формирования цепочки:")
for robot in chain_robots:
    robot.show_status()

chain_manager.create_robot_chain(spacing=3)

print("\nПозиции роботов после формирования цепочки:")
for robot in chain_robots:
    robot.show_status()

# СЦЕНАРИЙ 4: Продвинутое взаимодействие
print("\n🧪 СЦЕНАРИЙ 4: Эстафета роботов")

# Создаем сценарий эстафеты
class RelayRobot(CollaborativeRobot):
    """Робот для эстафеты"""
    
    def __init__(self, name, start_x, start_y, color):
        super().__init__(name, start_x, start_y, color)
        self.has_baton = False
        self.relay_position = 0
    
    def receive_baton(self):
        """Получает эстафетную палочку"""
        self.has_baton = True
        print(f"🏃 {self.name} получил эстафетную палочку!")
    
    def pass_baton(self, next_robot):
        """Передает палочку следующему роботу"""
        if self.has_baton:
            self.has_baton = False
            next_robot.receive_baton()
            print(f"🤝 {self.name} передал палочку → {next_robot.name}")
            return True
        return False

# Создаем команду эстафеты
relay_team = [
    RelayRobot("Бегун-1", 1, 3, "red"),
    RelayRobot("Бегун-2", 6, 6, "blue"),
    RelayRobot("Бегун-3", 10, 2, "green")
]

# Стартуем эстафету
relay_team[0].receive_baton()

print("🏃 ЭСТАФЕТА НАЧАЛАСЬ!")

# Каждый робот бежит к следующему и передает палочку
for i in range(len(relay_team) - 1):
    current_runner = relay_team[i]
    next_runner = relay_team[i + 1]
    
    print(f"\n--- Этап {i+1}: {current_runner.name} → {next_runner.name} ---")
    
    # Бежим к следующему роботу
    success = current_runner.navigate_to_point(next_runner.x, next_runner.y)
    
    if success:
        # Передаем палочку
        current_runner.pass_baton(next_runner)
    else:
        print(f"❌ {current_runner.name} не смог добраться до {next_runner.name}")
        break

print("\n🏁 ЭСТАФЕТА ЗАВЕРШЕНА!")

# ВИЗУАЛИЗАЦИЯ ВСЕХ СЦЕНАРИЕВ
print("\n🎨 ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ:")

plt.figure(figsize=(15, 10))

plt.subplot(2, 2, 1)
manager.draw_team_visualization()

plt.subplot(2, 2, 2)
chain_manager.draw_team_visualization()

# График 3: Эстафета
plt.subplot(2, 2, 3)
for robot in relay_team:
    if len(robot.path) > 1:
        x_coords = [p[0] for p in robot.path]
        y_coords = [p[1] for p in robot.path]
        plt.plot(x_coords, y_coords, color=robot.color, linewidth=3, label=robot.name)
    
    plt.scatter(robot.start_x, robot.start_y, color=robot.color, s=150, marker='^')
    plt.scatter(robot.x, robot.y, color=robot.color, s=200, marker='o')

plt.title("Сценарий 4: Эстафета роботов")
plt.legend()
plt.grid(True, alpha=0.3)

# График 4: Статистика
plt.subplot(2, 2, 4)
all_managers = [manager, chain_manager]
manager_names = ["Основная команда", "Цепочка"]
meetings = [mgr.meetings_coordinated + mgr.group_missions for mgr in all_managers]

plt.bar(manager_names, meetings, color=['blue', 'green'])
plt.title("Успешные взаимодействия")
plt.ylabel("Количество")

plt.tight_layout()
plt.show()

# ИТОГОВАЯ СТАТИСТИКА
print(f"\n📈 ИТОГОВАЯ СТАТИСТИКА ВЗАИМОДЕЙСТВИЙ:")

print("\nСтатистика основной команды:")
manager.show_team_statistics()

print("\nСтатистика команды цепочки:")
chain_manager.show_team_statistics()

# Общая статистика по всем роботам
all_robots = manager.robots + chain_manager.robots + relay_team
total_interactions = sum(robot.meetings_count for robot in all_robots)
total_steps = sum(robot.steps_made for robot in all_robots)

print(f"\n🌟 ОБЩАЯ СТАТИСТИКА:")
print(f"   🤖 Всего роботов участвовало: {len(all_robots)}")
print(f"   🤝 Общее количество взаимодействий: {total_interactions}")
print(f"   👣 Общее количество шагов: {total_steps}")
print(f"   📊 Среднее взаимодействий на робота: {total_interactions/len(all_robots):.1f}")

print(f"\n🎉 Система взаимодействия роботов успешно протестирована!")
print(f"💡 Роботы научились работать в команде!")
```