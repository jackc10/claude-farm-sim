# File: main.py

import pygame
import sys
from game_objects import Player, World
from ui import draw_world, draw_hud, draw_shop_window, HUD_HEIGHT

# Initialize Pygame
pygame.init()
pygame.display.init()

# Configuration constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600 + HUD_HEIGHT
TILE_SIZE = 32

# Set up display
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Claude's Farm Simulation")

# Initialize game objects
world = World(WINDOW_WIDTH // TILE_SIZE, (WINDOW_HEIGHT - HUD_HEIGHT) // TILE_SIZE)
player = Player(world.width // 2, world.height // 2)

# Main game loop
clock = pygame.time.Clock()
running = True
shop_open = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not shop_open:
            # Handle player input when shop is closed
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
                    result = player.interact(world)
                    if result == "open_shop":
                        shop_open = True
                elif event.key == pygame.K_e:
                    player.switch_tool()
        else:
            # Handle shop interactions when shop is open
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if buy_button.collidepoint(mouse_pos):
                        if world.vendor.sell_seeds(player, "corn_seeds", 1):
                            print("Bought 1 corn seed")
                        else:
                            print("Not enough money or seeds out of stock")
                    elif sell_button.collidepoint(mouse_pos):
                        if world.vendor.buy_crops(player, "corn", 1):
                            print("Sold 1 corn")
                        else:
                            print("No corn to sell")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    shop_open = False

    # Update game state
    world.update_crops()

    # Draw everything
    display.fill((0, 0, 0))  # Clear screen
    draw_world(display, world, player)
    draw_hud(display, player)
    
    if shop_open:
        buy_button, sell_button = draw_shop_window(display, player, world.vendor)

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
sys.exit()