import pygame
import random


# Initializing pygame
pygame.init()

# Creating screen
screen = pygame.display.set_mode((800, 600))

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.png')

# Background Music
pygame.mixer.music.load('background_music.wav')
pygame.mixer.music.play(-1)

# Score
score_value = 0
score_font = pygame.font.Font("Mango_Drink.ttf", 32)

textX = 10
textY = 10

# Game Over Text
game_over_font = pygame.font.Font("Black_Metal.otf", 64)
is_game_over = False

# Restart Game Text
restart_game_font = pygame.font.Font("Mango_Drink.ttf", 32)
restart = False

# Player
playerImg = pygame.image.load('player.png')
playerX = 368
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 15

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# Bullet
# ready - You can't see the bullet on the screen
# fire - The bullet is currently moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
# bulletX_change = 0
bulletY_change = 15
bullet_state = 'ready'


def show_score(x, y):
    score = score_font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    global is_game_over
    game_over = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (200, 200))
    is_game_over = True


def restart_game_text():
    restart_game = restart_game_font.render("Press 'R' to Play Again", True, (255, 255, 255))
    screen.blit(restart_game, (310, 300))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def isColliding(enemyX, enemyY, bulletX, bulletY):
    distance = ((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2) ** (0.5)
    return distance < 27


# Game Loop
running = True

while running:
    # Background Color (RGB) # Min value = 0 and Max value = 255
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    # # Threshold Line
    # pygame.draw.line(screen, (50, 50, 100), (0, 470), (800, 470))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If a key is pressed check whether it is right or left or up or r
        if event.type == pygame.KEYDOWN:
            if is_game_over:
                if event.key == pygame.K_r:
                    is_game_over = False
                    restart = True
                    break

            if event.key == pygame.K_LEFT:
                if score_value < 50:
                    playerX_change = -6
                elif score_value < 100:
                    playerX_change = -6.5
                elif score_value < 200:
                    playerX_change = -7
                elif score_value < 350:
                    playerX_change = -7.5
                elif score_value < 500:
                    playerX_change = -8
                else:
                    playerX_change = -8.5

            if event.key == pygame.K_RIGHT:
                if score_value < 50:
                    playerX_change = 6
                elif score_value < 100:
                    playerX_change = 6.5
                elif score_value < 200:
                    playerX_change = 7
                elif score_value < 350:
                    playerX_change = 7.5
                elif score_value < 500:
                    playerX_change = 8
                else:
                    playerX_change = 8.5

            if event.key == pygame.K_UP:
                if bullet_state is 'ready':
                    bullet_sound = pygame.mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Restart Game
    if restart:
        restart = False
        score_value = 0
        textX = 10
        textY = 10
        playerX = 368
        playerY = 480
        playerX_change = 0
        enemyX = []
        enemyY = []
        num_of_enemies = 15

        for i in range(num_of_enemies):
            enemyX.append(random.randint(0, 735))
            enemyY.append(random.randint(50, 150))

        bulletX = 0
        bulletY = 480
        bulletY_change = 15

    # Speed of Bullet
    if score_value < 50:
        bulletY_change = 15
    elif score_value < 100:
        bulletY_change = 16
    elif score_value < 200:
        bulletY_change = 17
    elif score_value < 350:
        bulletY_change = 18
    elif score_value < 500:
        bulletY_change = 19
    else:
        bulletY_change = 20

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 416:
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            game_over_text()
            restart_game_text()
            break

        # Enemy Movement
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            if score_value < 50:
                enemyX_change[i] = 4
            elif score_value < 100:
                enemyX_change[i] = 4.5
            elif score_value < 200:
                enemyX_change[i] = 5
            elif score_value < 350:
                enemyX_change[i] = 5.5
            elif score_value < 500:
                enemyX_change[i] = 6
            else:
                enemyX_change[i] = 6.5

            enemyY[i] += enemyY_change[i]

        if enemyX[i] >= 736:
            if score_value < 50:
                enemyX_change[i] = -4
            elif score_value < 100:
                enemyX_change[i] = -4.5
            elif score_value < 200:
                enemyX_change[i] = -5
            elif score_value < 350:
                enemyX_change[i] = -5.5
            elif score_value < 500:
                enemyX_change[i] = -6
            else:
                enemyX_change[i] = -6.5

            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isColliding(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = pygame.mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 5
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()