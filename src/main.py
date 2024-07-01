# File: src/main.py

import pygame
import sys
from .game import Game
from .ui import HUD_HEIGHT

# Initialize Pygame
pygame.init()
pygame.display.init()

# Configuration constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600 + HUD_HEIGHT

# Set up display
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Claude's Farm Simulation")

# Initialize game
game = Game(WINDOW_WIDTH, WINDOW_HEIGHT - HUD_HEIGHT)

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        game.handle_input(event)
        
        # Handle shop interactions
        if game.shop_open and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                game.handle_shop_interaction(mouse_pos)

    game.update()

    # Get current mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Draw everything
    display.fill((0, 0, 0))  # Clear screen
    game.draw(display, mouse_pos)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
sys.exit()