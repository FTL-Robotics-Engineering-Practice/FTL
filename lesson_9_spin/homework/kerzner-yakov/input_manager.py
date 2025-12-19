"""Модуль для управления вводом с клавиатуры и мыши"""
import pygame

class InputManager:
    """Класс для управления всем вводом (мышь + клавиатура)"""

    def __init__(self, grid, history, map_manager, running_flag, mode_manager, robot, brain=None):
        """
        Инициализация менеджера ввода

        Args:
            grid: объект Grid
            history: объект History
            map_manager: объект MapManager
            running_flag: список [True/False] для управления циклом
            mode_manager: объект ModeManager
            robot: объект Robot
            brain: объект Brain (опционально, для управления паузой)
        """
        self.grid = grid
        self.history = history
        self.map_manager = map_manager
        self.running_flag = running_flag
        self.mode_manager = mode_manager
        self.robot = robot
        self.brain = brain

        # Флаги состояния мыши
        self.left_mouse_pressed = False
        self.right_mouse_pressed = False
        self.last_drawn_cell = None
        self.last_erased_cell = None

        # Флаги для управления симуляцией
        self.simu_going = True
        self.old_linear = 0
        self.old_angular = 0

        # Словарь для отслеживания нажатых клавиш управления
        self.pressed_keys = {
            pygame.K_w: False,
            pygame.K_s: False,
            pygame.K_a: False,
            pygame.K_d: False,
            pygame.K_x: False,  # X - остановка симуляции
        }

        # Словарь привязок клавиш
        self.key_bindings = {}

        # Настраиваем привязки клавиш
        self._setup_default_bindings()

    def bind_key(self, key, description, function):
        """
        Привязать клавишу к функции

        Args:
            key: код клавиши pygame (pygame.K_z, pygame.K_c и т.д.)
            description: описание действия (строка)
            function: функция, которую нужно вызвать
        """
        self.key_bindings[key] = {
            'description': description,
            'function': function
        }

    def _setup_default_bindings(self):
        """Настроить привязки клавиш по умолчанию"""
        # Основные привязки
        self.bind_key(pygame.K_ESCAPE, "выход", self._exit_program)
        self.bind_key(pygame.K_h, "показать справку", self._show_help)
        self.bind_key(pygame.K_z, "отменить последнее действие", self._undo_action)
        self.bind_key(pygame.K_c, "очистить всё", self._clear_all)
        
        # Управление режимами
        self.bind_key(pygame.K_TAB, "переключить режим", self._toggle_mode)
        
        # Управление картами
        self.bind_key(pygame.K_k, "сохранить карту", self._save_map)
        self.bind_key(pygame.K_l, "загрузить карту", self._load_map)

    def handle_event(self, event):
        """
        Обработать событие pygame

        Args:
            event: объект события pygame
        """
        # Обработка клавиш
        if event.type == pygame.KEYDOWN:
            # Если нажата клавиша управления роботом - сохраняем в словарь
            if event.key in self.pressed_keys:
                self.pressed_keys[event.key] = True
            
           

            # Проверяем, есть ли привязка для этой клавиши
            if event.key in self.key_bindings:
                self.key_bindings[event.key]['function']()

        # Обработка отпускания клавиш
        elif event.type == pygame.KEYUP:
            # Если отпущена клавиша управления - сбрасываем в словаре
            if event.key in self.pressed_keys:
                self.pressed_keys[event.key] = False
            

        # Обработка мыши - нажатие
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_button_down(event.button)

        # Обработка мыши - отпускание
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_button_up(event.button)

    def handle_mouse_button_down(self, button):
        """Обработать нажатие кнопки мыши"""
        if button == 1:  # Левая кнопка
            self.left_mouse_pressed = True
            self.last_drawn_cell = None
        elif button == 3:  # Правая кнопка
            self.right_mouse_pressed = True
            self.last_erased_cell = None

    def handle_mouse_button_up(self, button):
        """Обработать отпускание кнопки мыши"""
        if button == 1:  # Левая кнопка
            self.left_mouse_pressed = False
            self.last_drawn_cell = None
        elif button == 3:  # Правая кнопка
            self.right_mouse_pressed = False
            self.last_erased_cell = None

    def handle_mouse_motion(self, mouse_x, mouse_y):
        """
        Обработать движение мыши (рисование/стирание)

        Args:
            mouse_x: координата X мыши
            mouse_y: координата Y мыши
        """
        # Проверяем, что мы в режиме редактирования карты
        if not self.mode_manager.is_map_mode():
            return

        # Рисование при зажатой левой кнопке
        if self.left_mouse_pressed:
            cell = self.grid.get_cell_at_position(mouse_x, mouse_y)
            if cell is not None:
                col, row = cell
                if cell != self.last_drawn_cell:
                    self.grid.fill_cell(col, row)
                    self.history.add_action({'type': 'fill', 'cell': (col, row)})
                    self.last_drawn_cell = cell

        # Стирание при зажатой правой кнопке
        if self.right_mouse_pressed:
            cell = self.grid.get_cell_at_position(mouse_x, mouse_y)
            if cell is not None:
                col, row = cell
                if cell != self.last_erased_cell:
                    if self.grid.is_cell_filled(col, row):
                        self.grid.clear_cell(col, row)
                        self.history.add_action({'type': 'erase', 'cell': (col, row)})
                    self.last_erased_cell = cell

    def _stop_simu(self):
        """Остановить/возобновить симуляцию"""
        if not self.mode_manager.is_robot_mode():
            return

        if self.pressed_keys.get(pygame.K_x, False):
            if self.simu_going:
                # Сохраняем текущие скорости и останавливаем
                self.old_linear = self.robot.linear_velocity
                self.old_angular = self.robot.angular_velocity
                self.robot.set_velocities(0, 0)
                self.simu_going = False
                print("Симуляция остановлена")
        else:
            if not self.simu_going:
                # Восстанавливаем скорости
                self.robot.set_velocities(self.old_linear, self.old_angular)
                self.old_linear = 0
                self.old_angular = 0
                self.simu_going = True
                print("Симуляция возобновлена")

    # ===== Функции-обработчики команд =====

    def _exit_program(self):
        """Выход из программы"""
        self.running_flag[0] = False
        print("Выход из программы")

    def _undo_action(self):
        """Отменить последнее действие"""
        # Работает только в режиме редактирования карты
        if not self.mode_manager.is_map_mode():
            return
            
        action = self.history.undo()
        if action is not None:
            col, row = action['cell']

            if action['type'] == 'fill':
                self.grid.clear_cell(col, row)
                print(f"Отменено заполнение ({col}, {row})")

            elif action['type'] == 'erase':
                self.grid.fill_cell(col, row)
                print(f"Отменено стирание ({col}, {row})")
        else:
            print("История пуста, нечего отменять")

    def _clear_all(self):
        """Очистить всю сетку и историю"""
        # Работает только в режиме редактирования карты
        if not self.mode_manager.is_map_mode():
            return
            
        self.grid.clear_all()
        self.history.clear()
        print("Сетка и история очищены")

    def _show_help(self):
        """Показать справку по управлению"""
        print("\n" + "="*50)
        print("УПРАВЛЕНИЕ:")
        print("="*50)

        # Выводим все привязки клавиш
        for key, binding in self.key_bindings.items():
            key_name = pygame.key.name(key).upper()
            description = binding['description']
            print(f"  {key_name} - {description}")

        # Дополнительные клавиши управления роботом
        print("  W/S - движение вперёд/назад")
        print("  A/D - поворот влево/вправо")
        print("  X - остановить/возобновить симуляцию")

        print("="*50)
        print("МЫШЬ:")
        print("  ЛКМ (зажать) - рисовать препятствия")
        print("  ПКМ (зажать) - стирать препятствия")
        print("="*50)
        print(f"Клеток заполнено: {len(self.grid.filled_cells)}")
        print(f"Действий в истории: {self.history.get_size()}")
        print("="*50 + "\n")

    def _save_map(self):
        """Сохранить карту"""
        # Работает только в режиме редактирования карты
        if not self.mode_manager.is_map_mode():
            return
            
        if self.map_manager.save_map(self.grid):
            # После сохранения очищаем историю
            self.history.clear()
            print("Карта сохранена")

    def _load_map(self):
        """Загрузить карту"""
        # Работает только в режиме редактирования карты
        if not self.mode_manager.is_map_mode():
            return
            
        if self.map_manager.load_map(self.grid):
            # После загрузки очищаем историю
            self.history.clear()
            print("Карта загружена")

    def _toggle_mode(self):
        """Переключить режим работы"""
        self.mode_manager.toggle_mode()
        current_mode = "редактирования карты" if self.mode_manager.is_map_mode() else "управления роботом"
        print(f"Режим переключен: {current_mode}")

    def update_robot_velocities(self):
        """
        Обновить скорости робота на основе нажатых клавиш

        Вызывается каждый кадр в игровом цикле
        """
        # Только в режиме робота
        if not self.mode_manager.is_robot_mode():
            return

        # Обработка остановки/возобновления симуляции клавишей X
        self._stop_simu()

        # Если симуляция остановлена, не обновляем скорости
        if not self.simu_going:
            return

        # Вычисляем линейную скорость
        linear_velocity = 0.0
        if self.pressed_keys[pygame.K_w]:
            linear_velocity += self.robot.max_linear_velocity
        if self.pressed_keys[pygame.K_s]:
            linear_velocity -= self.robot.max_linear_velocity

        # Вычисляем угловую скорость
        angular_velocity = 0.0
        if self.pressed_keys[pygame.K_a]:
            angular_velocity -= self.robot.max_angular_velocity
        if self.pressed_keys[pygame.K_d]:
            angular_velocity += self.robot.max_angular_velocity

        # Устанавливаем скорости робота
        self.robot.set_velocities(linear_velocity, angular_velocity)