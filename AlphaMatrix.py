import pygame
import random

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_e,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FONT_SIZE = 50

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.hitbox = pygame.Surface((75, 25))
        self.hitbox.fill((0,0,0))
        self.rect_hitbox = self.hitbox.get_rect(
            center=(
            SCREEN_HEIGHT/2, 
            SCREEN_WIDTH/2
            )
        )
        self.surf = pygame.image.load("Average_red_pill_enjoyer.png").convert_alpha()
        self.rect = self.surf.get_rect(
            center=(
            SCREEN_HEIGHT/2, 
            SCREEN_WIDTH/2
            )
        )
    # Movement
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -10)
            self.rect_hitbox.move_ip(0, -10)
        if pressed_keys[K_DOWN]:
          self.rect.move_ip(0, 10)
          self.rect_hitbox.move_ip(0, 10)
        if pressed_keys[K_LEFT]:
          self.rect.move_ip(-10, 0)
          self.rect_hitbox.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
           self.rect.move_ip(10, 0)
           self.rect_hitbox.move_ip(10, 0)
    
        # Window borders
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface(( 20, 10))
        self.surf.fill((69, 255, 255))
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                0
            )
        )
        self.speed = random.randint(5, 20)

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.right < 0:
            self.kill()

# Places a random symbol on given cordinates
class Symbol(pygame.sprite.Sprite):
    def __init__(self, x_cord, y_cord, age):
        super(Symbol, self).__init__()
        self.age_of_chain = age
        self.age = age
        self.x_cord = x_cord
        self.y_cord = y_cord 
        # Random symbol from the ASCII table (33->'!'; 126->'`')
        self.symbol = chr(random.randint(33, 126))
        self.surf = font.render(self.symbol, True, (0, 255, 65))
        self.rect = self.surf.get_rect()
        self.rect.center=(
            x_cord,
            y_cord
        )

    def update(self):
        if self.age == 0:
            self.kill()
        # Delete after reaching bottom
        if self.rect.bottom >= (SCREEN_HEIGHT):
            self.kill()
        # Changing colour
        if self.age == self.age_of_chain - 2:
            self.surf = font.render(self.symbol, True, (0, 143, 17))
        if self.age == 3 or self.age == 4:
            self.surf = font.render(self.symbol, True, (0, 59, 0))
        if self.age == 2 or self.age == 1:
            self.surf = font.render(self.symbol, True, (13, 20, 8))

# Starts a chain of symbols from the top
class Chain(pygame.sprite.Sprite):

    def __init__(self):
        super(Chain, self).__init__()
        self.age_of_chain = random.randint(7, 15)
        self.age = self.age_of_chain
        self.x_cord = random.randint(0, SCREEN_WIDTH)
        self.y_cord = 15
        # Random symbol from the ASCII table (33->'!'; 126->'`')
        self.symbol = chr(random.randint(33, 126))
        self.surf = font.render(self.symbol, True, (0, 255, 65))
        self.rect = self.surf.get_rect()
        self.rect.center=(
            self.x_cord,
            self.y_cord
        )

    def update(self):
        if self.age == 0:
            self.kill()
        # Delete after reaching bottom
        if self.rect.bottom >= (SCREEN_HEIGHT):
            self.kill()
        # Changing colour
        if self.age == self.age_of_chain - 2:
            self.surf = font.render(self.symbol, True, (0, 143, 17))
        if self.age == self.age_of_chain - 3:
            self.surf = font.render(self.symbol, True, (0, 59, 0))
        if self.age == 2 or self.age == 1:
            self.surf = font.render(self.symbol, True, (13, 20, 8))

pygame.init()

font = pygame.font.Font(None, FONT_SIZE)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Custom event to create a new symbol
ADDSYMBOL = pygame.USEREVENT + 1
pygame.time.set_timer(ADDSYMBOL, 150)
# Custom event to create a new chain of symbols
CREATECHAIN = pygame.USEREVENT + 2
pygame.time.set_timer(CREATECHAIN, 300)

player = Player()

enemies = pygame.sprite.Group()
symbols = pygame.sprite.Group()
chain = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# The loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        elif event.type == ADDSYMBOL:
            # Adds another symbol to every chain and makes it the new end of chain, 
            # whilst removing the previous one from the group
            for entity in chain:
                new_symbol = Symbol(entity.x_cord, entity.y_cord + (FONT_SIZE - 15), entity.age_of_chain)
                symbols.add(new_symbol)
                chain.add(new_symbol)
                all_sprites.add(new_symbol)
                chain.remove(entity)
            # Makes every existing symbol older(if age == 0) they disappear
            for entity in symbols:
                entity.age -= 1

        # Starts a new chain of symbols        
        elif event.type == CREATECHAIN:
            new_chain = Chain()
            chain.add(new_chain)
            symbols.add(new_chain)
            all_sprites.add(new_chain)
            
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    symbols.update()
    
    screen.fill((0, 0, 0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    screen.blit(player.hitbox, player.rect_hitbox)
    
    # Game ends when you touch a symbol
    if pygame.sprite.spritecollideany(player, symbols):
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
