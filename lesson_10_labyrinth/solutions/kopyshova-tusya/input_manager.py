"""Модуль для управления вводом с клавиатуры и мыши"""
import pygame

class InputManager:
    """Класс для управления всем вводом (мышь + клавиатура)"""

    def __init__(self, grid, history, map_manager, running_flag, mode_manager, robot):
        """
        Инициализация менеджера ввода

        Args:
            grid: объект Grid
            history: объект History
            map_manager: объект MapManager 
            running_flag: список [True/False] для управления циклом
        """
        self.grid = grid
        self.history = history
        self.running_flag = running_flag
        self.mode_manager = mode_manager
        self.robot = robot
        self.map_manager = map_manager 

        # Флаги состояния мыши
        self.left_mouse_pressed = False
        self.right_mouse_pressed = False
        self.last_drawn_cell = None
        self.last_erased_cell = None

        self.simu_going = True
        self.old_linear = 0
        self.old_angular = 0


        # Формат: {код_клавиши: True/False}
        self.pressed_keys = {
            pygame.K_w: False, 
            pygame.K_s: False,  
            pygame.K_a: False,  
            pygame.K_d: False,
            pygame.K_x: False   # для остановки симуляции
        }


        self.key_bindings = {}

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
        self.bind_key(pygame.K_ESCAPE, "выход", self._exit_program)
        self.bind_key(pygame.K_h, "показать справку", self._show_help)
        self.bind_key(pygame.K_z, "отменить последнее действие", self._undo_action)
        self.bind_key(pygame.K_c, "очистить всё", self._clear_all)

        self.bind_key(pygame.K_TAB, "переключить режим", self._toggle_mode)

        self.bind_key(pygame.K_u, "сохранить карту", self._save_map)
        self.bind_key(pygame.K_l, "загрузить карту", self._load_map)

        
    def handle_event(self, event):
        """
        Обработать событие pygame

        Args:
            event: объект события pygame
        """
        if event.type == pygame.KEYDOWN:
            if event.key in self.pressed_keys:
                self.pressed_keys[event.key] = True

            if event.key in self.key_bindings:
                # Вызываем привязанную функцию
                self.key_bindings[event.key]['function']()

        elif event.type == pygame.KEYUP:  # KEYUP
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
        if not self.mode_manager.is_map_mode():
            return 

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

    # ===== Функции-обработчики команд =====

    def _exit_program(self):
        """Выход из программы"""
        self.running_flag[0] = False
        print("Выход из программы")


    def _undo_action(self):
        """Отменить последнее действие"""
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
        self.grid.clear_all()
        self.history.clear()
        print("Сетка и история очищены")


    def _show_help(self):
        """Показать справку по управлению"""
        print("\n" + "="*50)
        print("УПРАВЛЕНИЕ:")
        print("="*50)

        for key, binding in self.key_bindings.items():
            # Получаем название клавиши
            key_name = pygame.key.name(key).upper()
            description = binding['description']
            print(f"  {key_name} - {description}")

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
        if self.map_manager.save_map(self.grid):
            self.history.clear()


    def _load_map(self):
        """Загрузить карту"""
        if self.map_manager.load_map(self.grid):
            self.history.clear()


    def _toggle_mode(self):
        """Переключить режим работы"""
        self.mode_manager.toggle_mode()


    def _stop_simu(self):
        """остановить симуляцию и полюбоваться результатом проделанной работы"""

        if not self.mode_manager.is_robot_mode():
            return

        if self.pressed_keys.get(pygame.K_x, False):

            if self.simu_going:
                self.old_linear = self.robot.linear_velocity
                self.old_angular = self.robot.angular_velocity

                self.robot.set_velocities(0, 0)

                self.simu_going = False

        else:

            if not self.simu_going:

                self.robot.set_velocities(self.old_linear, self.old_angular)

                self.old_linear = 0
                self.old_angular = 0

                self.simu_going = True


    def update_robot_velocities(self):
        """
        Обновить скорости робота на основе нажатых клавиш

        Вызывается каждый кадр в игровом цикле
        """
        # Только в режиме робота
        if not self.mode_manager.is_robot_mode():
            linear_velocity = 0.0

            if self.pressed_keys[pygame.K_w]:
                linear_velocity += self.robot.max_linear_velocity  
            if self.pressed_keys[pygame.K_s]:  
                linear_velocity -= self.robot.max_linear_velocity

            angular_velocity = 0.0

            if self.pressed_keys[pygame.K_a]:  # A
                angular_velocity -= self.robot.max_angular_velocity 

            if self.pressed_keys[pygame.K_d]:  # D
                angular_velocity += self.robot.max_angular_velocity

            self.robot.set_velocities(linear_velocity, angular_velocity)

            return        
        
        self._stop_simu()

        if not self.simu_going:
            return
        
        