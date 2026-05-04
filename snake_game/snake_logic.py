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
        self.grow_pending = False

    def set_direction(self, direction):
        # Prevent reversing into self
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.new_direction = direction

    def move(self):
        self.direction = self.new_direction
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        self.body.insert(0, new_head)
        
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False

    def grow(self):
        self.grow_pending = True

    def check_collision(self):
        head = self.body[0]
        # Wall collision
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
