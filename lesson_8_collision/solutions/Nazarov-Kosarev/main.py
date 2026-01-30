import sys
import math
from enum import Enum

import pygame


class Grid:
    def __init__(self, width, height, cell_w, cell_h, offset_x=0):
        self.width = width
        self.height = height
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.offset_x = offset_x
        self.cols = width // cell_w
        self.rows = height // cell_h
        self.filled = set()

    def get_cell_at_pos(self, x, y):
        x -= self.offset_x
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        c = int(x // self.cell_w)
        r = int(y // self.cell_h)
        return c, r

    def fill_cell(self, c, r):
        if 0 <= c < self.cols and 0 <= r < self.rows:
            self.filled.add((c, r))

    def clear_cell(self, c, r):
        self.filled.discard((c, r))

    def is_filled(self, c, r):
        return (c, r) in self.filled

    def save_to_file(self, filename):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"{self.cols} {self.rows}\n")
                for r in range(self.rows):
                    line = "".join("1" if (c, r) in self.filled else "0"
                                   for c in range(self.cols))
                    f.write(line + "\n")
            print("Карта сохранена в", filename)
        except Exception as e:
            print("Ошибка сохранения карты:", e)

    def load_from_file(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                first = f.readline()
                self.filled.clear()
                for r, line in enumerate(f):
                    line = line.strip()
                    if r >= self.rows:
                        break
                    for c, ch in enumerate(line):
                        if c >= self.cols:
                            break
                        if ch == "1":
                            self.filled.add((c, r))
            print("Карта загружена из", filename)
        except FileNotFoundError:
            print("Файл карты не найден:", filename)
        except Exception as e:
            print("Ошибка загрузки карты:", e)


class History:
    def __init__(self):
        self.actions = []

    def add(self, action):
        self.actions.append(action)

    def undo(self, grid: Grid):
        if not self.actions:
            return
        a = self.actions.pop()
        t = a["type"]
        c, r = a["cell"]
        if t == "fill":
            grid.clear_cell(c, r)
        elif t == "erase":
            grid.fill_cell(c, r)

    def clear(self, grid: Grid):
        grid.filled.clear()
        self.actions.clear()


class Robot:
    def __init__(self, x, y, angle=0.0,
                 max_lin=10.0, max_ang=5.0, radius=1.0):
        self.x = float(x)
        self.y = float(y)
        self.angle = float(angle)
        self.radius = float(radius)
        self.max_lin = float(max_lin)
        self.max_ang = float(max_ang)
        self.lin_v = 0.0
        self.ang_v = 0.0

    def set_velocities(self, lin, ang):
        lin = max(min(lin, self.max_lin), -self.max_lin)
        ang = max(min(ang, self.max_ang), -self.max_ang)
        self.lin_v = lin
        self.ang_v = ang

    def _sector_cells(self, grid: Grid, base_angle,
                      radius_factor=2.0, sector_deg=45.0):
        cells = set()
        R = radius_factor * self.radius
        sector = math.radians(sector_deg)
        for c in range(int(self.x - R), int(self.x + R) + 1):
            for r in range(int(self.y - R), int(self.y + R) + 1):
                if 0 <= c < grid.cols and 0 <= r < grid.rows:
                    dx = (c + 0.5) - self.x
                    dy = (r + 0.5) - self.y
                    d = math.hypot(dx, dy)
                    if 0.1 < d <= R:
                        ang = math.atan2(dy, dx)
                        diff = ang - base_angle
                        while diff > math.pi:
                            diff -= 2 * math.pi
                        while diff < -math.pi:
                            diff += 2 * math.pi
                        if abs(diff) <= sector:
                            cells.add((c, r))
        return cells

    def detection_zone(self, grid: Grid):
        cells = set()
        R = 2 * self.radius
        for c in range(int(self.x - R), int(self.x + R) + 1):
            for r in range(int(self.y - R), int(self.y + R) + 1):
                if 0 <= c < grid.cols and 0 <= r < grid.rows:
                    dx = (c + 0.5) - self.x
                    dy = (r + 0.5) - self.y
                    if math.hypot(dx, dy) <= R:
                        cells.add((c, r))
        return cells

    def forward_sector(self, grid: Grid):
        return self._sector_cells(grid, self.angle)

    def update_with_collision(self, dt, grid: Grid):
        self.angle = (self.angle + self.ang_v * dt) % (2 * math.pi)
        if abs(self.lin_v) < 1e-3:
            return
        if self.lin_v >= 0:
            move_angle = self.angle
        else:
            move_angle = self.angle + math.pi
        cells = self._sector_cells(grid, move_angle)
        for c, r in cells:
            if grid.is_filled(c, r):
                return
        self.x += self.lin_v * math.cos(self.angle) * dt
        self.y += self.lin_v * math.sin(self.angle) * dt

    def clamp(self, min_x, max_x, min_y, max_y):
        self.x = max(min_x, min(max_x, self.x))
        self.y = max(min_y, min(max_y, self.y))


class Mode(Enum):
    MAP = 1
    MANUAL = 2
    AUTO = 3


class ModeManager:
    def __init__(self):
        self.mode = Mode.MAP

    def next_mode(self):
        if self.mode == Mode.MAP:
            self.mode = Mode.MANUAL
        elif self.mode == Mode.MANUAL:
            self.mode = Mode.AUTO
        else:
            self.mode = Mode.MAP

    def is_map(self):
        return self.mode == Mode.MAP

    def is_manual(self):
        return self.mode == Mode.MANUAL

    def is_auto(self):
        return self.mode == Mode.AUTO

    def name(self):
        if self.mode == Mode.MAP:
            return "РЕДАКТОР КАРТЫ"
        if self.mode == Mode.MANUAL:
            return "РОБОТ (РУЧНОЙ)"
        return "РОБОТ (АВТО)"


class InputManager:
    def __init__(self, grid, history, running_flag, mode_mgr, robot):
        self.grid = grid
        self.history = history
        self.running_flag = running_flag
        self.mode_mgr = mode_mgr
        self.robot = robot
        self.left_down = False
        self.right_down = False
        self.last_draw = None
        self.last_erase = None
        self.pressed = {
            pygame.K_w: False,
            pygame.K_s: False,
            pygame.K_a: False,
            pygame.K_d: False,
        }
        self.bindings = {}
        self._setup_bindings()

    def _setup_bindings(self):
        self.bindings[pygame.K_ESCAPE] = self._exit
        self.bindings[pygame.K_z] = self._undo
        self.bindings[pygame.K_c] = self._clear
        self.bindings[pygame.K_TAB] = self.mode_mgr.next_mode
        self.bindings[pygame.K_r] = self._place_robot
        # сохранение и загрузка по S / L
        self.bindings[pygame.K_s] = self._save_map
        self.bindings[pygame.K_l] = self._load_map

    def _exit(self):
        self.running_flag[0] = False

    def _undo(self):
        self.history.undo(self.grid)

    def _clear(self):
        self.history.clear(self.grid)

    def _place_robot(self):
        mx, my = pygame.mouse.get_pos()
        cell = self.grid.get_cell_at_pos(mx, my)
        if cell is None:
            return
        c, r = cell
        self.robot.x = c + 0.5
        self.robot.y = r + 0.5

    def _save_map(self):
        if not self.mode_mgr.is_map():
            return
        self.grid.save_to_file("map.txt")

    def _load_map(self):
        if not self.mode_mgr.is_map():
            return
        self.grid.load_from_file("map.txt")

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key in self.pressed:
                self.pressed[e.key] = True
            func = self.bindings.get(e.key)
            if func:
                func()
        elif e.type == pygame.KEYUP:
            if e.key in self.pressed:
                self.pressed[e.key] = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                self.left_down = True
                self.last_draw = None
            elif e.button == 3:
                self.right_down = True
                self.last_erase = None
        elif e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1:
                self.left_down = False
            elif e.button == 3:
                self.right_down = False

    def handle_mouse_motion(self, mx, my):
        if not self.mode_mgr.is_map():
            return
        cell = self.grid.get_cell_at_pos(mx, my)
        if cell is None:
            return
        c, r = cell
        if self.left_down and cell != self.last_draw:
            self.grid.fill_cell(c, r)
            self.history.add({"type": "fill", "cell": (c, r)})
            self.last_draw = cell
        if self.right_down and cell != self.last_erase:
            if self.grid.is_filled(c, r):
                self.grid.clear_cell(c, r)
                self.history.add({"type": "erase", "cell": (c, r)})
            self.last_erase = cell

    def update_robot_velocities(self):
        if self.mode_mgr.is_map():
            self.robot.set_velocities(0.0, 0.0)
            return
        if self.mode_mgr.is_manual():
            lin = 0.0
            ang = 0.0
            if self.pressed[pygame.K_w]:
                lin += self.robot.max_lin
            if self.pressed[pygame.K_s]:
                lin -= self.robot.max_lin
            # положительный угол крутит вправо, отрицательный — влево
            if self.pressed[pygame.K_a]:
                ang -= self.robot.max_ang  # влево
            if self.pressed[pygame.K_d]:
                ang += self.robot.max_ang  # вправо
            self.robot.set_velocities(lin, ang)
            return
        if self.mode_mgr.is_auto():
            fwd = self.robot.forward_sector(self.grid)
            obstacle = any(self.grid.is_filled(c, r) for c, r in fwd)
            if not obstacle:
                self.robot.set_velocities(self.robot.max_lin * 0.7, 0.0)
            else:
                # вращаемся влево
                self.robot.set_velocities(0.0, -self.robot.max_ang * 0.7)


class Renderer:
    def __init__(self, screen, panel_w=0):
        self.screen = screen
        self.panel_w = panel_w
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.DARK = (100, 100, 100)
        self.BLUE = (120, 150, 255)
        self.GREEN = (50, 200, 50)
        self.RED = (255, 120, 120)
        self.YELLOW = (255, 255, 80)
        self.BLACK = (0, 0, 0)
        self.font = pygame.font.Font(None, 20)

    def draw_grid(self, grid: Grid, hover):
        self.screen.fill(self.WHITE)
        for c, r in grid.filled:
            x = c * grid.cell_w + grid.offset_x
            y = r * grid.cell_h
            pygame.draw.rect(self.screen, self.DARK,
                             (x, y, grid.cell_w, grid.cell_h))
        if hover and not grid.is_filled(*hover):
            c, r = hover
            x = c * grid.cell_w + grid.offset_x
            y = r * grid.cell_h
            pygame.draw.rect(self.screen, self.BLUE,
                             (x, y, grid.cell_w, grid.cell_h))
        for c in range(grid.cols + 1):
            x = c * grid.cell_w + grid.offset_x
            pygame.draw.line(self.screen, self.GRAY, (x, 0), (x, grid.height), 1)
        for r in range(grid.rows + 1):
            y = r * grid.cell_h
            pygame.draw.line(self.screen, self.GRAY,
                             (grid.offset_x, y),
                             (grid.offset_x + grid.width, y), 1)

    def draw_robot(self, robot: Robot, grid: Grid):
        sx = robot.x * grid.cell_w + grid.offset_x
        sy = robot.y * grid.cell_h
        rp = int(robot.radius * (grid.cell_w + grid.cell_h) / 2)
        pygame.draw.circle(self.screen, self.GREEN, (int(sx), int(sy)), rp)
        ex = sx + rp * math.cos(robot.angle)
        ey = sy + rp * math.sin(robot.angle)
        pygame.draw.line(self.screen, self.BLACK, (sx, sy), (ex, ey), 3)

    def draw_detection(self, robot: Robot, grid: Grid):
        for c, r in robot.detection_zone(grid):
            s = pygame.Surface((grid.cell_w, grid.cell_h))
            s.set_alpha(40)
            s.fill(self.BLUE)
            x = c * grid.cell_w + grid.offset_x
            y = r * grid.cell_h
            self.screen.blit(s, (x, y))
        for c, r in robot.forward_sector(grid):
            s = pygame.Surface((grid.cell_w, grid.cell_h))
            s.set_alpha(80)
            color = self.RED if grid.is_filled(c, r) else self.YELLOW
            s.fill(color)
            x = c * grid.cell_w + grid.offset_x
            y = r * grid.cell_h
            self.screen.blit(s, (x, y))

    def draw_panel(self, robot: Robot, mode_mgr: ModeManager, grid: Grid):
        if self.panel_w == 0:
            return
        pygame.draw.rect(self.screen, (50, 50, 50),
                         (0, 0, self.panel_w, self.screen.get_height()))
        y = 10

        def line(text, color=(255, 255, 255)):
            nonlocal y
            surf = self.font.render(text, True, color)
            self.screen.blit(surf, (10, y))
            y += 22

        line(f"Режим: {mode_mgr.name()}", (255, 255, 0))
        line("")
        line(f"X робота: {robot.x:.2f}")
        line(f"Y робота: {robot.y:.2f}")
        line(f"Угол: {math.degrees(robot.angle):.1f}°")
        line("")
        det = robot.detection_zone(grid)
        fwd = robot.forward_sector(grid)
        in_zone = sum(1 for c, r in det if grid.is_filled(c, r))
        ahead = sum(1 for c, r in fwd if grid.is_filled(c, r))
        line("Препятствия:")
        line(f"В зоне: {in_zone}")
        col = (255, 100, 100) if ahead > 0 else (255, 255, 255)
        line(f"Впереди: {ahead}", col)
        line("")
        line("Управление:", (100, 200, 255))
        line("TAB  - сменить режим")
        line("R    - робот под курсор")
        line("ЛКМ  - препятствие")
        line("ПКМ  - стереть")
        line("Z    - отмена")
        line("C    - очистить карту")
        line("S  - сохранить карту")
        line("L  - загрузить карту")
        line("")
        line("Ручной режим:", (150, 220, 255))
        line("W/S  - вперёд / назад")
        line("A/D  - поворот влево / вправо")
        line("")
        line("Авто режим:", (150, 220, 255))
        line("Едет вперёд, пока нет")
        line("стены в секторе.")
        line("У стены крутится влево.")


def main():
    pygame.init()
    panel_w = 220
    grid_w = 800
    h = 600
    w = panel_w + grid_w
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Сим робота")
    cols = 75
    rows = 50
    cell_w = grid_w // cols
    cell_h = h // rows
    grid = Grid(grid_w, h, cell_w, cell_h, offset_x=panel_w)
    history = History()
    mode_mgr = ModeManager()
    robot = Robot(cols / 2, rows / 2, radius=1.0)
    running = [True]
    inp = InputManager(grid, history, running, mode_mgr, robot)
    renderer = Renderer(screen, panel_w=panel_w)
    clock = pygame.time.Clock()

    while running[0]:
        dt = clock.tick(60) / 1000.0
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running[0] = False
            else:
                inp.handle_event(e)
        mx, my = pygame.mouse.get_pos()
        hover = grid.get_cell_at_pos(mx, my) if mode_mgr.is_map() else None
        if mode_mgr.is_map():
            inp.handle_mouse_motion(mx, my)
        inp.update_robot_velocities()
        if mode_mgr.is_manual() or mode_mgr.is_auto():
            robot.update_with_collision(dt, grid)
            robot.clamp(robot.radius,
                        grid.cols - robot.radius,
                        robot.radius,
                        grid.rows - robot.radius)
        renderer.draw_grid(grid, hover)
        renderer.draw_robot(robot, grid)
        if mode_mgr.is_manual() or mode_mgr.is_auto():
            renderer.draw_detection(robot, grid)
        renderer.draw_panel(robot, mode_mgr, grid)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
