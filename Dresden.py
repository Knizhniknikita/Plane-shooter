# Импорт библиотек №1 
import pygame
import random
from os import path
from random import randint 
from setings import *

# Инциализация звуков и цветов №2
pygame.init()

s1 = pygame.mixer.Sound("Boom.wav")
s2 = pygame.mixer.Sound("boevoy-vzryiv.mp3")

img_dir = path.join(path.dirname(__file__), 'img')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# настройка папки ассетов №3
game_folder = path.dirname(__file__)
background = pygame.image.load('background.jpg')
background_rect = background.get_rect()
player_img = pygame.image.load('PRISEL.png')
boom_img = pygame.image.load('boom.png')
airplane_img = pygame.image.load('airplane.png')
town_img = pygame.image.load('town.png')
bomb_img = pygame.image.load('bomb.png')



#Создание классов №5
class Player(pygame.sprite.Sprite): #Игрок
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect = self.image.get_rect()
        
    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.center = (mouse_x + 8, mouse_y + 8)
    def shoot(self):
        global score
        s1.play(0)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for mob in mobs.sprites():          # копия списка, чтобы убивать внутри цикла
            if mob.rect.collidepoint(mouse_x + 8, mouse_y + 8):
                score += 50
                expl = Explosion(mob.rect.center, 'lg')
                all_sprites.add(expl)
                mob.kill()
                m = Mob()
                all_sprites.add(m)
                mobs.add(m)
        
class Explosion(pygame.sprite.Sprite): #Взрыв
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.image.set_colorkey(WHITE)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.image.set_colorkey(BLACK)

class Mob(pygame.sprite.Sprite):#Противники(Мобы)
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = airplane_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(100, 400)
        self.rect.x = random.randrange(-200, -100)
        self.speedy = random.randrange(MOB_SPEED_MIN, MOB_SPEED_MAX)
    def update(self):
        a = randint(0, BOMB_DROP_CHANCE)
        if a == 20:
            bullet = bomb(self.rect[0],self.rect[1])
            all_sprites.add(bullet)
            bombs.add(bullet)
        self.rect.x += self.speedy
        if self.rect.x > WIDTH + 10:
            self.rect.y = random.randrange(100, 400)
            self.rect.x = random.randrange(-200, -199)
            self.speedy = random.randrange(MOB_SPEED_MIN, MOB_SPEED_MAX)

            
class Bullet(pygame.sprite.Sprite):  # Снаряд
    def __init__(self, x, y):
        self.speedy = BULLET_SPEED
        pygame.sprite.Sprite.__init__(self)
        self.image = boom_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        
    def update(self):
        global score
        hits = pygame.sprite.groupcollide(mobs, booms, True, True)
        for hit in hits:
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
            expl = Explosion(hit.rect.center, 'lg')
            
            all_sprites.add(expl)
        self.kill()
    
class bomb(pygame.sprite.Sprite):#Бомба
    def __init__(self, x, y):
        self.speedy = BULLET_SPEED
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10
        self.image = bomb_img
        self.image.set_colorkey(WHITE)
    def update(self):
        self.rect.y += self.speedy

class Grass(pygame.sprite.Sprite):#Земля
    def __init__(self):
        self.image = pygame.Surface((WIDTH * 5, 200))
        pygame.sprite.Sprite.__init__(self)
        self.speedx = 0
        self.shield = 100
        self.image = pygame.Surface((4000,200))
        self.image = town_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT - 65)
        self.image.set_colorkey(WHITE)
        
    def update(self):
        global lives
        if pygame.sprite.groupcollide(bombs,grass1, True, False):
            s2.play()
            lives -= 1           
             
#Создание экрана конца игры №6
FONT_PATH = 'font.ttf' 
def draw_text(surf, text, size, x, y):
    # Теперь загружаем шрифт из файла
    font = pygame.font.Font(FONT_PATH, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

font_name = pygame.font.match_font('Copyright')

           
def show_end_screen(message, result, waiting_key='Press KEYDOWN to begin'):
    screen.blit(background, background_rect)
    draw_text(screen, "Dresden 1945", 64, WIDTH / 2, HEIGHT / 5)
    draw_text(screen, "Move mouse cursor, mouse left button to fire", 20, WIDTH / 2, HEIGHT / 1.4)
    draw_text(screen, message, 50, WIDTH / 2, HEIGHT / 3)
    draw_text(screen, result, 50, WIDTH / 2, HEIGHT / 2.2)
    draw_text(screen, waiting_key, 18, WIDTH / 2, HEIGHT * 3 / 3.7)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def reset_game():
    global all_sprites, mobs, booms, bombs, player, grass, grass1
    global score, lives

    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    booms = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    player = Player()
    grass = Grass()
    grass1 = pygame.sprite.Group()
    grass1.add(grass)
    all_sprites.add(grass)
    all_sprites.add(player)
    for i in range(MOB_COUNT):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    score = 0
    lives = LIVES

#Инциализация №7
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Анимация №4
explosion_anim = {}
explosion_anim['lg'] = []
boom_src = pygame.image.load(path.join(img_dir, 'boom.png')).convert()
boom_src.set_colorkey(BLACK)
for size in range(10, 61, 6):        # кадры: 10, 16, 22, ... 58 пикселей
    img = pygame.transform.scale(boom_src, (size, size))
    explosion_anim['lg'].append(img)
pygame.display.set_caption("Dresden 1945")

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
booms = pygame.sprite.Group()
bombs = pygame.sprite.Group()
player = Player()
grass =  Grass()
grass1 = pygame.sprite.Group()
grass1.add(grass)
all_sprites.add(grass)
all_sprites.add(player)
for i in range(MOB_COUNT):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
score = 0
lives = LIVES

#Цикл игры №8
running = True
game_over = False
game_win = False
while running:
    if game_over:
        show_end_screen("Dresden is dead", "YOU LOSE!")
        game_over = False
        reset_game()

    if game_win:
        show_end_screen("Dresden was saved", "YOU WIN!")
        game_win = False
        reset_game()

    pygame.mouse.set_visible(False)
    clock.tick(FPS)
    # Если игрок умер, игра окончена
    if lives <= 0:
        game_over = True
    # Если игрок победил, игра окончена
    if score >= WIN_SCORE:
        game_win = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.shoot()
        
    # Обновление
    all_sprites.update()

    # Рендеринг

    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str("Score: " +str(score)), 30, WIDTH - 75, 10)
    draw_text(screen, str("Lives: "+str(lives)), 30, 75, 10)
    # После отрисовки всего, отчищаем экран
    pygame.display.flip()
    
pygame.quit()
