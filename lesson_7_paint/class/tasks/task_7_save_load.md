# 💾 Блок 7: Сохранение и загрузка карт (25-30 мин) - БОНУС

## 🎯 Зачем сохранять карты?

Представьте: вы нарисовали сложную карту с лабиринтом, закрыли программу... и всё пропало!

**Решение:** Сохранение карты в файл JSON!

---

## 🧠 Теория: JSON формат

**JSON (JavaScript Object Notation)** - текстовый формат для хранения данных.

**Пример JSON файла:**
```json
{
  "grid_cols": 75,
  "grid_rows": 50,
  "cell_width": 10,
  "cell_height": 12,
  "filled_cells": [
    [5, 10],
    [5, 11],
    [6, 10],
    [6, 11]
  ]
}
```

**Почему JSON?**
- ✅ Читаемый формат (можно открыть в блокноте)
- ✅ Стандарт для хранения данных
- ✅ Встроенная поддержка в Python

---

## 📝 Задание 7.1: Создаём map_manager.py (15 мин)

**Создайте файл `map_manager.py` и скопируйте:**

```python
"""Модуль для сохранения и загрузки карт"""
import json

class MapManager:
    """Класс для работы с сохранением/загрузкой карт в JSON"""

    def __init__(self, filename="map.json"):
        """
        Инициализация менеджера карт

        Args:
            filename: имя файла для сохранения/загрузки
        """
        self.filename = filename

    def save_map(self, grid):
        """
        Сохранить карту в файл

        Args:
            grid: объект Grid с сеткой

        Returns:
            True если сохранение успешно, False иначе
        """
        try:
            # TODO: Преобразуйте множество клеток в список
            # JSON не умеет работать с множествами, только со списками
            filled_cells_list = list(___)

            # TODO: Создайте словарь с данными карты
            map_data = {
                "grid_cols": ___,      # grid.cols
                "grid_rows": ___,      # grid.rows
                "cell_width": ___,     # grid.cell_width
                "cell_height": ___,    # grid.cell_height
                "filled_cells": ___    # filled_cells_list
            }

            # TODO: Сохраните в файл
            # open() с режимом 'w' (write) создаёт/перезаписывает файл
            # encoding='utf-8' для поддержки русских символов
            # indent=2 для красивого форматирования
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(___, f, indent=2)

            print(f"✅ Карта сохранена в файл: {self.filename}")
            print(f"   Клеток сохранено: {len(filled_cells_list)}")
            return True

        except Exception as e:
            print(f"❌ Ошибка при сохранении: {e}")
            return False

    def load_map(self, grid):
        """
        Загрузить карту из файла

        Args:
            grid: объект Grid с сеткой

        Returns:
            True если загрузка успешна, False иначе
        """
        try:
            # TODO: Загрузите данные из файла
            with open(self.filename, 'r', encoding='utf-8') as f:
                map_data = json.load(___)

            # TODO: Проверьте совместимость размеров сетки
            if (map_data["grid_cols"] != ___ or
                map_data["grid_rows"] != ___):
                print(f"⚠️ Предупреждение: размер сетки в файле не совпадает!")
                print(f"   Файл: {map_data['grid_cols']}×{map_data['grid_rows']}")
                print(f"   Текущий: {grid.cols}×{grid.rows}")

            # TODO: Очистите текущую карту
            grid.___()

            # TODO: Загрузите клетки из файла
            loaded_count = 0
            for cell in map_data["filled_cells"]:
                col, row = cell

                # Проверяем, что клетка в пределах текущей сетки
                if 0 <= col < ___ and 0 <= row < ___:
                    grid.fill_cell(___, ___)
                    loaded_count += 1

            print(f"✅ Карта загружена из файла: {self.filename}")
            print(f"   Клеток загружено: {loaded_count}")
            return True

        except FileNotFoundError:
            print(f"❌ Файл не найден: {self.filename}")
            return False

        except Exception as e:
            print(f"❌ Ошибка при загрузке: {e}")
            return False
```

**Сохраните файл.**

---

## 📝 Задание 7.2: Интегрируем в InputManager (10 мин)

Добавим команды сохранения/загрузки.

**Откройте `input_manager.py` и внесите изменения:**

### Шаг 1: Добавьте map_manager в __init__

Найдите метод `__init__` и добавьте параметр:

```python
def __init__(self, grid, history, map_manager, running_flag):
    """
    Инициализация менеджера ввода

    Args:
        grid: объект Grid
        history: объект History
        map_manager: объект MapManager  # <-- ДОБАВЛЕНО
        running_flag: список [True/False] для управления циклом
    """
    self.grid = grid
    self.history = history
    self.map_manager = map_manager  # <-- ДОБАВЛЕНО
    self.running_flag = running_flag

    # ... остальной код без изменений
```

### Шаг 2: Добавьте привязки клавиш

В методе `_setup_default_bindings()` добавьте две строки:

