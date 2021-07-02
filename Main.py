import pygame as pg
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
sound_dir = path.join(path.dirname(__file__), 'sound')

WIDTH = 800
HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE =(0, 0, 255)

font_name = pg.font.match_font('arial')
def draw_text(sc, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect()
    text_rect.center = (x, y)
    sc.blit(text_surf, text_rect)

# define classes
class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-15, -15)
        self.rect.center = (WIDTH/2, HEIGHT-60)
        self.y_speed = 15

    def update(self):
        pg.mouse.set_visible(False)
        mouse_pos = pg.mouse.get_pos()
        self.rect.x = mouse_pos[0]
        if self.rect.right > WIDTH - 10:
            self.rect.right = WIDTH - 10
        if self.rect.left < 10:
            self.rect.left = 10

class Coins(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(coin_img, (35, 35))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-200, -100)
        self.speed = random.randrange(3, 8)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed = random.randrange(1, 5)

class Gems(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(gem_img, (35, 35))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-200, -100)
        self.speed = 10

    def update(self):
        self.rect.y += self.speed

class Bomb(pg.sprite.Sprite):
    def __init__(self, speed_lim):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(bomb_img, (45, 45))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-200, -100)
        self.speed_lim = speed_lim
        self.speedy = speed_lim
        self.speedx = random.randrange(-5, 5 )

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left < 0:
            self.speedx *= -1
        if self.rect.right > WIDTH:
            self.speedx *= -1
        if self.rect.top > HEIGHT:
            self.kill()

#define gameover screen function
def show_gameover_screen():
    sc.blit(background, background_rect)
    draw_text(sc, "Collecting Coins", 36, WIDTH/2, 100)
    draw_text(sc, "collect as much coins as posible, without getting hit by bombs", 24, WIDTH/2, 300)
    draw_text(sc, "press space to begin", 18, WIDTH/2, 400)
    draw_text(sc, ("score:" + str(score)), 24, WIDTH/2, 20)

    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYUP:
                if event.key== pg.K_SPACE:
                    waiting = False

# initializes pygame
pg.init()
pg.mixer.init()
sc = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Catching Coins")
clock = pg.time.Clock()


# load the sprite graphics
background = pg.image.load(path.join(img_dir, "background.png")).convert()
background_rect = background.get_rect()
player_img = pg.image.load(path.join(img_dir, "player.png")).convert()
bomb_img = pg.image.load(path.join(img_dir, "bomb2.png")).convert()
coin_img = pg.image.load(path.join(img_dir, "hud_coins.png")).convert()
gem_img = pg.image.load(path.join(img_dir, "hud_gem_blue.png")).convert()

# load sound
coin_sound = pg.mixer.Sound(path.join(sound_dir, "coin_pickup.wav"))
explotion_sound = pg.mixer.Sound(path.join(sound_dir, "explosion.wav"))
pg.mixer.music.load(path.join(sound_dir, "backgound_music.mp3"))


pg.mixer.music.play(loops=-1)

game_over = True
running = True
score = 0

while running:
    clock.tick(FPS)
    if game_over:
        show_gameover_screen()
        game_over = False

        # initialize sprite group
        all_sprites = pg.sprite.Group()
        all_coins = pg.sprite.Group()
        all_gems = pg.sprite.Group()
        all_bombs = pg.sprite.Group()

        player = Player()
        all_sprites.add(player)

        for i in range(6):
            coin =  Coins()
            all_sprites.add(coin)
            all_coins.add(coin)

        bomb_probability = 200
        speed_lim = 10
        max_score = 20
        score = 0
    else:
        if score > max_score:
            if bomb_probability > 10:
                bomb_probability -= 10
            speed_lim += 2
            max_score *= 2

        if random.randrange(0, bomb_probability) == 1:
            bom = Bomb(speed_lim)
            all_sprites.add(bom)
            all_bombs.add(bom)

        if random.randrange(0, 200) == 1:
            gem = Gems()
            all_sprites.add(gem)
            all_gems.add(gem)


        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # updates screen
        all_sprites.update()

        # checks for collition
        hits = pg.sprite.spritecollide(player, all_coins, True)
        for hit in hits:
            score += 1
            coin =  Coins()
            all_sprites.add(coin)
            all_coins.add(coin)
            coin_sound.play()

        hits = pg.sprite.spritecollide(player, all_gems, True)
        for hit in hits:
            score += 5
            coin_sound.play()

        hits = pg.sprite.spritecollide(player, all_bombs, False)
        if hits:
            explotion_sound.play()
            game_over = True

        # draws to screen
        sc.fill(BLACK)
        sc.blit(background, background_rect)
        all_sprites.draw(sc)

        draw_text(sc, ("score:" + str(score)), 24, WIDTH/2, 20)

        # flips the screen
        pg.display.flip()

pg.quit()
