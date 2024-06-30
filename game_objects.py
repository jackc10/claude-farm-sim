# File: game_objects.py

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = []
        self.current_tool = "hands"

    def move(self, dx, dy, world):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < world.width and 0 <= new_y < world.height:
            self.x = new_x
            self.y = new_y

    def interact(self, world):
        if self.current_tool == "hoe":
            self.till_soil(world)
        else:
            print(f"Interacting with tile at ({self.x}, {self.y}) using {self.current_tool}")

    def till_soil(self, world):
        if world.grid[self.y][self.x] == 0:  # If it's grass
            world.grid[self.y][self.x] = 2  # 2 will represent tilled soil
            print(f"Tilled soil at ({self.x}, {self.y})")
        else:
            print("Can't till here!")

    def switch_tool(self):
        self.current_tool = "hoe" if self.current_tool == "hands" else "hands"
        print(f"Switched to {self.current_tool}")

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        # Initialize world (add some soil tiles, etc.)
        for i in range(5, 10):
            for j in range(5, 10):
                self.grid[i][j] = 1  # 1 represents untilled soil