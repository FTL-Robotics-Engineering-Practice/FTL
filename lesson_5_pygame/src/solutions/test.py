import pygame
import math

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

class Robot:
    """Класс робота из Занятия 4 + методы для Pygame"""
    
    def __init__(self, name, x=0, y=0):
        # Базовые атрибуты
        self.name = name
        self.x = x
        self.y = y
        self.direction = 0  # градусы
        self.speed = 0
        self.angular_speed = 0
        self.dt = 1/60  # 60 FPS
        
        # История для траектории
        self.history = [(self.x, self.y)]
        
        # Визуальные параметры
        self.radius = 15
        self.color = BLUE
        self.trail_color = (100, 150, 255)
        
    # === ГЕТТЕРЫ ===
    def get_position(self):
        return (self.x, self.y)
    
    def get_direction(self):
        return self.direction
    
    def get_speed(self):
        return self.speed
    
    def get_angular_speed(self):
        return self.angular_speed
    
    # === СЕТТЕРЫ ===
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.history.append((self.x, self.y))
    
    def set_direction(self, new_direction):
        self.direction = new_direction % 360
    
    def set_speed(self, new_speed):
        self.speed = max(0, min(new_speed, 200))
    
    def set_angular_speed(self, new_angular_speed):
        self.angular_speed = max(-180, min(new_angular_speed, 180))
    
    # === ДВИЖЕНИЕ ===
    def move_forward(self, distance):
        """Двигаться вперед на заданное расстояние"""
        rad = math.radians(self.direction)
        self.x += distance * math.cos(rad)
        self.y += distance * math.sin(rad)
        self.history.append((self.x, self.y))
    
    def turn(self, angle):
        """Повернуть на угол"""
        self.direction = (self.direction + angle) % 360
    
    def update(self):
        """Обновление состояния робота (вызывается каждый кадр)"""
        # Поворот
        angle_change = self.angular_speed * self.dt
        self.turn(angle_change)
        
        # Движение
        distance = self.speed * self.dt
        if distance > 0:
            self.move_forward(distance)
    
    # === PYGAME МЕТОДЫ ===
    def draw(self, screen):
        """Рисует робота на экране"""
        # Преобразование координат (центр экрана = (0,0))
        screen_x = int(self.x + WIDTH/2)
        screen_y = int(HEIGHT/2 - self.y)
        
        # Рисуем тело (круг)
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)
        
        # Рисуем направление (треугольник)
        angle = math.radians(self.direction)
        # Вершина треугольника (направление)
        tip_x = screen_x + math.cos(angle) * self.radius * 1
        tip_y = screen_y - math.sin(angle) * self.radius * 1
        
        # Две задние точки (угол 130° вместо 140° для более острого треугольника)
        triangle_angle = 150
        left_angle = angle + math.radians(triangle_angle)
        right_angle = angle - math.radians(triangle_angle)

        offset = 0.5
        
        left_x = screen_x + math.cos(left_angle) * self.radius * offset
        left_y = screen_y - math.sin(left_angle) * self.radius * offset
        
        right_x = screen_x + math.cos(right_angle) * self.radius * offset
        right_y = screen_y - math.sin(right_angle) * self.radius * offset
        
        pygame.draw.polygon(screen, WHITE, [
            (tip_x, tip_y),
            (left_x, left_y),
            (right_x, right_y)
        ])
        
        # Контур
        pygame.draw.circle(screen, BLACK, (screen_x, screen_y), self.radius, 2)
    
    def draw_trail(self, screen, max_points=300):
        """Рисует траекторию движения"""
        if len(self.history) < 2:
            return
        
        # Берем последние N точек
        points = self.history[-max_points:]
        
        # Преобразуем координаты
        screen_points = [
            (int(x + WIDTH/2), 
             int(HEIGHT/2 - y))
            for x, y in points
        ]
        
        # Рисуем линию
        if len(screen_points) > 1:
            pygame.draw.lines(screen, self.trail_color, False, screen_points, 2)
    
    # === ПОЛЕЗНЫЕ МЕТОДЫ ===
    def move_in_circle(self, radius, period):
        """Настроить движение по кругу"""
        circumference = 2 * math.pi * radius
        self.set_speed(circumference / period)
        self.set_angular_speed(360 / period)
    
    def info(self):
        """Информация о роботе"""
        return f"{self.name}: pos=({self.x:.1f}, {self.y:.1f}), dir={self.direction:.1f}°, speed={self.speed:.1f}"


# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===

def draw_grid(screen):
    """Рисует сетку координат"""
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    
    # Вертикальные линии
    for x in range(0, WIDTH, 50):
        color = GRAY if x != center_x else BLACK
        width = 1 if x != center_x else 2
        pygame.draw.line(screen, color, (x, 0), (x, HEIGHT), width)
    
    # Горизонтальные линии
    for y in range(0, HEIGHT, 50):
        color = GRAY if y != center_y else BLACK
        width = 1 if y != center_y else 2
        pygame.draw.line(screen, color, (0, y), (WIDTH, y), width)


def draw_ui(screen, robot, font):
    """Рисует информацию на экране"""
    info_texts = [
        f"Позиция: ({robot.x:.1f}, {robot.y:.1f})",
        f"Направление: {robot.direction:.1f}°",
        f"Скорость: {robot.speed:.1f}",
        f"Угл. скорость: {robot.angular_speed:.1f}°/с",
        "",
        "ПРОБЕЛ - пауза/возобновить",
        "R - сброс позиции"
    ]
    
    y_offset = 10
    for text in info_texts:
        surface = font.render(text, True, BLACK)
        screen.blit(surface, (10, y_offset))
        y_offset += 25


# === ГЛАВНАЯ ПРОГРАММА ===

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Робот в Pygame - Занятие 5")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

# Создаем робота в центре
robot = Robot("Исследователь", x=0, y=0)

# Запускаем движение по кругу
robot.move_in_circle(radius=150, period=8.0)

# Главный игровой цикл
running = True
while running:
    # 1. ОБРАБОТКА СОБЫТИЙ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # Пауза на пробел
            if event.key == pygame.K_SPACE:
                if robot.speed > 0:
                    robot.set_speed(0)
                    robot.set_angular_speed(0)
                else:
                    robot.move_in_circle(radius=150, period=8.0)
            
            # Сброс позиции на R
            if event.key == pygame.K_r:
                robot.set_position(0, 0)
                robot.history = [(0, 0)]
                robot.set_direction(0)
    
    # 2. ОБНОВЛЕНИЕ ЛОГИКИ
    robot.update()
    
    # 3. ОТРИСОВКА
    screen.fill(WHITE)
    draw_grid(screen)
    robot.draw_trail(screen)
    robot.draw(screen)
    draw_ui(screen, robot, font)
    pygame.display.flip()
    
    # 4. КОНТРОЛЬ FPS
    clock.tick(FPS)

pygame.quit()

