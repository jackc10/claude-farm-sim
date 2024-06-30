# File: src/world.py

import time
from .entities import Vendor
from .config import calculate_grid_size, calculate_tile_size

class World:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width, self.height = calculate_grid_size(screen_width, screen_height)
        self.tile_size = calculate_tile_size(screen_width, screen_height)
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.crops = {}
        self.last_update_time = time.time()
        self.vendor = self.place_shop()

    def recalculate_grid(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        new_width, new_height = calculate_grid_size(screen_width, screen_height)
        new_tile_size = calculate_tile_size(screen_width, screen_height)
        
        # Resize grid if necessary
        if new_width != self.width or new_height != self.height:
            new_grid = [[0 for _ in range(new_width)] for _ in range(new_height)]
            for y in range(min(self.height, new_height)):
                for x in range(min(self.width, new_width)):
                    new_grid[y][x] = self.grid[y][x]
            self.grid = new_grid
            self.width, self.height = new_width, new_height
        
        self.tile_size = new_tile_size
        self.vendor.x = min(self.vendor.x, self.width - 1)
        self.vendor.y = min(self.vendor.y, self.height - 1)

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