# Блок 4.3: Система энергии (дополнительный)

## 📖 Текстовая ячейка (интро)

### 🔋 Реалистичная система энергии

До сих пор наши роботы двигались бесконечно, но в реальности **у всех роботов ограниченная энергия**! Батарейки садятся, и роботы должны уметь:
- 📊 **Отслеживать энергию** 
- ⚡ **Экономить заряд**
- 🛌 **Отдыхать для восстановления**
- 🚨 **Принимать решения** при низком заряде

### 🔄 Баланс активности и отдыха

**Движение тратит энергию:**
- Каждый шаг = -10 энергии
- Сложные команды = больше трат

**Отдых восстанавливает энергию:**
- Каждый цикл отдыха = +5 энергии  
- Максимум = 100 энергии

### 🤖 Умное поведение

Робот должен сам решать:
- **Двигаться**, если энергии достаточно
- **Отдыхать**, если энергии мало
- **Планировать маршрут** с учетом энергии

### 🎮 Стратегии энергосбережения

- **Консервативная**: отдых при <50 энергии
- **Рискованная**: отдых при <20 энергии  
- **Адаптивная**: зависит от расстояния до цели

### 📊 Статистика энергопотребления

Мы будем отслеживать:
- Общее потребление энергии
- Время в движении vs отдыхе
- Эффективность различных стратегий

---

## 💻 Код для ученика

