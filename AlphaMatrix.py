import pygame
import random

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_w,
    K_a,
    K_d,
    K_s,
    K_LSHIFT,
)

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FONT_SIZE = 50

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # Image
        self.image = pygame.image.load("Average_red_pill_enjoyer.png").convert_alpha()
        self.rect = self.image.get_rect(
            center=(
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2
            )
        )
        # Define the size of the hitbox relative to the image
        hitbox_width = self.rect.width * 0.6
        hitbox_height = self.rect.height
        # Create the hitbox surface
        self.hitbox = pygame.Surface((hitbox_width, hitbox_height))
        self.hitbox.fill((255, 0, 0))
        self.rect_hitbox = self.hitbox.get_rect()
        self.rect_hitbox.center = self.rect.center
        # Cooldown for teleportation ability
        self.teleport_cooldown = 750
        self.last_teleport_time = pygame.time.get_ticks()

    # Basic movement
    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -15)
            self.rect_hitbox.move_ip(0, -15)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 15)
            self.rect_hitbox.move_ip(0, 15)
        if pressed_keys[K_a]:
            self.rect.move_ip(-15, 0)
            self.rect_hitbox.move_ip(-15, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(15, 0)
            self.rect_hitbox.move_ip(15, 0)

        # Teleportation ability 
        teleport_distance = 500  # Distance to teleport
        current_time = pygame.time.get_ticks()
        time_since_last_teleport = current_time - self.last_teleport_time

        if time_since_last_teleport >= self.teleport_cooldown:
            if pressed_keys[K_UP]:
                self.rect.y -= teleport_distance 
                self.rect_hitbox.y -= teleport_distance
            if pressed_keys[K_DOWN]:
                self.rect.y += teleport_distance 
                self.rect_hitbox.y += teleport_distance
            if pressed_keys[K_LEFT]:
                self.rect.x -= teleport_distance 
                self.rect_hitbox.x -= teleport_distance
            if pressed_keys[K_RIGHT]:
                self.rect.x += teleport_distance  
                self.rect_hitbox.x += teleport_distance
            self.last_teleport_time = current_time


        # Window borders for image
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
            self.rect_hitbox.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.rect_hitbox.bottom = SCREEN_HEIGHT
        # Window borders for hitbox
        if self.rect_hitbox.left < 26:
            self.rect_hitbox.left = 26
        if self.rect_hitbox.right > SCREEN_WIDTH - 26:
            self.rect_hitbox.right = SCREEN_WIDTH - 26
    
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
        # Lenght of chain is between 7 and 15 symbols
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
pygame.time.set_timer(ADDSYMBOL, 300)
# Custom event to create a new chain of symbols
CREATECHAIN = pygame.USEREVENT + 2
pygame.time.set_timer(CREATECHAIN, 600)

player = Player()

enemies = pygame.sprite.Group()
symbols = pygame.sprite.Group()
chain = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
#all_sprites.add(player)

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
    screen.blit(player.image, player.rect)
    #screen.blit(player.hitbox, player.rect_hitbox) # <-- Shows hitbox
    
    # Checks if any of the symbols collide with the player's hitbox
    # by using their rectangles
    for entity in symbols:
        if entity.rect.colliderect(player.rect_hitbox):
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
