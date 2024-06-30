# File: ui.py

import pygame
import random

# Constants
TILE_SIZE = 32
GRASS_COLOR = (34, 139, 34)  # Forest green
SOIL_COLOR = (139, 69, 19)   # Saddle brown
TILLED_SOIL_COLOR = (92, 64, 51)  # Darker brown

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

    def generate_textures(self):
        grass_textures = [self.create_grass_texture() for _ in range(10)]
        self.grass_grid = [[random.choice(grass_textures) for _ in range(self.world_width)] 
                           for _ in range(self.world_height)]
        self.textures['soil'] = self.create_soil_texture()
        self.textures['tilled_soil'] = self.create_tilled_soil_texture()
        self.textures['crops'] = self.create_crop_textures()

texture_atlas = None  # Will be initialized in draw_world

def draw_world(display, world, player):
    global texture_atlas
    if texture_atlas is None:
        texture_atlas = TextureAtlas(world.width, world.height)
        texture_atlas.generate_textures()

    for y in range(world.height):
        for x in range(world.width):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
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

    # Draw player
    player_rect = pygame.Rect(player.x * TILE_SIZE, player.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(display, (255, 0, 0), player_rect)  # Simple red rectangle for now

def draw_hud(display, player):
    font = pygame.font.Font(None, 36)
    position_text = font.render(f"Position: ({player.x}, {player.y})", True, (255, 255, 255))
    tool_text = font.render(f"Tool: {player.current_tool}", True, (255, 255, 255))
    seed_text = font.render(f"Seeds: {player.inventory['seeds']}", True, (255, 255, 255))
    crop_text = font.render(f"Crops: {player.inventory['crops']}", True, (255, 255, 255))
    money_text = font.render(f"Money: ${player.money}", True, (255, 255, 255))
    
    display.blit(position_text, (10, 10))
    display.blit(tool_text, (10, 50))
    display.blit(seed_text, (10, 90))
    display.blit(crop_text, (10, 130))
    display.blit(money_text, (10, 170))

    # Draw sell button
    sell_button = pygame.Rect(10, 210, 100, 50)
    pygame.draw.rect(display, (0, 255, 0), sell_button)
    sell_text = font.render("Sell Crops", True, (0, 0, 0))
    display.blit(sell_text, (15, 225))

    return sell_button  # Return the button rect for click detection