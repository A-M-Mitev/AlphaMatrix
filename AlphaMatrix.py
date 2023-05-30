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
#from pygame.sprite import _Group

# Screen size
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((0, 255, 65))
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
        if pressed_keys[K_DOWN]:
          self.rect.move_ip(0, 10)
        if pressed_keys[K_LEFT]:
          self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
           self.rect.move_ip(10, 0)
        if pressed_keys[K_e]:
            symbol = random.randint(33, 126)
            print(chr(symbol))
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

class Symbol(pygame.sprite.Sprite):
    def __init__(self):
        super(Symbol, self).__init__()
        # Random symbol from the ASCII table (33->'!'; 126->'`')
        symbol = chr(random.randint(33, 126))
        self.surf = font.render(symbol, True, (0, 255, 65))
        self.rect = self.surf.get_rect()
        self.rect.center=(
            random.randint(0, SCREEN_WIDTH),
            SCREEN_HEIGHT - (random.randint(100,1000))
        )

pygame.init()

#Text
FONT_SIZE = 40
font = pygame.font.Font(None, FONT_SIZE)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Custom event to create a new symbol
ADDSYMBOL = pygame.USEREVENT + 2
pygame.time.set_timer(ADDSYMBOL, 250)

player = Player()

enemies = pygame.sprite.Group()
symbols = pygame.sprite.Group()
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
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDSYMBOL:
            new_symbol = Symbol()
            symbols.add(new_symbol)
            all_sprites.add(new_symbol)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    
    screen.fill((13, 2, 8))
    #screen.blit(single_symbol, single_symbolRect)
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
