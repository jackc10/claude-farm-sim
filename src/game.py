# File: src/game.py

import pygame
from entities import Player
from world import World
from ui import draw_world, draw_hud, draw_shop_window

class Game:
    def __init__(self, width, height):
        self.world = World(width, height)
        self.player = Player(self.world.width // 2, self.world.height // 2)
        self.shop_open = False
        self.shop_buttons = None

    def update(self):
        self.world.update_crops()

    def draw(self, display):
        draw_world(display, self.world, self.player)
        draw_hud(display, self.player)
        if self.shop_open:
            self.shop_buttons = draw_shop_window(display, self.player, self.world.vendor)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.player.move(0, -1, self.world)
            elif event.key == pygame.K_s:
                self.player.move(0, 1, self.world)
            elif event.key == pygame.K_a:
                self.player.move(-1, 0, self.world)
            elif event.key == pygame.K_d:
                self.player.move(1, 0, self.world)
            elif event.key == pygame.K_SPACE:
                result = self.player.interact(self.world)
                if result == "open_shop":
                    self.shop_open = True
            elif event.key == pygame.K_e:
                self.player.switch_tool()
            elif event.key == pygame.K_ESCAPE and self.shop_open:
                self.shop_open = False

    def handle_shop_interaction(self, mouse_pos):
        if self.shop_buttons:
            buy_button, sell_button = self.shop_buttons
            if buy_button.collidepoint(mouse_pos):
                if self.world.vendor.sell_seeds(self.player, "corn_seeds", 1):
                    print("Bought 1 corn seed")
                else:
                    print("Not enough money or seeds out of stock")
            elif sell_button.collidepoint(mouse_pos):
                if self.world.vendor.buy_crops(self.player, "corn", 1):
                    print("Sold 1 corn")
                else:
                    print("No corn to sell")