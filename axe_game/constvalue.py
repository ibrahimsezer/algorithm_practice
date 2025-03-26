import pygame

# Game window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
GOLD = (255, 215, 0)

# Player settings
PLAYER_SPEED = 5
PLAYER_SIZE = 40

# Game object sizes
TREE_SIZE = 50
MARKET_SIZE = 80

# Initial inventory values
WOOD_PRICE_PER_UNIT = 1.67
AXE_PRICE = 50
MAX_AXE_HEALTH = 120
WOOD_COLLECT_PER_HIT = 15
require_axe = "You need an axe to collect wood. Buy an axe!"

# Asset paths
PLAYER_IMG = "assets/player.png"
TREE_IMG = "assets/tree.png"
MARKET_IMG = "assets/market.png"