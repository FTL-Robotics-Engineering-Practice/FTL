"""
Симуляция математического маятника (метод Эйлера)
Часть 4.2: Маятник без трения

Управление:
  SPACE - пауза/продолжить
  R - перезапуск
  G - показать график θ(t) и E(t)
  UP/DOWN - изменить длину L
  LEFT/RIGHT - изменить g
  ESC - выход

Эксперименты:
  1. Найти g по периоду колебаний
  2. Найти L по периоду колебаний
  3. Наблюдать дрейф энергии (ошибка метода Эйлера!)
"""

import pygame
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================================
# КОНСТАНТЫ И НАЧАЛЬНЫЕ ПАРАМЕТРЫ
# ============================================================================

# Размеры окна
WIDTH, HEIGHT = 1200, 600
FPS = 100

# Физические параметры (можно менять клавишами)
L = 1.0          # длина маятника (метры)
g = 9.81         # ускорение свободного падения (м/с²)
theta = 0.3      # начальный угол (радианы) ~17°
omega = 0.0      # начальная угловая скорость (рад/с)

# Шаг времени
dt = 1.0 / FPS

# Визуализация
ORIGIN_X = WIDTH // 2
ORIGIN_Y = 100
SCALE = 200  # пикселей на метр

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
RED = (255, 50, 50)
GRAY = (150, 150, 150)
GREEN = (50, 255, 50)

# ============================================================================
# ФУНКЦИИ
# ============================================================================

def calculate_energy(L, g, theta, omega, m=1.0):
    """
    Вычисляет полную механическую энергию маятника

    E = E_kinetic + E_potential
    E_kinetic = (1/2) * m * v² = (1/2) * m * (L*ω)²
    E_potential = m * g * h, где h = L * (1 - cos(θ))

    Для упрощения считаем m = 1 кг
    """
    v = L * omega  # линейная скорость
    E_kinetic = 0.5 * m * v**2

    # Высота относительно нижней точки
    h = L * (1 - math.cos(theta))
    E_potential = m * g * h

    return E_kinetic + E_potential


def euler_step(theta, omega, L, g, dt):
    """
    Один шаг метода Эйлера

    Обновление угла и угловой скорости
    """
    alpha = ...  # угловое ускорение

    theta_new = ...
    omega_new = ...

    return theta_new, omega_new


def draw_pendulum(screen, theta, L, font, params_text):
    """Отрисовка маятника"""
    screen.fill(WHITE)

    # Вычисляем позицию грузика
    x = ORIGIN_X + L * SCALE * math.sin(theta)
    y = ORIGIN_Y + L * SCALE * math.cos(theta)

    # Рисуем нить
    pygame.draw.line(screen, BLACK, (ORIGIN_X, ORIGIN_Y), (x, y), 2)

    # Рисуем точку подвеса
    pygame.draw.circle(screen, GRAY, (ORIGIN_X, ORIGIN_Y), 8)

    # Рисуем грузик
    pygame.draw.circle(screen, BLUE, (int(x), int(y)), 20)
    pygame.draw.circle(screen, BLACK, (int(x), int(y)), 20, 2)

    # Отрисовка параметров
    y_offset = 20
    for line in params_text:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (10, y_offset))
        y_offset += 25

    # Инструкции
    instructions = [
        "SPACE - пауза | R - reset | G - график | ESC - выход",
        "UP/DOWN - изменить L | LEFT/RIGHT - изменить g"
    ]
    y_offset = HEIGHT - 60
    for line in instructions:
        text_surface = font.render(line, True, GRAY)
        screen.blit(text_surface, (10, y_offset))
        y_offset += 25


def plot_graphs(time_data, theta_data, energy_data, L, g):
    """
    Построение графиков θ(t) и E(t) через Plotly
    """
    # Создаем subplot с двумя графиками
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Угол θ(t)', 'Энергия E(t)'),
        vertical_spacing=0.12
    )

    # График θ(t)
    fig.add_trace(
        go.Scatter(
            x=time_data,
            y=[math.degrees(t) for t in theta_data],  # конвертируем в градусы
            mode='lines',
            name='θ(t)',
            line=dict(color='blue', width=2)
        ),
        row=1, col=1
    )

    # График E(t)
    E_initial = energy_data[0] if energy_data else 0
    fig.add_trace(
        go.Scatter(
            x=time_data,
            y=energy_data,
            mode='lines',
            name='E(t)',
            line=dict(color='red', width=2)
        ),
        row=2, col=1
    )

    # Линия начальной энергии (для сравнения)
    if energy_data:
        fig.add_trace(
            go.Scatter(
                x=[time_data[0], time_data[-1]],
                y=[E_initial, E_initial],
                mode='lines',
                name='E₀ (начальная)',
                line=dict(color='green', width=1, dash='dash')
            ),
            row=2, col=1
        )

    # Настройка осей
    fig.update_xaxes(title_text="Время (с)", row=1, col=1)
    fig.update_xaxes(title_text="Время (с)", row=2, col=1)
    fig.update_yaxes(title_text="θ (градусы)", row=1, col=1)
    fig.update_yaxes(title_text="Энергия (Дж)", row=2, col=1)

    # Общий заголовок
    period_theoretical = 2 * math.pi * math.sqrt(L / g)
    fig.update_layout(
        title_text=f'Маятник (метод Эйлера): L={L:.2f}м, g={g:.2f}м/с², T_теор={period_theoretical:.3f}с',
        height=800,
        showlegend=True
    )

    # Открываем в браузере
    fig.show()
    print("График открыт в браузере!")


# ============================================================================
# ГЛАВНАЯ ПРОГРАММА
# ============================================================================