```python
def _setup_default_bindings(self):
    """Настроить привязки клавиш по умолчанию"""
    self.bind_key(pygame.K_ESCAPE, "выход", self._exit_program)
    self.bind_key(pygame.K_h, "показать справку", self._show_help)
    self.bind_key(pygame.K_z, "отменить последнее действие", self._undo_action)
    self.bind_key(pygame.K_c, "очистить всё", self._clear_all)

    # TODO: Добавьте эти две строки
    self.bind_key(pygame.K_s, "сохранить карту", self._save_map)
    self.bind_key(pygame.K_l, "загрузить карту", self._load_map)
```

### Шаг 3: Добавьте методы-обработчики

В конец файла (после метода `_show_help`) добавьте:

```python
    def _save_map(self):
        """Сохранить карту"""
        # TODO: Вызовите метод save_map у map_manager
        if self.map_manager.___(___ ):
            # После сохранения очищаем историю
            # (т.к. сохранённое состояние становится "точкой отсчёта")
            self.history.clear()

    def _load_map(self):
        """Загрузить карту"""
        # TODO: Вызовите метод load_map у map_manager
        if self.map_manager.___(___ ):
            # После загрузки очищаем историю
            # (т.к. загруженное состояние - новая "точка отсчёта")
            self.history.clear()
```

**Сохраните файл.**

---

## 📝 Задание 7.3: Обновляем main.py (5 мин)

Последний штрих - создаём MapManager и передаём в InputManager.

**Откройте `main.py` и добавьте:**

### Шаг 1: Импорт

В начале файла добавьте:

```python
from grid import Grid
from history import History
from renderer import Renderer
from input_manager import InputManager
from map_manager import MapManager  # <-- ДОБАВЛЕНО
```

### Шаг 2: Создание объекта

В функции `main()` после создания renderer:

```python
# Создайте объекты
grid = Grid(WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT)
history = History()
renderer = Renderer(screen)
map_manager = MapManager()  # <-- ДОБАВЛЕНО
input_manager = InputManager(grid, history, map_manager, running)  # <-- ИЗМЕНЕНО
```

**Сохраните файл.**

---

## ✅ Запуск и тестирование

**Запустите программу:**

```bash
python main.py
```

### Тест 1: Сохранение карты

1. Нарисуйте что-нибудь (например, лабиринт)
2. Нажмите **S** (сохранить)
3. В консоли должно появиться:
   ```
   ✅ Карта сохранена в файл: map.json
      Клеток сохранено: 42
   ```
4. Проверьте, что файл `map.json` появился рядом с программой

### Тест 2: Просмотр JSON файла

Откройте `map.json` в блокноте. Вы увидите:

```json
{
  "grid_cols": 75,
  "grid_rows": 50,
  "cell_width": 10,
  "cell_height": 12,
  "filled_cells": [
    [10, 15],
    [11, 15],
    [12, 15],
    ...
  ]
}
```

### Тест 3: Загрузка карты

1. Нажмите **C** (очистить всё) - карта исчезнет
2. Нажмите **L** (загрузить) - карта вернётся!
3. В консоли:
   ```
   ✅ Карта загружена из файла: map.json
      Клеток загружено: 42
   ```

### Тест 4: Перезапуск программы

1. Закройте программу
2. Запустите снова
3. Нажмите **L** - карта загружается из файла!

---

## 🎉 Полностью готово!

Теперь у нас есть **полнофункциональный редактор препятствий** с:

- ✅ Рисованием мышью
- ✅ Стиранием мышью
- ✅ Подсветкой курсора
- ✅ Системой отмены (Z)
- ✅ Очисткой (C)
- ✅ Сохранением карты (S)
- ✅ Загрузкой карты (L)
- ✅ Справкой (H)
- ✅ Модульной архитектурой

---

## 🎓 Что мы узнали?

1. ✅ **JSON формат** - стандарт для хранения данных
2. ✅ **Модуль json** - json.dump() и json.load()
3. ✅ **Работа с файлами** - open(), чтение/запись
4. ✅ **Преобразование типов** - set → list для JSON
5. ✅ **Обработка ошибок** - try/except для FileNotFoundError

---

## 💡 Полезные команды

| Клавиша | Действие |
|---------|----------|
| **H** | Показать справку |
| **Z** | Отменить последнее действие |
| **C** | Очистить всё |
| **S** | Сохранить карту в map.json |
| **L** | Загрузить карту из map.json |
| **ESC** | Выход |
| **ЛКМ** | Рисовать (зажать и водить) |
| **ПКМ** | Стирать (зажать и водить) |

---

## 🌟 Поздравляю!

Вы создали профессиональный редактор карт с модульной архитектурой, системой отмены и сохранением!

Это серьёзный проект, который показывает:
- ✅ Работу с классами и модулями
- ✅ Обработку событий мыши и клавиатуры
- ✅ Паттерны проектирования (History, Manager)
- ✅ Работу с файлами и JSON
- ✅ Организацию кода в большом проекте

**Отличная работа! 🎉**
