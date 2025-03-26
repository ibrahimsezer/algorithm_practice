# 30 wood = 50 gold
# 1 axe = 60 wood to be collected
# 1 axe price = 50 gold
# axe health = 120
# 4 hits * 15 wood = 60 wood collected

import pygame
import pygame.key
import random
import constvalue
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((constvalue.PLAYER_SIZE, constvalue.PLAYER_SIZE))
        self.image.fill(constvalue.BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.wood = 0
        self.gold = 50.0
        self.has_axe = False
        self.axe_health = 0
        self.speed = constvalue.PLAYER_SPEED

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        # Keep player in bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, constvalue.WINDOW_WIDTH, constvalue.WINDOW_HEIGHT))

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((constvalue.TREE_SIZE, constvalue.TREE_SIZE))
        self.image.fill(constvalue.GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Market(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((constvalue.MARKET_SIZE, constvalue.MARKET_SIZE))
        self.image.fill(constvalue.GOLD)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game:
    def __init__(self):
        #pygame.init()
        self.screen = pygame.display.set_mode((constvalue.WINDOW_WIDTH, constvalue.WINDOW_HEIGHT))
        pygame.display.set_caption("Wood Collector 2D")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        self.market = pygame.sprite.Group()
        
        # Create player
        self.player = Player(constvalue.WINDOW_WIDTH // 2, constvalue.WINDOW_HEIGHT // 2)
        self.all_sprites.add(self.player)
        
        # Create market
        market = Market(constvalue.WINDOW_WIDTH - 100, 50)
        self.market.add(market)
        self.all_sprites.add(market)
        
        # Create trees
        self.spawn_trees()

    def spawn_trees(self):
        for _ in range(5):
            while True:
                x = random.randint(50, constvalue.WINDOW_WIDTH - 100)
                y = random.randint(50, constvalue.WINDOW_HEIGHT - 100)
                tree = Tree(x, y)
                # Ensure trees don't overlap
                if not pygame.sprite.spritecollide(tree, self.trees, False):
                    self.trees.add(tree)
                    self.all_sprites.add(tree)
                    break

    def handle_market_interaction(self):
        if pygame.sprite.spritecollide(self.player, self.market, False):
            keys = pygame.key.get_pressed()
            if keys[K_b] and self.player.gold >= constvalue.AXE_PRICE:
                self.player.has_axe = True
                self.player.axe_health = constvalue.MAX_AXE_HEALTH
                self.player.gold -= constvalue.AXE_PRICE
            elif keys[K_RIGHT] and self.player.wood > 0:
                gold_earned = self.player.wood * constvalue.WOOD_PRICE_PER_UNIT
                self.player.gold += gold_earned
                self.player.wood = 0

    def handle_tree_interaction(self):
        if self.player.has_axe and self.player.axe_health > 0:
            tree_hits = pygame.sprite.spritecollide(self.player, self.trees, False)
            if tree_hits and pygame.key.get_pressed()[K_SPACE]:
                self.player.wood += constvalue.WOOD_COLLECT_PER_HIT
                self.player.axe_health -= 30
                if self.player.axe_health <= 0:
                    self.player.has_axe = False

    def draw_status(self):
        status_text = f"Gold: {self.player.gold:.1f} Wood: {self.player.wood}"
        axe_text = f"Axe: {'Yes' if self.player.has_axe else 'No'} Health: {max(0, self.player.axe_health)}"
        text_surface = self.font.render(status_text, True, constvalue.BLACK)
        axe_surface = self.font.render(axe_text, True, constvalue.BLACK)
        self.screen.blit(text_surface, (10, 10))
        self.screen.blit(axe_surface, (10, 40))

    def run(self):
        running = True
        while running:
            # Event handling
            dx = dy = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b and pygame.sprite.spritecollide(self.player, self.market, False):
                        if self.player.gold >= constvalue.AXE_PRICE:
                            self.player.has_axe = True
                            self.player.axe_health = constvalue.MAX_AXE_HEALTH
                            self.player.gold -= constvalue.AXE_PRICE
                    elif event.key == pygame.K_s and pygame.sprite.spritecollide(self.player, self.market, False):
                        if self.player.wood > 0:
                            gold_earned = self.player.wood * constvalue.WOOD_PRICE_PER_UNIT
                            self.player.gold += gold_earned
                            self.player.wood = 0
                    elif event.key == pygame.K_SPACE:
                        if self.player.has_axe and self.player.axe_health > 0:
                            tree_hits = pygame.sprite.spritecollide(self.player, self.trees, False)
                            if tree_hits:
                                self.player.wood += constvalue.WOOD_COLLECT_PER_HIT
                                self.player.axe_health -= 30
                                if self.player.axe_health <= 0:
                                    self.player.has_axe = False

            # Continuous movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: dx -= 1
            if keys[pygame.K_RIGHT]: dx += 1
            if keys[pygame.K_UP]: dy -= 1
            if keys[pygame.K_DOWN]: dy += 1
            self.player.move(dx, dy)

            # Drawing
            self.screen.fill(constvalue.WHITE)
            self.all_sprites.draw(self.screen)
            self.draw_status()
            
            pygame.display.flip()
            self.clock.tick(constvalue.FPS)

        pygame.quit()

def game_start():
    game = Game()
    game.run()

