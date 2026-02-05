"""Модуль для управления вводом с клавиатуры и мыши"""
import pygame


class InputManager:
    """Класс для обработки ввода с клавиатуры и мыши"""

    def __init__(self, robot, grid, history, map_manager, mode_manager, running_flag):
        """
        Инициализация менеджера ввода

        Args:
            robot: объект Robot
            grid: объект Grid
            history: объект History
            map_manager: объект MapManager
            mode_manager: объект ModeManager
            running_flag: список [True/False] для управления циклом
        """
        self.robot = robot
        self.grid = grid
        self.history = history
        self.map_manager = map_manager
        self.mode_manager = mode_manager
        self.running_flag = running_flag

        # Словарь для отслеживания нажатых клавиш робота
        self.pressed_keys = {
            pygame.K_w: False,
            pygame.K_s: False,
            pygame.K_a: False,
            pygame.K_d: False,
        }

        # Флаги для рисования мышью
        self.left_mouse_pressed = False
        self.right_mouse_pressed = False
        self.last_drawn_cell = None
        self.last_erased_cell = None

    def handle_event(self, event):
        """
        Обработать событие pygame

        Args:
            event: объект события pygame
        """
        if event.type == pygame.KEYDOWN:
            self._handle_keydown(event.key)
        elif event.type == pygame.KEYUP:
            self._handle_keyup(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_button_down(event.button)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._handle_mouse_button_up(event.button)

    def _handle_keydown(self, key):
        """Обработать нажатие клавиши"""
        # Выход
        if key == pygame.K_ESCAPE:
            self.running_flag[0] = False
            print("Выход из программы")

        # Переключение режима (TAB)
        elif key == pygame.K_TAB:
            self.mode_manager.toggle_mode()

        # Клавиши для режима карты
        elif self.mode_manager.is_map_mode():
            if key == pygame.K_z:
                self._undo_action()
            elif key == pygame.K_c:
                self._clear_all()
            elif key == pygame.K_k:
                self._save_map()
            elif key == pygame.K_l:
                self._load_map()

        # Клавиши для режима робота
        elif self.mode_manager.is_robot_mode():
            if key in self.pressed_keys:
                self.pressed_keys[key] = True

    def _handle_keyup(self, key):
        """Обработать отпускание клавиши"""
        if key in self.pressed_keys:
            self.pressed_keys[key] = False

    def _handle_mouse_button_down(self, button):
        """Обработать нажатие кнопки мыши"""
        if button == 1:  # Левая кнопка
            self.left_mouse_pressed = True
            self.last_drawn_cell = None
        elif button == 3:  # Правая кнопка
            self.right_mouse_pressed = True
            self.last_erased_cell = None

    def _handle_mouse_button_up(self, button):
        """Обработать отпускание кнопки мыши"""
        if button == 1:
            self.left_mouse_pressed = False
            self.last_drawn_cell = None
        elif button == 3:
            self.right_mouse_pressed = False
            self.last_erased_cell = None

    def handle_mouse_motion(self, mouse_x, mouse_y):
        """
        Обработать движение мыши (рисование/стирание)

        Args:
            mouse_x: координата X мыши
            mouse_y: координата Y мыши
        """
        # Рисование только в режиме карты
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

    def update(self):
        """
        Обновить скорости робота на основе нажатых клавиш
        Вызывается каждый кадр
        """
        # Обновление только в режиме робота
        if not self.mode_manager.is_robot_mode():
            return

        # Вычисляем линейную скорость
        linear_velocity = 0.0
        forward_speed = 50
        if self.pressed_keys[pygame.K_w]:
            linear_velocity += forward_speed
        if self.pressed_keys[pygame.K_s]:
            linear_velocity -= forward_speed

        # Вычисляем угловую скорость
        angular_velocity = 0.0
        rotation_speed = 3
        if self.pressed_keys[pygame.K_a]:
            angular_velocity -= rotation_speed
        if self.pressed_keys[pygame.K_d]:
            angular_velocity += rotation_speed

        # Проверяем коллизию перед установкой скорости
        safe_linear_velocity = self.robot.check_collision(
            self.grid,
            linear_velocity
        )

        # Устанавливаем безопасную скорость
        self.robot.set_velocities(safe_linear_velocity, angular_velocity)

    # ===== Функции-обработчики команд =====

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
            print("История пуста")

    def _clear_all(self):
        """Очистить всю карту"""
        self.grid.clear_all()
        self.history.clear()
        print("Карта очищена")

    def _save_map(self):
        """Сохранить карту"""
        if self.map_manager.save_map(self.grid):
            self.history.clear()

    def _load_map(self):
        """Загрузить карту"""
        if self.map_manager.load_map(self.grid):
            self.history.clear()
