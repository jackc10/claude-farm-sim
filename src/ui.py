# File: src/ui.py

import pygame
import random

# Constants
TILE_SIZE = 32
GRASS_COLOR = (34, 139, 34)  # Forest green
SOIL_COLOR = (139, 69, 19)   # Saddle brown
TILLED_SOIL_COLOR = (92, 64, 51)  # Darker brown
HUD_HEIGHT = 100
HUD_COLOR = (50, 50, 50)  # Dark gray
SHOP_COLOR = (139, 69, 19)  # Brown for shop building
HUD_BACKGROUND_COLOR = (50, 50, 50)
HUD_TEXT_COLOR = (255, 255, 255)
HUD_HIGHLIGHT_COLOR = (255, 200, 0)
HUD_SECTION_COLOR = (70, 70, 70)

class TextureAtlas:
    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        self.textures = {}
        self.grass_grid = []

    def create_grass_texture(self):
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        base_color = (34 + random.randint(-10, 10), 
                      139 + random.randint(-10, 10), 
                      34 + random.randint(-10, 10))
        surface.fill(base_color)
        for _ in range(3):
            start = (random.randint(0, TILE_SIZE), TILE_SIZE)
            end = (start[0], TILE_SIZE - random.randint(5, 15))
            pygame.draw.line(surface, (0, 100, 0), start, end, 1)
        return surface

    def create_soil_texture(self):
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surface.fill(SOIL_COLOR)
        for _ in range(5):
            pos = (random.randint(0, TILE_SIZE), random.randint(0, TILE_SIZE))
            pygame.draw.circle(surface, (101, 67, 33), pos, 1)
        return surface

    def create_tilled_soil_texture(self):
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surface.fill(TILLED_SOIL_COLOR)
        for i in range(3):
            y = (i + 1) * TILE_SIZE // 4
            pygame.draw.line(surface, (66, 40, 14), (0, y), (TILE_SIZE, y), 1)
        return surface

    def create_crop_textures(self):
        textures = []
        for stage in range(4):
            surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            if stage == 0:
                pygame.draw.line(surface, (0, 100, 0), 
                                 (TILE_SIZE // 2, TILE_SIZE), 
                                 (TILE_SIZE // 2, TILE_SIZE // 2 + 5), 2)
            elif stage == 1:
                pygame.draw.line(surface, (0, 100, 0), 
                                 (TILE_SIZE // 2, TILE_SIZE), 
                                 (TILE_SIZE // 2, TILE_SIZE // 2), 2)
                pygame.draw.circle(surface, (50, 205, 50), (TILE_SIZE // 2, TILE_SIZE // 2), 3)
            elif stage == 2:
                pygame.draw.line(surface, (0, 100, 0), 
                                 (TILE_SIZE // 2, TILE_SIZE), 
                                 (TILE_SIZE // 2, 5), 3)
                pygame.draw.circle(surface, (50, 205, 50), (TILE_SIZE // 2, TILE_SIZE // 2), 5)
            else:
                pygame.draw.line(surface, (0, 100, 0), 
                                 (TILE_SIZE // 2, TILE_SIZE), 
                                 (TILE_SIZE // 2, 2), 3)
                pygame.draw.circle(surface, (255, 215, 0), (TILE_SIZE // 2, 7), 7)
            textures.append(surface)
        return textures

    def create_vendor_texture(self):
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # Simple farmer representation
        pygame.draw.rect(surface, (0, 0, 255), (8, 8, 16, 16))  # Blue shirt
        pygame.draw.circle(surface, (255, 200, 150), (16, 6), 6)  # Head
        pygame.draw.rect(surface, (139, 69, 19), (12, 24, 8, 8))  # Brown pants
        return surface

    def create_shop_texture(self):
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surface.fill(SHOP_COLOR)
        # Add some details to make it look like a building
        pygame.draw.rect(surface, (100, 40, 0), (5, 5, TILE_SIZE - 10, TILE_SIZE - 10))
        pygame.draw.rect(surface, (200, 200, 200), (12, 15, 8, 8))  # Window
        return surface

    def generate_textures(self):
        grass_textures = [self.create_grass_texture() for _ in range(10)]
        self.grass_grid = [[random.choice(grass_textures) for _ in range(self.world_width)] 
                           for _ in range(self.world_height)]
        self.textures['soil'] = self.create_soil_texture()
        self.textures['tilled_soil'] = self.create_tilled_soil_texture()
        self.textures['crops'] = self.create_crop_textures()
        self.textures['vendor'] = self.create_vendor_texture()
        self.textures['shop'] = self.create_shop_texture()

texture_atlas = None  # Will be initialized in draw_world

def draw_world(display, world, player):
    global texture_atlas
    if texture_atlas is None:
        texture_atlas = TextureAtlas(world.width, world.height)
        texture_atlas.generate_textures()

    for y in range(world.height):
        for x in range(world.width):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + HUD_HEIGHT, TILE_SIZE, TILE_SIZE)
            if world.grid[y][x] == 0:  # Grass
                display.blit(texture_atlas.grass_grid[y][x], rect)
            elif world.grid[y][x] == 1:  # Untilled soil
                display.blit(texture_atlas.textures['soil'], rect)
            elif world.grid[y][x] == 2:  # Tilled soil
                display.blit(texture_atlas.textures['tilled_soil'], rect)
            elif 3 <= world.grid[y][x] <= 6:  # Growing crops
                display.blit(texture_atlas.textures['tilled_soil'], rect)
                display.blit(texture_atlas.textures['crops'][world.grid[y][x] - 3], rect)
                
                if world.grid[y][x] == 6:  # Fully grown crop, add glow
                    glow_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    pygame.draw.rect(glow_surf, (255, 255, 0, 64), glow_surf.get_rect())
                    display.blit(glow_surf, rect)
            elif world.grid[y][x] == 7:  # Shop
                display.blit(texture_atlas.textures['shop'], rect)

    # Draw vendor
    vendor_rect = pygame.Rect(world.vendor.x * TILE_SIZE, world.vendor.y * TILE_SIZE + HUD_HEIGHT, TILE_SIZE, TILE_SIZE)
    display.blit(texture_atlas.textures['vendor'], vendor_rect)

    # Draw player
    player_rect = pygame.Rect(player.x * TILE_SIZE, player.y * TILE_SIZE + HUD_HEIGHT, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(display, (255, 0, 0), player_rect)  # Simple red rectangle for now

def draw_hud(display, player):
    # Draw HUD background
    pygame.draw.rect(display, HUD_BACKGROUND_COLOR, (0, 0, display.get_width(), HUD_HEIGHT))
    
    # Create a custom font
    font = pygame.font.Font(None, 24)
    large_font = pygame.font.Font(None, 32)
    
    # Draw sections
    section_width = display.get_width() // 4
    for i in range(4):
        pygame.draw.rect(display, HUD_SECTION_COLOR, (i * section_width, 0, section_width, HUD_HEIGHT))
        pygame.draw.line(display, HUD_HIGHLIGHT_COLOR, (i * section_width, 0), (i * section_width, HUD_HEIGHT), 2)
    
    # Player info section
    player_info = large_font.render("Player Info", True, HUD_HIGHLIGHT_COLOR)
    display.blit(player_info, (20, 10))
    tool_text = font.render(f"Tool: {player.current_tool.capitalize()}", True, HUD_TEXT_COLOR)
    display.blit(tool_text, (20, 40))

    # Inventory section
    inventory_text = large_font.render("Inventory", True, HUD_HIGHLIGHT_COLOR)
    display.blit(inventory_text, (section_width + 20, 10))
    seed_text = font.render(f"Seeds: {player.inventory['corn_seeds']}", True, HUD_TEXT_COLOR)
    display.blit(seed_text, (section_width + 20, 40))
    crop_text = font.render(f"Corn: {player.inventory['corn']}", True, HUD_TEXT_COLOR)
    display.blit(crop_text, (section_width + 20, 70))

    # Money section
    money_text = large_font.render("Money", True, HUD_HIGHLIGHT_COLOR)
    display.blit(money_text, (2 * section_width + 20, 10))
    money_value = font.render(f"${player.money}", True, HUD_TEXT_COLOR)
    display.blit(money_value, (2 * section_width + 20, 40))

    # Time section (placeholder for future implementation)
    time_text = large_font.render("Time", True, HUD_HIGHLIGHT_COLOR)
    display.blit(time_text, (3 * section_width + 20, 10))
    day_text = font.render("Day 1", True, HUD_TEXT_COLOR)  # Placeholder
    display.blit(day_text, (3 * section_width + 20, 40))

def draw_shop_window(display, player, vendor):
    window_width, window_height = 300, 200
    window_x = (display.get_width() - window_width) // 2
    window_y = (display.get_height() - window_height) // 2
    
    # Draw window background
    pygame.draw.rect(display, (200, 200, 200), (window_x, window_y, window_width, window_height))
    pygame.draw.rect(display, (100, 100, 100), (window_x, window_y, window_width, window_height), 2)

    font = pygame.font.Font(None, 28)

    # Draw title
    title = font.render("Shop", True, (0, 0, 0))
    display.blit(title, (window_x + 10, window_y + 10))

    # Draw buy button
    buy_button = pygame.Rect(window_x + 10, window_y + 50, 100, 40)
    pygame.draw.rect(display, (0, 255, 0), buy_button)
    buy_text = font.render("Buy Seeds", True, (0, 0, 0))
    display.blit(buy_text, (buy_button.x + 10, buy_button.y + 10))

    # Draw sell button
    sell_button = pygame.Rect(window_x + 10, window_y + 100, 100, 40)
    pygame.draw.rect(display, (255, 0, 0), sell_button)
    sell_text = font.render("Sell Corn", True, (0, 0, 0))
    display.blit(sell_text, (sell_button.x + 10, sell_button.y + 10))

    # Display prices
    seed_price = font.render(f"Seed Price: ${vendor.prices['corn_seeds']}", True, (0, 0, 0))
    display.blit(seed_price, (window_x + 150, window_y + 60))
    corn_price = font.render(f"Corn Price: ${vendor.prices['corn']}", True, (0, 0, 0))
    display.blit(corn_price, (window_x + 150, window_y + 110))

    return buy_button, sell_button