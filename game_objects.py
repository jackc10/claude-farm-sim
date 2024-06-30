# File: game_objects.py

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = []  # We'll implement this later

    def move(self, dx, dy, world):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < world.width and 0 <= new_y < world.height:
            self.x = new_x
            self.y = new_y

    def interact(self, world):
        # This is where we'll implement interaction with the world
        # For now, let's just print a message
        print(f"Interacting with tile at ({self.x}, {self.y})")

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        # Initialize world (add some soil tiles, etc.)
        for i in range(5, 10):
            for j in range(5, 10):
                self.grid[i][j] = 1  # 1 represents soil