```python
# Блок 4.3: Система энергии - реалистичные роботы!
# Добавляем батарейки, отдых и энергоменеджмент

import matplotlib.pyplot as plt
import time

class EnergyRobot:
    """Робот с реалистичной системой энергии"""
    
    def __init__(self, name, start_x=0, start_y=0, color="blue", max_energy=100):
        self.name = name
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.color = color
        
        # Энергетическая система
        self.max_energy = max_energy
        self.energy = max_energy
        self.energy_per_step = 10
        self.energy_per_rest = 5
        self.low_energy_threshold = 30
        
        # Статистика
        self.steps_made = 0
        self.rest_cycles = 0
        self.path = [(start_x, start_y)]
        self.energy_history = [max_energy]
        self.actions_log = []
        
        print(f"🔋 {name} создан с энергией {max_energy}/100")
    
    def show_energy_status(self):
        """Показывает текущий статус энергии"""
        # TODO: Создайте красивый индикатор энергии
        energy_bar = "█" * (self.energy // 10) + "░" * ((100 - self.energy) // 10)
        status = "🟢" if self.energy > 50 else "🟡" if self.energy > 20 else "🔴"
        
        print(f"{status} {self.name}: [{energy_bar}] {self.energy}/100")
    
    def can_move(self):
        """Проверяет, хватает ли энергии для движения"""
        return self.energy >= self.___  # TODO: какое условие?
    
    def need_rest(self):
        """Определяет, нужен ли отдых"""
        # TODO: Реализуйте логику необходимости отдыха
        return self.energy < self.___  # когда робот должен отдыхать?
    
    def move_step(self, direction):
        """Делает один шаг (если хватает энергии)"""
        if not self.can_move():
            print(f"⚠️ {self.name}: Недостаточно энергии для движения!")
            return False
        
        # TODO: Реализуйте движение и трату энергии
        if direction == "up":
            self.y += 1
        elif direction == "down":
            self.y -= 1
        elif direction == "left":
            self.x -= 1
        elif direction == "right":
            self.x += 1
        
        # Тратим энергию
        self.energy -= self.___  # TODO: сколько энергии тратим?
        self.steps_made += 1
        self.path.append((self.x, self.y))
        self.energy_history.append(self.energy)
        self.actions_log.append(f"move_{direction}")
        
        print(f"🚶 {self.name} {direction} → ({self.x}, {self.y}) [⚡{self.energy}]")
        return True
    
    def rest(self):
        """Отдыхает и восстанавливает энергию"""
        # TODO: Реализуйте отдых и восстановление энергии
        old_energy = self.energy
        self.energy = min(self.max_energy, self.energy + self.___)  # TODO: сколько восстанавливаем?
        self.rest_cycles += 1
        self.energy_history.append(self.energy)
        self.actions_log.append("rest")
        
        print(f"😴 {self.name} отдыхает: {old_energy} → {self.energy} [💤]")
    
    def smart_execute_command(self, command):
        """Умное выполнение команды с учетом энергии"""
        # Сначала проверяем, нужен ли отдых
        while self.need_rest():
            self.rest()
            self.show_energy_status()
        
        # Пытаемся выполнить команду
        if command in ["up", "down", "left", "right"]:
            success = self.move_step(command)
            if not success and self.need_rest():
                print(f"🔋 {self.name} вынужден отдохнуть перед продолжением...")
                self.rest()
                self.move_step(command)  # повторная попытка
        else:
            print(f"❓ {self.name}: Неизвестная команда '{command}'")
    
    def execute_sequence_with_energy(self, commands):
        """Выполняет последовательность команд с энергоменеджментом"""
        print(f"\n🎯 {self.name} выполняет {len(commands)} команд: {commands}")
        
        for i, command in enumerate(commands):
            print(f"\n--- Команда {i+1}/{len(commands)}: {command} ---")
            self.smart_execute_command(command)
            self.show_energy_status()
            
            # Небольшая пауза для наглядности (уберите в реальном коде)
            # time.sleep(0.1)
        
        print(f"✅ {self.name} завершил выполнение команд!")
    
    def show_statistics(self):
        """Показывает детальную статистику энергопотребления"""
        total_actions = len(self.actions_log)
        move_actions = sum(1 for action in self.actions_log if action.startswith("move"))
        rest_actions = sum(1 for action in self.actions_log if action == "rest")
        
        print(f"\n📊 ЭНЕРГОСТАТИСТИКА {self.name}:")
        print(f"   🔋 Текущая энергия: {self.energy}/{self.max_energy}")
        print(f"   👣 Шагов сделано: {self.steps_made}")
        print(f"   😴 Циклов отдыха: {self.rest_cycles}")
        print(f"   📈 Общее действий: {total_actions}")
        print(f"   ⚡ Энергии потрачено: {self.steps_made * self.energy_per_step}")
        print(f"   💤 Энергии восстановлено: {self.rest_cycles * self.energy_per_rest}")
        print(f"   📊 Эффективность: {move_actions/total_actions*100:.1f}% движения")
    
    def draw_energy_chart(self):
        """Рисует график изменения энергии"""
        plt.figure(figsize=(12, 4))
        
        # График энергии
        plt.subplot(1, 2, 1)
        plt.plot(self.energy_history, linewidth=2, color=self.color, label=f'{self.name} энергия')
        plt.axhline(y=self.low_energy_threshold, color='red', linestyle='--', alpha=0.7, label='Низкий заряд')
        plt.axhline(y=50, color='orange', linestyle='--', alpha=0.7, label='Средний заряд')
        plt.fill_between(range(len(self.energy_history)), self.energy_history, alpha=0.3, color=self.color)
        
        plt.title(f"График энергии - {self.name}")
        plt.xlabel("Время (действия)")
        plt.ylabel("Энергия")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 105)
        
        # Диаграмма действий
        plt.subplot(1, 2, 2)
        action_types = ["Движение", "Отдых"]
        action_counts = [
            sum(1 for action in self.actions_log if action.startswith("move")),
            sum(1 for action in self.actions_log if action == "rest")
        ]
        colors = [self.color, 'lightgray']
        
        plt.pie(action_counts, labels=action_types, colors=colors, autopct='%1.1f%%')
        plt.title(f"Распределение активности - {self.name}")
        
        plt.tight_layout()
    
    def draw_path(self):
        """Рисует путь робота с индикацией уровня энергии"""
        if len(self.path) < 2:
            return
            
        plt.figure(figsize=(10, 8))
        
        x_coords = [p[0] for p in self.path]
        y_coords = [p[1] for p in self.path]
        
        # Путь с градиентом энергии
        for i in range(len(self.path) - 1):
            energy_ratio = self.energy_history[i] / 100
            alpha = 0.3 + 0.7 * energy_ratio  # прозрачность зависит от энергии
            
            plt.plot([x_coords[i], x_coords[i+1]], 
                    [y_coords[i], y_coords[i+1]], 
                    color=self.color, 
                    linewidth=3, 
                    alpha=alpha)
        
        # Стартовая и финальная точки
        plt.scatter(x_coords[0], y_coords[0], color='green', s=200, marker='^', label='Старт')
        plt.scatter(x_coords[-1], y_coords[-1], color='red', s=200, marker='s', label='Финиш')
        
        # Точки отдыха
        rest_points_x = []
        rest_points_y = []
        for i, action in enumerate(self.actions_log):
            if action == "rest" and i < len(self.path):
                rest_points_x.append(x_coords[min(i, len(x_coords)-1)])
                rest_points_y.append(y_coords[min(i, len(y_coords)-1)])
        
        if rest_points_x:
            plt.scatter(rest_points_x, rest_points_y, color='orange', s=100, marker='o', alpha=0.7, label='Отдых')
        
        plt.title(f"Путь {self.name} (яркость = уровень энергии)")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axis('equal')

# ТЕСТ 1: Базовая система энергии
print("🧪 ТЕСТ 1: Основы энергетической системы")

# TODO: Создайте робота с энергией
energy_robot = EnergyRobot("___", ___, ___, "blue", ___)

# Показать начальный статус
energy_robot.show_energy_status()

# Простой тест движения
print("\nТест базового движения:")
test_commands = ["right", "right", "up", "up", "left", "left", "down", "down"]

# TODO: Выполните команды с энергоменеджментом
energy_robot.execute_sequence_with_energy(___)

energy_robot.show_statistics()

# ТЕСТ 2: Робот с низкой энергией
print("\n🧪 ТЕСТ 2: Робот с ограниченной энергией")

# TODO: Создайте робота с малой батарейкой
low_energy_robot = EnergyRobot("___", ___, ___, "red", max_energy=___)

# Команды, которые потребуют отдыха
demanding_commands = ["up"] * 8 + ["right"] * 6

print(f"\nТест с большой нагрузкой ({len(demanding_commands)} команд):")
low_energy_robot.execute_sequence_with_energy(demanding_commands)

low_energy_robot.show_statistics()

# ТЕСТ 3: Сравнение стратегий
print("\n🧪 ТЕСТ 3: Сравнение энергетических стратегий")

# Робот-консерватор (отдыхает рано)
class ConservativeRobot(EnergyRobot):
    def __init__(self, name, start_x=0, start_y=0, color="blue"):
        super().__init__(name, start_x, start_y, color)
        self.low_energy_threshold = ___  # TODO: высокий порог для консерватора

# Робот-рискован (отдыхает поздно)
class RiskyRobot(EnergyRobot):
    def __init__(self, name, start_x=0, start_y=0, color="red"):
        super().__init__(name, start_x, start_y, color)
        self.low_energy_threshold = ___  # TODO: низкий порог для рисковача

# TODO: Создайте роботов с разными стратегиями
conservative = ConservativeRobot("___", 0, 0, "green")
risky = RiskyRobot("___", 0, 5, "red")

# Одинаковые команды для честного сравнения
challenge_commands = ["right", "right", "up", "up", "right", "up", "left", "left", "down", "down", "down"]

print("Консервативный робот:")
conservative.execute_sequence_with_energy(challenge_commands)

print("\nРискованный робот:")  
risky.execute_sequence_with_energy(challenge_commands)

# Сравнение результатов
print("\n📊 СРАВНЕНИЕ СТРАТЕГИЙ:")
robots = [conservative, risky]

for robot in robots:
    efficiency = robot.steps_made / (robot.steps_made + robot.rest_cycles) * 100
    print(f"{robot.name}:")
    print(f"   Шагов: {robot.steps_made}, Отдыха: {robot.rest_cycles}")
    print(f"   Эффективность: {efficiency:.1f}%")
    print(f"   Финальная энергия: {robot.energy}")

# ВИЗУАЛИЗАЦИЯ
print("\n🎨 ВИЗУАЛИЗАЦИЯ ЭНЕРГОСИСТЕМЫ:")

# График энергии
energy_robot.draw_energy_chart()
plt.show()

low_energy_robot.draw_energy_chart()
plt.show()

# Пути роботов
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
energy_robot.draw_path()
plt.title("Обычный робот")

plt.subplot(1, 3, 2)
conservative.draw_path()
plt.title("Консервативный")

plt.subplot(1, 3, 3)
risky.draw_path()
plt.title("Рискованный")

plt.tight_layout()
plt.show()

# Итоговая статистика всех роботов
print(f"\n📈 ИТОГОВАЯ СТАТИСТИКА ЭНЕРГОСИСТЕМЫ:")
all_robots = [energy_robot, low_energy_robot, conservative, risky]

total_steps = sum(robot.steps_made for robot in all_robots)
total_rest = sum(robot.rest_cycles for robot in all_robots)

print(f"   🤖 Роботов протестировано: {len(all_robots)}")
print(f"   👣 Общее количество шагов: {total_steps}")
print(f"   😴 Общее количество отдыха: {total_rest}")
print(f"   ⚖️ Соотношение движение/отдых: {total_steps/max(total_rest,1):.2f}")

# Самый эффективный робот
most_efficient = max(all_robots, key=lambda r: r.steps_made / max(r.steps_made + r.rest_cycles, 1))
print(f"   🏆 Самый эффективный: {most_efficient.name}")

print(f"\n🎉 Энергетическая система успешно внедрена!")
print(f"💡 Теперь роботы ведут себя реалистично!")
```
