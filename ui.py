# File: ui.py

import pygame

TILE_SIZE = 32
GRASS_COLOR = (0, 255, 0)
SOIL_COLOR = (139, 69, 19)
TILLED_SOIL_COLOR = (101, 67, 33)
PLAYER_COLOR = (255, 0, 0)

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
            pygame.draw.rect(display, (0, 0, 0), rect, 1)  # Grid lines

    # Draw player
    player_rect = pygame.Rect(player.x * TILE_SIZE, player.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(display, PLAYER_COLOR, player_rect)

def draw_hud(display, player):
    font = pygame.font.Font(None, 36)
    position_text = font.render(f"Position: ({player.x}, {player.y})", True, (255, 255, 255))
    tool_text = font.render(f"Tool: {player.current_tool}", True, (255, 255, 255))
    display.blit(position_text, (10, 10))
    display.blit(tool_text, (10, 50))