import pygame
import os
pygame.font.init()
pygame.mixer.init()
#GENERAL DEFINATIONS
WIDTH, HEIGHT = 900, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('STAR WAR')
FPS = 120
STEP = 5
BORDER_WIDTH = 10
BORDER = pygame.Rect(WIDTH//2 - BORDER_WIDTH/2 , 0, BORDER_WIDTH, HEIGHT)
BULLET_VEL = 7
MAX_BULLETS = 5 # Max bullets can shoot at a time
LEFT_HIT = pygame.USEREVENT + 1
RIGHT_HIT = pygame.USEREVENT + 2

#COLOR
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#FONT
HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
WINNER_FONT = pygame.font.SysFont('comicsans', 50)

#SOUND EFFECTS
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Hit_Sound.mp3'))
BULLET_SHOOT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Shoot_Sound.mp3'))
#CHARACTERS
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

RIGHT_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'Right_Spaceship.png'))
RIGHT_SPACESHIP = pygame.transform.rotate((pygame.transform.scale(
    RIGHT_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))), 90)

LEFT_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'Left_Spaceship.png'))
LEFT_SPACESHIP = pygame.transform.rotate((pygame.transform.scale(
    LEFT_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))), -90)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = SPACESHIP_HEIGHT, SPACESHIP_WIDTH

SPACE_IMAGE = pygame.image.load(os.path.join('Assets', 'Space.jpg'))
SPACE = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))

BORDER_IMAGE = pygame.image.load(os.path.join('Assets', 'Border.png'))
BORDER_GUI = pygame.transform.scale(BORDER_IMAGE, (BORDER_WIDTH,HEIGHT))
#---------------------------------------

def draw_window(left, right, left_bullets, right_bullets, left_health, right_health):
    SCREEN.blit(SPACE, (0, 0))
    SCREEN.blit(BORDER_GUI, (WIDTH//2 - BORDER_WIDTH/2 , 0))
    left_health_text = HEALTH_FONT.render('Health: ' + str(left_health), 1, WHITE)
    right_health_text = HEALTH_FONT.render('Health: ' + str(right_health), 1, WHITE) 
    #pygame.draw.rect(SCREEN, BLACK, BORDER)
    SCREEN.blit(right_health_text,(WIDTH - right_health_text.get_width() -10, 10))
    SCREEN.blit(left_health_text,(10, 10))

    SCREEN.blit(RIGHT_SPACESHIP, (right.x, right.y))
    SCREEN.blit(LEFT_SPACESHIP, (left.x, left.y))

    for bullet in left_bullets:
        pygame.draw.rect(SCREEN, YELLOW, bullet)

    for bullet in right_bullets:
        pygame.draw.rect(SCREEN, RED, bullet)

    pygame.display.update()

def left_ship_movement_handler(keys_pressed, left):
    if keys_pressed[pygame.K_a] and left.x - STEP > 0:
        left.x -= STEP 
    if keys_pressed[pygame.K_d] and left.x + STEP < BORDER.x - SPACESHIP_WIDTH:
        left.x += STEP 
    if keys_pressed[pygame.K_w] and left.y - STEP > 0:
        left.y -= STEP 
    if keys_pressed[pygame.K_s] and left.y + STEP < HEIGHT - SPACESHIP_HEIGHT:
        left.y += STEP 

def right_ship_movement_handler(keys_pressed, right):
    if keys_pressed[pygame.K_LEFT] and right.x - STEP >BORDER.x + BORDER.width/2:
        right.x -= STEP 
    if keys_pressed[pygame.K_RIGHT] and right.x + STEP < WIDTH - SPACESHIP_WIDTH:
        right.x += STEP 
    if keys_pressed[pygame.K_UP] and right.y - STEP > 0:
        right.y -= STEP 
    if keys_pressed[pygame.K_DOWN] and right.y + STEP < HEIGHT - SPACESHIP_HEIGHT:
        right.y += STEP 

def bullets_handler(left_bullets, right_bullets, left, right):
    for bullet in left_bullets:
         bullet.x += BULLET_VEL
         if right.colliderect(bullet):
             pygame.event.post(pygame.event.Event(RIGHT_HIT))
             left_bullets.remove(bullet)
         elif bullet.x > WIDTH:
             left_bullets.remove(bullet)

    for bullet in right_bullets:
         bullet.x -= BULLET_VEL
         if left.colliderect(bullet):
             pygame.event.post(pygame.event.Event(LEFT_HIT))
             right_bullets.remove(bullet)
         elif bullet.x < 0:
             right_bullets.remove(bullet)
def draw_winner(winner_text):
    draw_text = WINNER_FONT.render(winner_text, 1, WHITE)
    SCREEN.blit(draw_text,(WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(6000)
def main():
    left = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # first appearance
    right = pygame.Rect(700, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # first appearance

    left_bullets = []
    right_bullets = []

    left_health = 10
    right_health = 10

    clock = pygame.time.Clock()
    IS_RUNNING = True
    while IS_RUNNING:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                IS_RUNNING = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(left_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(left.x + left.width, left.y + left.height//2 -2, 10, 5)
                    left_bullets.append(bullet)
                    BULLET_SHOOT_SOUND.play( )
                if event.key == pygame.K_KP_ENTER and len(right_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(right.x, right.y + right.height//2 -2, 10, 5)
                    right_bullets.append(bullet)
                    BULLET_SHOOT_SOUND.play( )
            if event.type == LEFT_HIT:
                left_health -= 1
                BULLET_HIT_SOUND.play( )
            if event.type == RIGHT_HIT:
                right_health -= 1
                BULLET_HIT_SOUND.play( )
        
        winner_text = ''
        if right_health <= 0:
            winner_text = 'P1 win!'

        if left_health <= 0:
            winner_text = 'P2 win!'

        if winner_text != '':
            draw_winner(winner_text)
            break       
        
        keys_pressed = pygame.key.get_pressed()
        left_ship_movement_handler(keys_pressed, left)
        right_ship_movement_handler(keys_pressed, right)
        bullets_handler(left_bullets, right_bullets, left, right)
        draw_window(left, right, left_bullets, right_bullets, left_health, right_health)
    main()

if __name__ == '__main__':
    main()