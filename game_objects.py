# File: game_objects.py

import time

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = {"corn_seeds": 5, "corn": 0}
        self.current_tool = "hands"
        self.money = 100  # Starting money

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

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.crops = {}
        self.last_update_time = time.time()
        self.vendor = self.place_shop()

    def place_shop(self):
        shop_x, shop_y = self.width - 2, 1
        self.grid[shop_y][shop_x] = 7  # 7 represents shop
        return Vendor(shop_x, shop_y - 1)  # Vendor stands in front of the shop

    def is_near_vendor(self, x, y):
        return abs(x - self.vendor.x) <= 1 and abs(y - self.vendor.y) <= 1

    def plant_seed(self, x, y):
        self.grid[y][x] = 3  # 3 represents a newly planted seed
        self.crops[(x, y)] = {"growth_stage": 0, "plant_time": time.time()}

    def update_crops(self):
        current_time = time.time()
        if current_time - self.last_update_time >= 5:  # Check if 5 seconds have passed
            for (x, y), crop in list(self.crops.items()):
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