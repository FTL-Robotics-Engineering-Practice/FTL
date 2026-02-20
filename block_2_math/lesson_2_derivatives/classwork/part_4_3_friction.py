"""
Симуляция математического маятника с трением (метод Верле)
Часть 4.3: Маятник с затуханием

Управление:
  SPACE - пауза/продолжить
  R - перезапуск
  G - показать график θ(t) и E(t) с огибающей
  +/- - изменить коэффициент трения β
  UP/DOWN - изменить длину L
  LEFT/RIGHT - изменить g
  ESC - выход

Эксперимент:
  Найти β из времени затухания амплитуды!
"""

import pygame
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ============================================================================
# КОНСТАНТЫ И НАЧАЛЬНЫЕ ПАРАМЕТРЫ
# ============================================================================

# Размеры окна
WIDTH, HEIGHT = 1200, 600
FPS = 100

# Физические параметры (можно менять клавишами)
L = 2.0          # длина маятника (метры)
g = 9.81         # ускорение свободного падения (м/с²)
beta = 0.1       # коэффициент затухания (1/с)
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
ORANGE = (255, 165, 0)

# ============================================================================
# ФУНКЦИИ
# ============================================================================

def calculate_energy(L, g, theta, omega, m=1.0):
    """
    Вычисляет полную механическую энергию маятника
    """
    v = L * omega  # линейная скорость
    E_kinetic = 0.5 * m * v**2

    # Высота относительно нижней точки
    h = L * (1 - math.cos(theta))
    E_potential = m * g * h

    return E_kinetic + E_potential


def verlet_step_with_friction(theta, omega, L, g, beta, dt):
    """
    Один шаг метода Верле с трением

    Обновление угла и угловой скорости
    """
    # Шаг 1: текущее ускорение
    alpha_old = ...

    # Шаг 2: обновление позиции
    theta_new = ...

    # Шаг 3: новое ускорение
    # Для точности используем предварительную оценку omega_new
    omega_predicted = ...
    alpha_new = ...

    # Шаг 4: обновление скорости (среднее)
    omega_new = ...

    return theta_new, omega_new


def find_amplitude(theta_history):
    """
    Находит текущую амплитуду по истории углов
    Амплитуда = максимальное отклонение за последние несколько периодов
    """
    if len(theta_history) < 10:
        return 0.0

    # Берем последние N точек
    recent = theta_history[-100:] if len(theta_history) > 100 else theta_history
    return max(abs(min(recent)), abs(max(recent)))


def theoretical_amplitude(t, A0, beta):
    """
    Теоретическая огибающая амплитуды
    A(t) = A₀ * e^(-βt/2)
    """
    return A0 * math.exp(-beta * t / 2)


def draw_amplitude_marks(screen, L, A0, font):
    """Рисует полупрозрачные засечки для визуализации амплитуды (как на линейке)"""
    if A0 <= 0:
        return

    # Создаем полупрозрачную поверхность
    marks_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    radius = L * SCALE

    # Уровни амплитуды с цветами (RGBA с альфа-каналом для прозрачности)
    amplitude_levels = [
        (A0, (255, 50, 50, 180), "A₀", 3),           # Красный - начальная (толще)
        (A0/2, (50, 200, 50, 180), "A₀/2", 2),       # Зеленый - половина
        (A0/4, (50, 150, 255, 180), "A₀/4", 2)       # Голубой - четверть
    ]

    for amplitude, color, label, thickness in amplitude_levels:
        # Вычисляем позицию на траектории (справа и слева)
        for sign in [1, -1]:  # правая и левая стороны
            angle = sign * amplitude

            # Точка на траектории
            x = ORIGIN_X + radius * math.sin(angle)
            y = ORIGIN_Y + radius * math.cos(angle)

            # Вектор перпендикулярный к радиусу (касательная к окружности)
            # Касательная: perpendicular к (sin, cos) = (-cos, sin)
            tangent_x = -math.cos(angle)
            tangent_y = math.sin(angle)

            # Длина засечки
            mark_length = 30

            # Концы засечки
            x1 = x - tangent_x * mark_length / 2
            y1 = y - tangent_y * mark_length / 2
            x2 = x + tangent_x * mark_length / 2
            y2 = y + tangent_y * mark_length / 2

            # Рисуем засечку на полупрозрачной поверхности
            pygame.draw.line(marks_surface, color, (int(x1), int(y1)), (int(x2), int(y2)), thickness)

            # Рисуем цветную точку на траектории (меньше)
            pygame.draw.circle(marks_surface, color, (int(x), int(y)), 3)

    # Накладываем полупрозрачную поверхность поверх основного экрана
    screen.blit(marks_surface, (0, 0))


