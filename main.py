import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))

background = pygame.image.load("G:\CS\gameoffire\background.png")
pygame.display.set_caption("Game of Fire")
icon = pygame.image.load("G:\CS\gameoffire\fire.png")
pygame.display.set_icon(icon)

mixer.music.load("G:\CS\gameoffire\backgroundgof.mp3")
mixer.music.play(-1)

dragonimg = pygame.image.load("G:\CS\gameoffire\dragon.png")
dragonx = 360
dragony = 510
dragonx_change = 0

fireimg = pygame.image.load('G:\CS\gameoffire\fire.png')
firex = 0
firey = 510
firex_change = 0
firey_change = 5
attack_state = "ready"

enemyimg = []
enemyx = []
enemyy =[]
enemyx_change = []
enemyy_change = []
no_of_enemies = 6
for i in range(no_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(2)
    enemyy_change.append(30)

score_value = 0
font = pygame.font.Font('starjedi.ttf', 32)
textx = 10
texty = 10

over_font = pygame.font.Font('starjedi.ttf', 64)

def gameover():
    gameover_text = over_font.render("ok", True, (240, 128, 128))
    screen.blit(gameover_text,(200,250))




def show_score(x, y):
    score = font.render("killed: " + str(score_value), True, (240, 128, 128))
    screen.blit(score, (x, y))


def dragon(x, y):
    screen.blit(dragonimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def attack(x, y):
    global attack_state
    attack_state = "fire"
    screen.blit(fireimg, (x + 16, y + 10))


def iscollision(enemyx, enemyy, firex, firey):
    distance = math.sqrt((math.pow((enemyx - firex), 2)) + math.pow((enemyy - firey), 2))
    if distance < 27:
        return True
    else:
        return False


# game loop
run = True
while run:
    # adding background color
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # moving boy along x axis
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dragonx_change = -2
            if event.key == pygame.K_RIGHT:
                dragonx_change = 2
            if event.key == pygame.K_SPACE:
                    if attack_state is "ready":
                        firex = dragonx
                        attack(firex, firey)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                dragonx_change = 0

    dragonx += dragonx_change
    if dragonx <= 0:
        dragonx = 0
    elif dragonx >= 736:
        dragonx = 736

    for i in range(no_of_enemies):
        if enemyy[i] > 600:
            for j in range(no_of_enemies):
                enemyy[j] = 2000
            gameover()
            break

        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] += 2
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] += -2
            enemyy[i] += enemyy_change[i]

        collision = iscollision(enemyx[i], enemyy[i], firex, firey)
        if collision:
            firey = 510
            attack_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)
        enemy(enemyx[i], enemyy[i], i)


    if firey <= 0:
        firey = 510
        attack_state = "ready"

    if attack_state is "fire":
        attack(firex, firey)
        firey -= firey_change

    dragon(dragonx, dragony)
    show_score(textx, texty)
    pygame.display.update()
