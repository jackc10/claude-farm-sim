# File: game_objects.py

import time

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = {"seeds": 5, "crops": 0}
        self.current_tool = "hands"
        self.money = 0

    def move(self, dx, dy, world):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < world.width and 0 <= new_y < world.height:
            self.x = new_x
            self.y = new_y

    def interact(self, world):
        if self.current_tool == "hoe":
            self.till_soil(world)
        elif self.current_tool == "hands" and self.inventory["seeds"] > 0:
            self.plant_seed(world)
        else:
            print(f"Interacting with tile at ({self.x}, {self.y}) using {self.current_tool}")

    def till_soil(self, world):
        if world.grid[self.y][self.x] == 0:  # If it's grass
            world.grid[self.y][self.x] = 2  # 2 represents tilled soil
            print(f"Tilled soil at ({self.x}, {self.y})")
        else:
            print("Can't till here!")

    def plant_seed(self, world):
        if world.grid[self.y][self.x] == 2:  # If it's tilled soil
            world.plant_seed(self.x, self.y)
            self.inventory["seeds"] -= 1
            print(f"Planted seed at ({self.x}, {self.y}). {self.inventory['seeds']} seeds left.")
        else:
            print("Can't plant here!")

    def switch_tool(self):
        self.current_tool = "hoe" if self.current_tool == "hands" else "hands"
        print(f"Switched to {self.current_tool}")

    def harvest(self, world):
        if world.grid[self.y][self.x] == 6:  # Fully grown crop
            world.harvest_crop(self.x, self.y)
            self.inventory["crops"] += 1
            print(f"Harvested crop at ({self.x}, {self.y}). Total crops: {self.inventory['crops']}")
        else:
            print("Nothing to harvest here!")

    def sell_crops(self, price_per_crop=10):
        crops_to_sell = self.inventory["crops"]
        if crops_to_sell > 0:
            earned_money = crops_to_sell * price_per_crop
            self.money += earned_money
            self.inventory["crops"] = 0
            print(f"Sold {crops_to_sell} crops for ${earned_money}. New balance: ${self.money}")
        else:
            print("No crops to sell!")

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.crops = {}
        self.last_update_time = time.time()

    def plant_seed(self, x, y):
        self.grid[y][x] = 3  # 3 represents a newly planted seed
        self.crops[(x, y)] = {"growth_stage": 0, "plant_time": time.time()}

    def update_crops(self):
        current_time = time.time()
        if current_time - self.last_update_time >= 5:  # Check if 5 seconds have passed
            for (x, y), crop in self.crops.items():
                growth_time = current_time - crop["plant_time"]
                if growth_time >= 30:  # Fully grown after 30 seconds
                    self.grid[y][x] = 6  # 6 represents a fully grown crop
                elif growth_time >= 25:
                    self.grid[y][x] = 5  # 5 represents almost grown crop
                elif growth_time >= 20:
                    self.grid[y][x] = 5  # 5 represents almost grown crop
                elif growth_time >= 15:
                    self.grid[y][x] = 4  # 4 represents medium growth crop
                elif growth_time >= 10:
                    self.grid[y][x] = 4  # 4 represents medium growth crop
                elif growth_time >= 5:
                    self.grid[y][x] = 3  # 3 represents small growth crop
            self.last_update_time = current_time

    def harvest_crop(self, x, y):
        if self.grid[y][x] == 6:  # If it's a fully grown crop
            self.grid[y][x] = 2  # Set back to tilled soil
            del self.crops[(x, y)]  # Remove the crop data