def draw_pendulum(screen, theta, L, A0, font, params_text):
    """Отрисовка маятника"""
    screen.fill(WHITE)

    # Вычисляем позицию грузика
    x = ORIGIN_X + L * SCALE * math.sin(theta)
    y = ORIGIN_Y + L * SCALE * math.cos(theta)

    # Рисуем нить
    pygame.draw.line(screen, BLACK, (ORIGIN_X, ORIGIN_Y), (x, y), 2)

    # Рисуем точку подвеса
    pygame.draw.circle(screen, GRAY, (ORIGIN_X, ORIGIN_Y), 8)

    # Рисуем грузик (оранжевый для маятника с трением)
    pygame.draw.circle(screen, ORANGE, (int(x), int(y)), 20)
    pygame.draw.circle(screen, BLACK, (int(x), int(y)), 20, 2)

    # Рисуем полупрозрачные засечки амплитуды ПОВЕРХ маятника
    draw_amplitude_marks(screen, L, A0, font)

    # Отрисовка параметров
    y_offset = 20
    for line in params_text:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (10, y_offset))
        y_offset += 25

    # Заголовок
    title_font = pygame.font.Font(None, 36)
    title_surface = title_font.render("Маятник с трением (Верле)", True, ORANGE)
    screen.blit(title_surface, (WIDTH - 400, 20))

    # Инструкции
    instructions = [
        "SPACE - пауза | R - reset | G - график | ESC - выход",
        "+/- - изменить β | UP/DOWN - L | LEFT/RIGHT - g"
    ]
    y_offset = HEIGHT - 60
    for line in instructions:
        text_surface = font.render(line, True, GRAY)
        screen.blit(text_surface, (10, y_offset))
        y_offset += 25


def plot_graphs(time_data, theta_data, energy_data, amplitude_data, L, g, beta, A0):
    """
    Построение графиков θ(t) и E(t) с теоретическими огибающими
    """
    # Создаем subplot с тремя графиками
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Угол θ(t) с огибающей', 'Амплитуда A(t)', 'Энергия E(t)'),
        vertical_spacing=0.10
    )

    # График 1: θ(t) с огибающей
    fig.add_trace(
        go.Scatter(
            x=time_data,
            y=[math.degrees(t) for t in theta_data],
            mode='lines',
            name='θ(t)',
            line=dict(color='blue', width=1)
        ),
        row=1, col=1
    )

    # Теоретическая огибающая
    envelope_upper = [math.degrees(theoretical_amplitude(t, A0, beta)) for t in time_data]
    envelope_lower = [-math.degrees(theoretical_amplitude(t, A0, beta)) for t in time_data]

    fig.add_trace(
        go.Scatter(
            x=time_data,
            y=envelope_upper,
            mode='lines',
            name='Огибающая (теория)',
            line=dict(color='red', width=2, dash='dash')
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=time_data,
            y=envelope_lower,
            mode='lines',
            name='',
            line=dict(color='red', width=2, dash='dash'),
            showlegend=False
        ),
        row=1, col=1
    )

    # График 2: Амплитуда A(t)
    fig.add_trace(
        go.Scatter(
            x=time_data,
            y=[math.degrees(a) for a in amplitude_data],
            mode='lines',
            name='A(t) измеренная',
            line=dict(color='green', width=2)
        ),
        row=2, col=1
    )

    # Теоретическая амплитуда
    theoretical_amp = [math.degrees(theoretical_amplitude(t, A0, beta)) for t in time_data]
    fig.add_trace(
        go.Scatter(
            x=time_data,
            y=theoretical_amp,
            mode='lines',
            name='A(t) теоретическая',
            line=dict(color='red', width=2, dash='dash')
        ),
        row=2, col=1
    )

    # График 3: E(t)
    fig.add_trace(
        go.Scatter(
            x=time_data,
            y=energy_data,
            mode='lines',
            name='E(t)',
            line=dict(color='orange', width=2)
        ),
        row=3, col=1
    )

    # Настройка осей
    fig.update_xaxes(title_text="Время (с)", row=1, col=1)
    fig.update_xaxes(title_text="Время (с)", row=2, col=1)
    fig.update_xaxes(title_text="Время (с)", row=3, col=1)

    fig.update_yaxes(title_text="θ (градусы)", row=1, col=1)
    fig.update_yaxes(title_text="Амплитуда (градусы)", row=2, col=1)
    fig.update_yaxes(title_text="Энергия (Дж)", row=3, col=1)

    # Вычисляем время половинного затухания
    t_half = (2 * math.log(2)) / beta if beta > 0 else float('inf')

    # Общий заголовок
    fig.update_layout(
        title_text=f'Маятник с трением: L={L:.2f}м, g={g:.2f}м/с², β={beta:.3f} 1/с, t₁/₂={t_half:.1f}с',
        height=900,
        showlegend=True
    )

    # Открываем в браузере
    fig.show()
    print("График открыт в браузере!")


