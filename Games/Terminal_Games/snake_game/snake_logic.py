import random
from constants import GRID_WIDTH as INITIAL_GRID_WIDTH, GRID_HEIGHT as INITIAL_GRID_HEIGHT

# Current grid dimensions (can be updated by main.py)
GRID_WIDTH = INITIAL_GRID_WIDTH
GRID_HEIGHT = INITIAL_GRID_HEIGHT

def set_grid_dimensions(width, height):
    global GRID_WIDTH, GRID_HEIGHT
    GRID_WIDTH = width
    GRID_HEIGHT = height

class Snake:
    MAX_QUEUE_SIZE = 2

    def __init__(self):
        # Initial position (center of grid) and length
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2), 
                     (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
                     (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0) # Moving right initially
        self.new_direction = (1, 0)
        self.growth_pool = 0
        self.command_queue = []  # F1: Input buffering queue
        self.prev_body = list(self.body)  # F5: For interpolation

    def set_direction(self, direction):
        """Enqueue a directional command. Validates: no reverse, no duplicate of last queued."""
        # Determine reference direction: last queued if any, otherwise current
        ref = self.command_queue[-1] if self.command_queue else self.direction
        # Block reverse of reference direction
        if (direction[0] * -1, direction[1] * -1) == ref:
            return
        # Block duplicate of last queued entry
        if self.command_queue and direction == self.command_queue[-1]:
            return
        # Enqueue if there's room
        if len(self.command_queue) < self.MAX_QUEUE_SIZE:
            self.command_queue.append(direction)

    def process_queue(self):
        """Pop one command from the queue and apply it. Called once per tick before move()."""
        if self.command_queue:
            self.new_direction = self.command_queue.pop(0)

    def move(self, wrap_around=False):
        self.prev_body = list(self.body)  # F5: Save previous positions
        self.direction = self.new_direction
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        
        new_head_x = head_x + dir_x
        new_head_y = head_y + dir_y
        
        if wrap_around:
            new_head_x %= GRID_WIDTH
            new_head_y %= GRID_HEIGHT
            
        new_head = (new_head_x, new_head_y)
        self.body.insert(0, new_head)
        
        if self.growth_pool > 0:
            self.growth_pool -= 1
        else:
            self.body.pop()

    def grow(self, amount=1):
        self.growth_pool += amount

    def check_collision(self, wall_collision=True):
        head = self.body[0]
        # Wall collision
        if wall_collision:
            if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
                return True
        # Self collision
        if head in self.body[1:]:
            return True
        return False

class Food:
    def __init__(self, snake_body, other_food_pos=None):
        self.position = (0, 0)
        self.spawn(snake_body, other_food_pos)

    def spawn(self, snake_body, other_food_pos=None):
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), 
                             random.randint(0, GRID_HEIGHT - 1))
            if self.position not in snake_body and self.position != other_food_pos:
                break

class BonusFood(Food):
    def __init__(self, snake_body, other_food_pos=None):
        super().__init__(snake_body, other_food_pos)
        self.active = False
        self.timer = 0
        self.size = 3 # 3x3 grid cells

    def spawn(self, snake_body, other_food_pos=None):
        # Ensure it doesn't spawn too close to the edges to avoid clipping
        while True:
            self.position = (random.randint(1, GRID_WIDTH - 2), 
                             random.randint(1, GRID_HEIGHT - 2))
            
            # Check if any part of the 3x3 area overlaps with snake or other food
            overlap = False
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    cell = (self.position[0] + dx, self.position[1] + dy)
                    if cell in snake_body or cell == other_food_pos:
                        overlap = True
                        break
                if overlap: break
            
            if not overlap:
                break
        self.active = True

    def is_hit(self, head_pos):
        # Check if head is within the size x size area centered at self.position
        hx, hy = head_pos
        px, py = self.position
        # Use absolute difference with size // 2 to ensure we cover the full area
        half = self.size // 2
        return abs(int(hx) - int(px)) <= half and abs(int(hy) - int(py)) <= half
