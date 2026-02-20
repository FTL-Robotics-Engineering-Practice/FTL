# Блок 4.2: Комбинаторика команд (дополнительный)

## 📖 Текстовая ячейка (интро)

### 🎲 Что такое комбинаторика?

**Комбинаторика** - раздел математики, изучающий различные способы расположения и выбора объектов. В робототехнике это помогает:
- 🔄 **Найти все возможные маршруты**
- 🎯 **Оптимизировать движения**  
- 🎮 **Создать разнообразные паттерны**
- 🧪 **Протестировать алгоритмы**

### 🔢 Основные операции

**Перестановки** - разные порядки одних элементов:
- Команды `["up", "right"]` можно переставить как:
  - `["up", "right"]` и `["right", "up"]`

**Перемешивание** - случайный порядок:
- `["up", "down", "left", "right"]` → `["right", "up", "down", "left"]`

**Повторения** - дублирование команд:
- `["up"]` × 3 = `["up", "up", "up"]`

### 🐍 Python инструменты

**itertools.permutations** - все перестановки:
```python
import itertools
commands = ["up", "right"]
for perm in itertools.permutations(commands):
    print(perm)  # ('up', 'right'), ('right', 'up')
```

**random.shuffle** - случайное перемешивание:
```python
import random
commands = ["up", "down", "left", "right"]
random.shuffle(commands)  # случайный порядок
```

### 🎯 Практическое применение

- **Тестирование роботов** - проверка всех вариантов движения
- **Оптимизация маршрутов** - поиск кратчайшего пути
- **Создание паттернов** - художественные траектории
- **Машинное обучение** - генерация обучающих данных

---

## 💻 Код для ученика