# ============================================================================
# ГЛАВНАЯ ПРОГРАММА
# ============================================================================

def main():
    global L, g, beta, theta, omega

    # Инициализация pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Маятник с трением - Метод Верле")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Переменные симуляции
    running = True
    paused = False
    time = 0.0
    frame_count = 0

    # Начальная амплитуда и энергия
    A0 = abs(theta)
    E_initial = calculate_energy(L, g, theta, omega)

    # Данные для графиков
    time_data = []
    theta_data = []
    energy_data = []
    amplitude_data = []

    # История углов для определения амплитуды
    theta_history = []

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
                    A0 = abs(theta)
                    E_initial = calculate_energy(L, g, theta, omega)
                    time_data.clear()
                    theta_data.clear()
                    energy_data.clear()
                    amplitude_data.clear()
                    theta_history.clear()
                    print("Перезапуск симуляции")

                # График
                if event.key == pygame.K_g:
                    if len(time_data) > 10:
                        print("Генерация графика...")
                        plot_graphs(time_data, theta_data, energy_data, amplitude_data, L, g, beta, A0)
                    else:
                        print("Недостаточно данных для графика. Подождите немного.")

                # Изменение β
                if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    beta += 0.01
                    print(f"β = {beta:.3f} 1/с")
                if event.key == pygame.K_MINUS:
                    beta = max(0.0, beta - 0.01)
                    print(f"β = {beta:.3f} 1/с")

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
            theta, omega = verlet_step_with_friction(theta, omega, L, g, beta, dt)
            time += dt
            frame_count += 1

            # История углов для определения амплитуды
            theta_history.append(theta)
            if len(theta_history) > 200:
                theta_history.pop(0)

            # Сохраняем данные для графика (каждые 3 кадра)
            if frame_count % 3 == 0:
                time_data.append(time)
                theta_data.append(theta)
                energy_data.append(calculate_energy(L, g, theta, omega))
                amplitude_data.append(find_amplitude(theta_history))

        # Вычисление параметров
        E_current = calculate_energy(L, g, theta, omega)
        current_amplitude = find_amplitude(theta_history)
        theoretical_amp = theoretical_amplitude(time, A0, beta)

        # Время половинного затухания
        t_half = (2 * math.log(2)) / beta if beta > 0 else float('inf')

        # Теоретический период (без трения, для малых углов)
        T_theoretical = 2 * math.pi * math.sqrt(L / g)

        # Текст параметров
        params_text = [
            f"Время: {time:.2f} с",
            f"L = {L:.2f} м",
            f"g = {g:.2f} м/с²",
            f"β = {beta:.3f} 1/с",
            f"θ = {math.degrees(theta):.1f}° ({theta:.3f} рад)",
            f"ω = {omega:.3f} рад/с",
            f"E = {E_current:.6f} Дж",
            f"A_текущ = {math.degrees(current_amplitude):.1f}°",
            f"A_теор = {math.degrees(theoretical_amp):.1f}°",
            f"t1/2 = {t_half:.1f} с",
            f"T = {T_theoretical:.3f} с",
            f"{'ПАУЗА' if paused else ''}"
        ]

        # Отрисовка
        draw_pendulum(screen, theta, L, A0, font, params_text)
        pygame.display.flip()

        # Ограничение FPS
        clock.tick(FPS)

    pygame.quit()
    print("Программа завершена")


