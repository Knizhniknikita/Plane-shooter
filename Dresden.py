# Импорт библиотек №1 
import pygame
import random
from os import path
from random import randint 

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

#Анимация №4
explosion_anim = {}
explosion_anim['lg'] = []
for i in range(9):
    filename = 'boom.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename))
    img.set_colorkey(BLACK)

    img_lg = pygame.transform.scale(img, (20, 20))
    explosion_anim['lg'].append(img_lg)
 
WIDTH = 800
HEIGHT = 650
FPS = 30

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
        if event.type == pygame.MOUSEMOTION:
            cursor_pos = event.pos
            c = []
            centerx = event.pos[0] - 12
            b = event.pos[1] - 12
            c.append(centerx)
            c.append(b)
            self.rect = c
    def shoot(self):
        s1.play(0)
        bullet = Bullet(self.rect[0],self.rect[1])
        all_sprites.add(bullet)
        booms.add(bullet)
        
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
            self.image.set_colorkey(WHITE)
        else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Mob(pygame.sprite.Sprite):#Противники(Мобы)
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(0,300)
        self.rect.x = random.randrange(-200, -199)
        self.speedy = random.randrange(3, 8)
        self.image = airplane_img
        self.image.set_colorkey(BLACK)
    def update(self):
        a = randint(0,300)
        if a == 20:
            bullet = bomb(self.rect[0],self.rect[1])
            all_sprites.add(bullet)
            bombs.add(bullet)
        self.rect.x += self.speedy
        if self.rect.x > WIDTH + 10:
            self.rect.y = random.randrange(0,300)
            self.rect.x = random.randrange(-200, -199)
            self.speedy = random.randrange(3, 8)

            
class Bullet(pygame.sprite.Sprite):#Снаряд
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        centerx = event.pos[0] +8
        b = event.pos[1] +8
        self.rect.bottom = b
        self.rect.centerx = centerx
        self.speedy = -10
        self.image = boom_img
        self.image.set_colorkey(BLACK)
        
    def update(self):
        global score
        hits = pygame.sprite.groupcollide(mobs, booms, True, True)
        for hit in hits:
            score += 50
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
            expl = Explosion(hit.rect.center, 'lg')
            
            all_sprites.add(expl)
        self.kill()
    
class bomb(pygame.sprite.Sprite):#Бомба
    def __init__(self, x, y):
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
        pygame.sprite.Sprite.__init__(self)
        self.speedx = 0
        self.shield = 100
        self.image = pygame.Surface((4000,200))
        self.image = town_img
        self.rect = self.image.get_rect()
        self.rect.center = (400,595)
        self.image.set_colorkey(WHITE)
        
    def update(self):
        global lives
        if pygame.sprite.groupcollide(bombs,grass1, True, False):
            s2.play()
            lives -= 1           
             
#Создание экрана конца игры №6
font_name = pygame.font.match_font('Copyright')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

font_name = pygame.font.match_font('Copyright')
def draw_text1(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
           
def show_go_screen():#Победа
    screen.blit(background, background_rect)
    draw_text(screen, "Dresden 1945", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Move mouse cursor, mouse left button to fire ", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Dresden is die", 70,
              WIDTH / 2, HEIGHT / 3)
    draw_text(screen, "YOU LOSE!", 70,
              WIDTH / 2, HEIGHT / 2.4)
    draw_text(screen, "Press KEYDOWN to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def show_go_screen1():#Поражение
    screen.blit(background, background_rect)
    draw_text(screen, "Dresden 1945", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Move mouse cursor, mouse left button to fire ", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Dresden was saved", 70,
              WIDTH / 2, HEIGHT / 3)
    draw_text(screen, "YOU WIN!", 70,
              WIDTH / 2, HEIGHT / 2.4)
    draw_text(screen, "Press KEYDOWN to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False   

#Инциализация №7
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
score = 0
lives = 20

#Цикл игры №8
running = True
game_over = False
game_win = False
while running:
    if game_over:
        show_go_screen()
        game_over = False
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
        for i in range(8):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        score = 0
        lives = 20
        
    if game_win:
        show_go_screen1()
        game_over = False
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
        for i in range(8):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        score = 0
        lives = 20

    pygame.mouse.set_visible(False)
    clock.tick(FPS)
    # Если игрок умер, игра окончена
    if lives <= 0:
        game_over = True
    # Если игрок победил, игра окончена
    if score >= 5000:
        game_win = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.shoot()
        
    # Обновление
    all_sprites.update()
    hits = pygame.sprite.groupcollide(mobs, booms, True, True)
    for hit in hits:
        score += 50
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
    # Рендеринг

    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 30, WIDTH / 2, 10)
    draw_text1(screen, str(lives), 30, 15, 10)
    # После отрисовки всего, отчищаем экран
    pygame.display.flip()
    
pygame.quit()
