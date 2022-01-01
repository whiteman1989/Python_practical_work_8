import pygame
from pygame import image
from pygame.display import update
from pygame.examples.freetype_misc import run
from Projectile import Projectile
from Side import Side
from Enemy import Enemy
from Bird import Bird

pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("practical work 8")

score = 0

walk_right = [pygame.image.load('sprites/R1E.png'),
pygame.image.load('sprites/R2E.png'),
pygame.image.load('sprites/R3E.png'),
pygame.image.load('sprites/R4E.png'),
pygame.image.load('sprites/R5E.png'),
pygame.image.load('sprites/R6E.png')]

walk_left = [pygame.image.load('sprites/L1E.png'),
pygame.image.load('sprites/L2E.png'),
pygame.image.load('sprites/L3E.png'),
pygame.image.load('sprites/L4E.png'),
pygame.image.load('sprites/L5E.png'),
pygame.image.load('sprites/L6E.png')]

bg = pygame.image.load('sprites/NBG.png')
player_stand = pygame.image.load('sprites/R7E.png')

font = pygame.font.SysFont('Comicsans', 20, True, True)

shoot_sound = pygame.mixer.Sound('sounds/bullet.wav')
hit_sound = pygame.mixer.Sound('sounds/hit.wav')

music = pygame.mixer.music.load('sounds/music.mp3')
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

x = 50
y = 525
width = 60
height = 71
speed = 5

is_jump = False
jump_count = 10

left = False
right = False
anim_count = 0
hitbox = (x+20, y, 28, 60)
last_direction = Side.RIGHT

shoot_loop = 0

goblin = Enemy(5, 436, 64, 64, 495)
bird = Bird(10, 100, 400)

def draw_window():
    global anim_count
    win.blit(bg, (0,0))
    if anim_count +1 >= 30:
        anim_count = 0
    
    if left:
        win.blit(walk_left[anim_count // 5], (x,y))
        anim_count += 1
    elif right:
        win.blit(walk_right[anim_count // 5], (x, y))
        anim_count += 1
    else:
        win.blit(player_stand, (x,y))
    for projectile in projectiles:
        projectile.draw(win)
    goblin.draw(win)
    bird.draw(win)
    #hitbox = (x+10, y, 28, 60)
    #pygame.draw.rect(win, (255, 0, 0), hitbox, 2)
    draw_score(score)

    pygame.display.update()

def draw_score(score: int) -> None:
    text = font.render("Рахунок: "+str(score), 1, (255,255,255))
    win.blit(text, (350, 10))

run = True

projectiles = []

def hit():
    global anim_count
    anim_count = 0
    font1 = pygame.font.SysFont('Comicsans', 100)
    text1 = font1.render('-5', 1, (255, 0, 0))
    win.blit(text1, (250 - (text1.get_width()/2), 200))
    pygame.display.update()
    i = 0
    while i < 300:
        pygame.time.delay(10)
        i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                i = 301
                pygame.quit

while run:
    clock.tick(30)
    hitbox = (x+10, y, 28, 60)
    if hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and hitbox[1] + hitbox[1] > goblin.hitbox[1]:
        if hitbox[0] + hitbox[2] > goblin.hitbox[0] and hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
            hit()
            x = 50
            y = 425
            score -= 5
    if shoot_loop > 0:
        shoot_loop += 1
    if shoot_loop > 3:
        shoot_loop = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for projectile in projectiles:
        if projectile.y - projectile.radius < goblin.hitbox[1] + goblin.hitbox[3] and projectile.y + projectile.radius > goblin.hitbox[1]:
            if projectile.x + projectile.radius > goblin.hitbox[0] and projectile.x - projectile.radius < goblin.hitbox[1] + goblin.hitbox[3]:
                goblin.hit()
                projectiles.pop(projectiles.index(projectile))
                score += 1
                hit_sound.play()
        if projectile.x < 500 and projectile.x > 0:
            projectile.x += projectile.vel
        else:
            projectiles.pop(projectiles.index(projectile))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_f] and shoot_loop == 0:
        shoot_sound.play()
        if last_direction == Side.RIGHT:
            facing = 1
        else:
            facing = -1
        if len(projectiles) < 5:
            projectiles.append(Projectile(round(x + width // 2), round(y + height // 2), 3, (255, 0, 0), facing))
        shoot_loop = 1
    if keys[pygame.K_LEFT] and x > 5:
        x-= speed
        left = True
        right =False
        last_direction = Side.LEFT
    elif keys[pygame.K_RIGHT] and x < 500 - width - 5:
        x+= speed
        left = False
        right = True
        last_direction = Side.RIGHT
    else:
        left = False
        right =False
        anim_count = 0
    if not (is_jump):
        if keys[pygame.K_UP] and y > 5:
            y -= speed
        if keys[pygame.K_DOWN] and y < 500 - height -5:
            y += speed
        if keys[pygame.K_SPACE]:
            is_jump = True

    else:
        if jump_count >= -10:
            if jump_count < 0:
                y += (jump_count**2)/2
            else:
                y -= (jump_count**2)/2
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 10

    draw_window()
pygame.quit()