# ============================================================================
# ЭКСПЕРИМЕНТЫ ДЛЯ СТУДЕНТОВ
# ============================================================================

"""
ЭКСПЕРИМЕНТ: Измерение коэффициента затухания β

Теория:
Амплитуда затухающих колебаний убывает экспоненциально:
  A(t) = A₀ * e^(-βt/2)

Время половинного затухания (когда A = A₀/2):
  t₁/₂ = (2*ln(2))/β ≈ 1.386/β

Отсюда:
  β = 1.386/t₁/₂


ЗАДАНИЕ 1: Проверка теории

1. Запустите программу с β = 0.1 (по умолчанию)
2. Посмотрите на экран:
   - A_текущ - измеренная амплитуда
   - A_теор - теоретическая амплитуда A₀*e^(-βt/2)
3. Через 10-20 секунд нажмите G для графика
4. Проверьте:
   - Совпадает ли зеленая линия (измеренная) с красной пунктирной (теория)?
   - График энергии E(t) должен плавно убывать!


ЗАДАНИЕ 2: Найти β из измерений

1. Установите β = 0.15 (нажимайте + несколько раз)
2. Нажмите R для перезапуска
3. Запишите начальную амплитуду A₀ (с экрана)
4. Засеките время когда амплитуда станет A₀/2
   Подсказка: смотрите на A_текущ на экране
5. Вычислите β по формуле:
   β = 1.386 / t₁/₂
6. Сравните с истинным значением β = 0.15


ЗАДАНИЕ 3: Влияние β на затухание

1. Попробуйте разные значения β:
   - β = 0.05 (слабое трение) - долго затухает
   - β = 0.2 (сильное трение) - быстро затухает
   - β = 0 (без трения) - энергия сохраняется!

2. Для каждого случая постройте график (G)
3. Сравните графики амплитуды A(t)


ЗАДАНИЕ 4 (БОНУС): Сравнение с экспериментом

В части 6 урока будет эксперимент с реальным маятником (подшипник).
Измерим β экспериментально и подставим в эту симуляцию.
Симуляция должна совпасть с реальным затуханием!


ВОПРОСЫ ДЛЯ РАЗМЫШЛЕНИЯ:

1. Почему амплитуда убывает как e^(-βt/2), а не e^(-βt)?
   Подсказка: посмотрите на уравнение движения θ'' = -(g/L)θ - βω

2. Что происходит при очень большом β (например, β = 1)?
   Маятник все еще колеблется или сразу останавливается?

3. Как связаны β и энергия?
   График E(t) показывает потерю энергии. Куда уходит энергия?
"""


if __name__ == "__main__":
    print("=" * 60)
    print("Симуляция маятника с трением - Метод Верле")
    print("=" * 60)
    print("Управление:")
    print("  SPACE      - пауза/продолжить")
    print("  R          - перезапуск")
    print("  G          - показать график")
    print("  +/-        - изменить β")
    print("  UP/DOWN    - изменить L")
    print("  LEFT/RIGHT - изменить g")
    print("  ESC        - выход")
    print("=" * 60)
    print("Цель: Измерить коэффициент затухания β!")
    print("=" * 60)

    main()
