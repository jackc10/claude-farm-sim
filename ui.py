# File: ui.py

import pygame

TILE_SIZE = 32
GRASS_COLOR = (0, 255, 0)
SOIL_COLOR = (139, 69, 19)
TILLED_SOIL_COLOR = (101, 67, 33)
PLAYER_COLOR = (255, 0, 0)
CROP_COLORS = [
    (0, 100, 0),    # Dark green for small growth
    (0, 150, 0),    # Medium green for medium growth
    (0, 200, 0),    # Light green for almost grown
    (255, 255, 0)   # Yellow for fully grown
]

def draw_world(display, world, player):
    for y in range(world.height):
        for x in range(world.width):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if world.grid[y][x] == 0:  # Grass
                pygame.draw.rect(display, GRASS_COLOR, rect)
            elif world.grid[y][x] == 1:  # Untilled soil
                pygame.draw.rect(display, SOIL_COLOR, rect)
            elif world.grid[y][x] == 2:  # Tilled soil
                pygame.draw.rect(display, TILLED_SOIL_COLOR, rect)
            elif 3 <= world.grid[y][x] <= 6:  # Growing crops
                pygame.draw.rect(display, TILLED_SOIL_COLOR, rect)
                growth_stage = world.grid[y][x] - 3
                crop_color = CROP_COLORS[growth_stage]
                crop_rect = pygame.Rect(x * TILE_SIZE + TILE_SIZE // 4, 
                                        y * TILE_SIZE + TILE_SIZE // 4 - growth_stage * 2, 
                                        TILE_SIZE // 2, 
                                        TILE_SIZE // 2 + growth_stage * 2)
                pygame.draw.rect(display, crop_color, crop_rect)
                
                if world.grid[y][x] == 6:  # Fully grown crop, add glow
                    glow_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    pygame.draw.rect(glow_surf, (255, 255, 0, 64), glow_surf.get_rect())
                    display.blit(glow_surf, rect)

            pygame.draw.rect(display, (0, 0, 0), rect, 1)  # Grid lines

    # Draw player
    player_rect = pygame.Rect(player.x * TILE_SIZE, player.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(display, PLAYER_COLOR, player_rect)

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