import math
import time


class Controller:

    def __init__(
        self,
        robot,
        *,
        linear_speed: float = 40.0,
        angular_step: float = 0.001,
        hit_window_seconds: float = 5.0,
    ):
        self.robot = robot
        self.linear_speed = linear_speed
        self.angular_step = angular_step
        self.hit_count = 0
        self.hit_times = []
        self.hit_window_seconds = hit_window_seconds
        self.consecutive_hits = 0
        self.last_hit_time = None

    def update(self, dt: float, grid):
        now = time.time()

        forward_cells = self.robot.get_forward_sector_cells(grid)
        wall_cells = [
            (col, row)
            for col, row in forward_cells
            if grid.is_cell_filled(col, row)
        ]

        angular_velocity = self.robot.angular_velocity

        
        self._register_hit(now)
        
        if self.last_hit_time is not None and (now - self.last_hit_time) < 0.2:
            self.consecutive_hits += 1
        else:
            self.consecutive_hits = 1
        self.last_hit_time = now
        if len(wall_cells) != 0:
            wall_position = self._get_wall_position(wall_cells)
        
            step = self.angular_step
            
            
            if wall_position == 'left':
                angular_velocity += step
            else:
                angular_velocity -= step
        

        max_w = self.robot.max_angular_velocity
        angular_velocity = max(-max_w, min(max_w, angular_velocity))

        linear_velocity = self.linear_speed

        self.robot.set_velocities(linear_velocity, angular_velocity)

    def _register_hit(self, now: float) -> None:
        self.hit_count += 1
        self.hit_times.append(now)

        cutoff = now - self.hit_window_seconds
        self.hit_times = [t for t in self.hit_times if t >= cutoff]

    def _get_hit_frequency(self, now: float) -> float:
        if not self.hit_times:
            return 0.0

        cutoff = now - self.hit_window_seconds
        recent_hits = [t for t in self.hit_times if t >= cutoff]
        if not recent_hits:
            return 0.0

        window = max(self.hit_window_seconds, 0.1)
        return len(recent_hits) / window

    def _get_wall_position(self, wall_cells) -> str:
        cx = 0.0
        cy = 0.0
        n = len(wall_cells)
        for col, row in wall_cells:
            cx += col + 0.5
            cy += row + 0.5
        cx /= n
        cy /= n

        vx = cx - self.robot.x
        vy = cy - self.robot.y
        
        
        wall_angle = -math.atan2(vy, vx)
        if wall_angle < 0:
            wall_angle = math.pi * 2 - abs(wall_angle)
        
        robot_angle = math.pi * 2 - self.robot.angle
        
        angle_diff = wall_angle - robot_angle
        print("wall angle -", math.degrees(wall_angle))
        print("robot angle -", math.degrees(robot_angle))
        print("angle diff -", math.degrees(angle_diff))
        
        if angle_diff <= 0:
            return "right"
        else:
            return "left"
