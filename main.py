# File: main.py

import pygame
import sys

# Initialize Pygame
pygame.init()

# Now import our custom modules
from game_objects import Player, World
from ui import draw_world, draw_hud

# Configuration constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TILE_SIZE = 32

# Set up display
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Claude's Farm Simulation")

# Initialize game objects
world = World(WINDOW_WIDTH // TILE_SIZE, WINDOW_HEIGHT // TILE_SIZE)
player = Player(world.width // 2, world.height // 2)

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle player input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.move(0, -1, world)
            elif event.key == pygame.K_s:
                player.move(0, 1, world)
            elif event.key == pygame.K_a:
                player.move(-1, 0, world)
            elif event.key == pygame.K_d:
                player.move(1, 0, world)
            elif event.key == pygame.K_SPACE:
                player.interact(world)

    # Draw everything
    display.fill((0, 0, 0))  # Clear screen
    draw_world(display, world, player)
    draw_hud(display, player)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()