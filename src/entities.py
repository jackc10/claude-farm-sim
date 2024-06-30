# File: src/entities.py

import time

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = {"corn_seeds": 5, "corn": 0}
        self.current_tool = "hands"
        self.money = 100

    def move(self, dx, dy, world):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < world.width and 0 <= new_y < world.height and world.grid[new_y][new_x] != 7:  # 7 is shop
            self.x = new_x
            self.y = new_y

    def interact(self, world):
        if self.current_tool == "hoe":
            self.till_soil(world)
        elif self.current_tool == "hands":
            if world.grid[self.y][self.x] == 6:  # Fully grown crop
                self.harvest(world)
            elif self.inventory["corn_seeds"] > 0 and world.grid[self.y][self.x] == 2:  # Tilled soil
                self.plant_seed(world)
            elif world.is_near_vendor(self.x, self.y):
                return "open_shop"
        return None

    def till_soil(self, world):
        if world.grid[self.y][self.x] == 0:  # If it's grass
            world.grid[self.y][self.x] = 2  # 2 represents tilled soil
            print(f"Tilled soil at ({self.x}, {self.y})")
        else:
            print("Can't till here!")

    def plant_seed(self, world):
        if world.grid[self.y][self.x] == 2:  # If it's tilled soil
            world.plant_seed(self.x, self.y)
            self.inventory["corn_seeds"] -= 1
            print(f"Planted corn seed at ({self.x}, {self.y}). {self.inventory['corn_seeds']} corn seeds left.")
        else:
            print("Can't plant here!")

    def switch_tool(self):
        self.current_tool = "hoe" if self.current_tool == "hands" else "hands"
        print(f"Switched to {self.current_tool}")

    def harvest(self, world):
        if world.grid[self.y][self.x] == 6:  # Fully grown crop
            world.harvest_crop(self.x, self.y)
            self.inventory["corn"] += 1
            print(f"Harvested corn at ({self.x}, {self.y}). Total corn: {self.inventory['corn']}")
        else:
            print("Nothing to harvest here!")

class Vendor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = {"corn_seeds": 1000}
        self.prices = {"corn_seeds": 5, "corn": 10}

    def sell_seeds(self, player, seed_type, amount):
        if seed_type not in self.inventory or self.inventory[seed_type] < amount:
            return False
        cost = self.prices[seed_type] * amount
        if player.money >= cost:
            player.money -= cost
            self.inventory[seed_type] -= amount
            player.inventory[seed_type] = player.inventory.get(seed_type, 0) + amount
            return True
        return False

    def buy_crops(self, player, crop_type, amount):
        if crop_type not in player.inventory or player.inventory[crop_type] < amount:
            return False
        payment = self.prices[crop_type] * amount
        player.money += payment
        player.inventory[crop_type] -= amount
        return True