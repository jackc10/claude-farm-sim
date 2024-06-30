# File: src/config.py

BASE_WIDTH = 800
BASE_HEIGHT = 600
MIN_TILE_SIZE = 16
BASE_TILE_SIZE = 32

def calculate_tile_size(screen_width, screen_height):
    tile_size_w = max(MIN_TILE_SIZE, screen_width // (BASE_WIDTH // BASE_TILE_SIZE))
    tile_size_h = max(MIN_TILE_SIZE, screen_height // (BASE_HEIGHT // BASE_TILE_SIZE))
    return min(tile_size_w, tile_size_h)

def calculate_grid_size(screen_width, screen_height):
    tile_size = calculate_tile_size(screen_width, screen_height)
    return screen_width // tile_size, screen_height // tile_size