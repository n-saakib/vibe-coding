import random
from constants import GRID_WIDTH, GRID_HEIGHT

class Snake:
    def __init__(self):
        # Initial position (center of grid) and length
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2), 
                     (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
                     (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0) # Moving right initially
        self.new_direction = (1, 0)
        self.growth_pool = 0

    def set_direction(self, direction):
        # Prevent reversing into self
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.new_direction = direction

    def move(self, wrap_around=False):
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
    def __init__(self, snake_body):
        self.position = (0, 0)
        self.spawn(snake_body)

    def spawn(self, snake_body):
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), 
                             random.randint(0, GRID_HEIGHT - 1))
            if self.position not in snake_body:
                break