def main():
    global L, g, theta, omega

    # Инициализация pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Маятник - Метод Эйлера")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Переменные симуляции
    running = True
    paused = False
    time = 0.0
    frame_count = 0  # счетчик кадров

    # Начальная энергия
    E_initial = calculate_energy(L, g, theta, omega)

    # Данные для графиков
    time_data = []
    theta_data = []
    energy_data = []

    # Главный цикл
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Пауза
                if event.key == pygame.K_SPACE:
                    paused = not paused

                # Перезапуск
                if event.key == pygame.K_r:
                    theta = 0.3
                    omega = 0.0
                    time = 0.0
                    frame_count = 0
                    E_initial = calculate_energy(L, g, theta, omega)
                    time_data.clear()
                    theta_data.clear()
                    energy_data.clear()
                    print("Перезапуск симуляции")

                # График
                if event.key == pygame.K_g:
                    if len(time_data) > 10:
                        print("Генерация графика...")
                        plot_graphs(time_data, theta_data, energy_data, L, g)
                    else:
                        print("Недостаточно данных для графика. Подождите немного.")

                # Изменение L
                if event.key == pygame.K_UP:
                    L += 0.1
                    print(f"L = {L:.2f} м")
                if event.key == pygame.K_DOWN:
                    L = max(0.1, L - 0.1)
                    print(f"L = {L:.2f} м")

                # Изменение g
                if event.key == pygame.K_RIGHT:
                    g += 0.5
                    print(f"g = {g:.2f} м/с²")
                if event.key == pygame.K_LEFT:
                    g = max(0.5, g - 0.5)
                    print(f"g = {g:.2f} м/с²")

                # Выход
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Обновление физики (если не на паузе)
        if not paused:
            theta, omega = euler_step(theta, omega, L, g, dt)
            time += dt
            frame_count += 1

            # Сохраняем данные для графика (каждые 3 кадра для экономии памяти)
            if frame_count % 3 == 0:
                time_data.append(time)
                theta_data.append(theta)
                energy_data.append(calculate_energy(L, g, theta, omega))

        # Вычисление текущей энергии
        E_current = calculate_energy(L, g, theta, omega)
        E_drift = ((E_current - E_initial) / E_initial * 100) if E_initial != 0 else 0

        # Вычисление теоретического периода (для малых углов)
        T_theoretical = 2 * math.pi * math.sqrt(L / g)

        # Текст параметров
        params_text = [
            f"Время: {time:.2f} с",
            f"L = {L:.2f} м",
            f"g = {g:.2f} м/с²",
            f"θ = {math.degrees(theta):.1f}° ({theta:.3f} рад)",
            f"ω = {omega:.3f} рад/с",
            f"E = {E_current:.4f} Дж",
            f"ΔE/E₀ = {E_drift:+.2f}% {'⚠' if abs(E_drift) > 5 else ''}",
            f"T_теор = {T_theoretical:.3f} с",
            f"{'ПАУЗА' if paused else ''}"
        ]

        # Отрисовка
        draw_pendulum(screen, theta, L, font, params_text)
        pygame.display.flip()

        # Ограничение FPS
        clock.tick(FPS)

    pygame.quit()
    print("Программа завершена")


# ============================================================================
# ЭКСПЕРИМЕНТЫ ДЛЯ СТУДЕНТОВ
# ============================================================================

"""
ЭКСПЕРИМЕНТ 1: Измерение g по периоду колебаний

Дано: L = 1.00 м (точно известно)

Задание:
1. Запустите программу (python part_4_2_pendulum.py)
2. Установите L = 1.0 м (используйте ↑↓)
3. Отпустите маятник и засеките время 10 полных колебаний
4. Вычислите период: T = время / 10
5. Используя формулу T = 2π√(L/g), найдите g:

   g = 4π²L / T²

6. Сравните с истинным значением g = 9.81 м/с²
7. Вычислите относительную погрешность

Теория:
- Из формулы периода: T² = 4π²L/g
- Выражаем g: g = 4π²L/T²
- Подставляем измеренные L и T


ЭКСПЕРИМЕНТ 2: Измерение L по периоду колебаний

Дано: g = 9.81 м/с² (считаем точно известным)

Задание:
1. Установите L на случайное значение (например, L = 1.5 м)
2. Запустите симуляцию и измерьте период T
3. Вычислите длину маятника:

   L = gT² / (4π²)

4. Сравните с истинным значением L (показано на экране)
5. Вычислите абсолютную погрешность

Применение:
Этот метод используется для точного измерения g в разных точках Земли!


ЭКСПЕРИМЕНТ 3 (БОНУС): Наблюдение дрейфа энергии

Задание:
1. Запустите маятник с θ₀ = 0.3 рад
2. Наблюдайте параметр ΔE/E₀ на экране
3. Через 30-60 секунд нажмите G для графика
4. Посмотрите на график E(t):
   - Энергия сохраняется? (Должна быть постоянной!)
   - Энергия растет или падает?

Вопросы для размышления:
- Почему энергия не сохраняется, хотя трения нет?
- Это физическая проблема или проблема численного метода?
- Как можно исправить эту проблему? (Подсказка: метод Верле в части 4.3!)

Теория:
Метод Эйлера имеет погрешность O(dt) и НЕ сохраняет энергию.
Для физических симуляций лучше использовать симплектические методы (например, Верле).
"""


if __name__ == "__main__":
    print("=" * 60)
    print("Симуляция маятника - Метод Эйлера")
    print("=" * 60)
    print("Управление:")
    print("  SPACE     - пауза/продолжить")
    print("  R         - перезапуск")
    print("  G         - показать график")
    print("  UP/DOWN   - изменить L")
    print("  LEFT/RIGHT- изменить g")
    print("  ESC       - выход")
    print("=" * 60)

    main()