```python
# Блок 4.2: Комбинаторика команд - математика для роботов!
# Изучаем перестановки, комбинации и случайные паттерны

import matplotlib.pyplot as plt
import itertools
import random
from collections import Counter

class CombinatorialRobot:
    """Робот, который экспериментирует с комбинаторикой команд"""
    
    def __init__(self, name, start_x=0, start_y=0, color="blue"):
        self.name = name
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.color = color
        self.steps_made = 0
        self.path = [(start_x, start_y)]
        self.experiments_done = 0
        print(f"🧮 {name} готов к комбинаторным экспериментам!")
    
    def reset_position(self):
        """Возвращается в стартовую позицию"""
        self.x = self.start_x
        self.y = self.start_y
        self.path = [(self.start_x, self.start_y)]
    
    def execute_commands(self, commands, show_steps=False):
        """Выполняет список команд"""
        for i, command in enumerate(commands):
            if command == "up":
                self.y += 1
            elif command == "down":
                self.y -= 1
            elif command == "left":
                self.x -= 1
            elif command == "right":
                self.x += 1
            
            self.steps_made += 1
            self.path.append((self.x, self.y))
            
            if show_steps:
                print(f"   {i+1}. {command} → ({self.x}, {self.y})")
    
    def test_all_permutations(self, base_commands):
        """Тестирует все возможные перестановки команд"""
        print(f"\n🔄 {self.name} тестирует все перестановки команд {base_commands}")
        
        # TODO: Используйте itertools.permutations для получения всех перестановок
        permutations = list(itertools.permutations(___))
        
        print(f"📊 Всего перестановок: {len(permutations)}")
        
        results = []
        for i, perm in enumerate(permutations):
            print(f"\nПерестановка {i+1}: {list(perm)}")
            
            # Сброс позиции перед каждым тестом
            self.reset_position()
            
            # Выполняем команды
            self.execute_commands(list(perm), show_steps=True)
            
            # Сохраняем результат
            final_pos = (self.x, self.y)
            results.append({
                'permutation': list(perm),
                'final_position': final_pos,
                'distance_from_start': ((self.x - self.start_x)**2 + (self.y - self.start_y)**2)**0.5
            })
            
            print(f"   Финальная позиция: {final_pos}")
        
        self.experiments_done += len(permutations)
        return results
    
    def create_random_walks(self, base_commands, num_walks=5):
        """Создает несколько случайных прогулок"""
        print(f"\n🎲 {self.name} создает {num_walks} случайных прогулок")
        
        walks = []
        for i in range(num_walks):
            # TODO: Создайте копию команд и перемешайте её
            shuffled_commands = base_commands.copy()
            random.___(shuffled_commands)  # перемешать
            
            print(f"\nПрогулка {i+1}: {shuffled_commands}")
            
            # Сброс и выполнение
            self.reset_position()
            self.execute_commands(shuffled_commands)
            
            walks.append({
                'walk_id': i+1,
                'commands': shuffled_commands,
                'final_position': (self.x, self.y),
                'path': self.path.copy()
            })
            
            print(f"   Финиш: ({self.x}, {self.y})")
        
        self.experiments_done += num_walks
        return walks
    
    def generate_repeated_patterns(self, single_commands, repetitions):
        """Генерирует паттерны с повторениями команд"""
        print(f"\n🔁 {self.name} создает паттерны с повторениями")
        
        patterns = []
        for command in single_commands:
            # TODO: Создайте список с повторением команды
            repeated_command = [___] * ___  # команда повторяется repetitions раз
            
            print(f"\nПаттерн: {command} × {repetitions} = {repeated_command}")
            
            self.reset_position()
            self.execute_commands(repeated_command)
            
            patterns.append({
                'pattern': repeated_command,
                'final_position': (self.x, self.y)
            })
            
            print(f"   Результат: ({self.x}, {self.y})")
        
        return patterns
    
    def analyze_command_frequency(self, all_experiments):
        """Анализирует частоту использования команд"""
        print(f"\n📊 {self.name} анализирует частоту команд")
        
        # Собираем все команды из экспериментов
        all_commands = []
        for exp in all_experiments:
            if 'permutation' in exp:
                all_commands.extend(exp['permutation'])
            elif 'commands' in exp:
                all_commands.extend(exp['commands'])
        
        # TODO: Используйте Counter для подсчета частоты
        frequency = Counter(___)
        
        print("Частота команд:")
        for command, count in frequency.most_common():
            print(f"   {command}: {count} раз")
        
        return frequency
    
    def draw_experiments(self, experiments_data, title="Эксперименты"):
        """Рисует результаты экспериментов"""
        plt.figure(figsize=(10, 8))
        
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
        
        for i, exp in enumerate(experiments_data):
            if 'path' in exp:
                # Рисуем путь
                path = exp['path']
                x_coords = [p[0] for p in path]
                y_coords = [p[1] for p in path]
                plt.plot(x_coords, y_coords, 
                        color=colors[i % len(colors)], 
                        linewidth=2, 
                        alpha=0.7,
                        label=f"Прогулка {exp.get('walk_id', i+1)}")
            else:
                # Рисуем только финальную точку
                final_pos = exp['final_position']
                plt.scatter(final_pos[0], final_pos[1], 
                           color=colors[i % len(colors)],
                           s=100,
                           alpha=0.8,
                           label=f"Результат {i+1}")
        
        # Стартовая точка
        plt.scatter(self.start_x, self.start_y, 
                   color='black', 
                   s=200, 
                   marker='*',
                   label='Старт')
        
        plt.grid(True, alpha=0.3)
        plt.title(title)
        plt.xlabel("X координата")
        plt.ylabel("Y координата")
        plt.legend()
        plt.axis('equal')

# ЭКСПЕРИМЕНТ 1: Все перестановки простых команд
print("🧪 ЭКСПЕРИМЕНТ 1: Перестановки команд")

# TODO: Создайте робота-экспериментатора
experimenter = CombinatorialRobot("___", ___, ___, "blue")

# Простой набор команд для тестирования
simple_commands = ["up", "right"]

# TODO: Протестируйте все перестановки
permutation_results = experimenter.test_all_permutations(___)

# Анализ результатов перестановок
print(f"\n📈 АНАЛИЗ ПЕРЕСТАНОВОК:")
unique_positions = set(result['final_position'] for result in permutation_results)
print(f"   Уникальных финальных позиций: {len(unique_positions)}")
print(f"   Позиции: {list(unique_positions)}")

# ЭКСПЕРИМЕНТ 2: Случайные прогулки
print(f"\n🧪 ЭКСПЕРИМЕНТ 2: Случайные прогулки")

# Более сложный набор команд
complex_commands = ["up", "down", "left", "right", "up", "right"]

# TODO: Создайте 5 случайных прогулок
random_walks = experimenter.create_random_walks(___, ___)

# ЭКСПЕРИМЕНТ 3: Паттерны с повторениями
print(f"\n🧪 ЭКСПЕРИМЕНТ 3: Повторяющиеся паттерны")

# TODO: Создайте паттерны с повторениями
pattern_results = experimenter.generate_repeated_patterns(
    ["up", "right", "down", "left"], 
    ___  # количество повторений
)

# ЭКСПЕРИМЕНТ 4: Анализ всех данных
print(f"\n🧪 ЭКСПЕРИМЕНТ 4: Общий анализ")

# Объединяем все эксперименты
all_experiments = permutation_results + random_walks + pattern_results

# TODO: Проанализируйте частоту команд
frequency_analysis = experimenter.analyze_command_frequency(___)

# Статистика
print(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
print(f"   🤖 Робот: {experimenter.name}")
print(f"   🧪 Экспериментов проведено: {experimenter.experiments_done}")
print(f"   👣 Общее количество шагов: {experimenter.steps_made}")

# Найдем самую далекую точку
max_distance = 0
farthest_experiment = None
for exp in all_experiments:
    pos = exp['final_position']
    distance = ((pos[0] - experimenter.start_x)**2 + (pos[1] - experimenter.start_y)**2)**0.5
    if distance > max_distance:
        max_distance = distance
        farthest_experiment = exp

print(f"   📏 Максимальное расстояние от старта: {max_distance:.2f}")
print(f"   🎯 Самая далекая точка: {farthest_experiment['final_position']}")

# ВИЗУАЛИЗАЦИЯ
print(f"\n🎨 ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ:")

# График 1: Перестановки
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
for i, result in enumerate(permutation_results):
    pos = result['final_position']
    plt.scatter(pos[0], pos[1], s=100, alpha=0.7, label=f"Пермутация {i+1}")
plt.scatter(experimenter.start_x, experimenter.start_y, color='black', s=200, marker='*', label='Старт')
plt.title("Результаты перестановок")
plt.grid(True, alpha=0.3)
plt.legend()

# График 2: Случайные прогулки  
plt.subplot(1, 3, 2)
colors = ['red', 'blue', 'green', 'orange', 'purple']
for i, walk in enumerate(random_walks):
    if 'path' in walk:
        path = walk['path']
        x_coords = [p[0] for p in path]
        y_coords = [p[1] for p in path]
        plt.plot(x_coords, y_coords, color=colors[i], linewidth=2, alpha=0.7, label=f"Прогулка {i+1}")
plt.scatter(experimenter.start_x, experimenter.start_y, color='black', s=200, marker='*', label='Старт')
plt.title("Случайные прогулки")
plt.grid(True, alpha=0.3)
plt.legend()

# График 3: Паттерны
plt.subplot(1, 3, 3)
for i, pattern in enumerate(pattern_results):
    pos = pattern['final_position']
    plt.scatter(pos[0], pos[1], s=150, alpha=0.8, label=f"Паттерн {i+1}")
plt.scatter(experimenter.start_x, experimenter.start_y, color='black', s=200, marker='*', label='Старт')
plt.title("Повторяющиеся паттерны")
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()

print(f"\n🎉 Комбинаторные эксперименты завершены!")
print(f"💡 Комбинаторика помогает роботам находить оптимальные стратегии!")
```
