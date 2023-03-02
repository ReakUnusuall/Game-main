import pygame
from random import randrange as rnd

WIDTH, HEIGHT = 1400, 800
fps = 74

paddle_w = 250
paddle_h = 30
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

ball_radius = 19
ball_speed = 5
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

block_list = [pygame.Rect(10 + 140 * i, 10 + 80 * j, 125, 68) for i in range(10) for j in range(4)]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
img = pygame.image.load('1.jpg').convert()

def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    screen.blit(img, (0, 0))

    [pygame.draw.rect(screen, pygame.Color('brown'), block) for color, block in enumerate(block_list)]
    pygame.draw.circle(screen, pygame.Color('darkgray'), ball.center, ball_radius)
    pygame.draw.rect(screen, pygame.Color('darkorange'), paddle)

    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
    
    if ball.centery < ball_radius:
        dy = -dy
    
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)

    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
    
    if ball.bottom > HEIGHT:
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((1280, 720))
        img = pygame.image.load('21.jpg').convert()
        screen.blit(img, (0, 0))
    elif not len(block_list):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((1280, 1024))
        img = pygame.image.load('31.jpg').convert()
        screen.blit(img, (0, 0))

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed
    
    pygame.display.flip()
    clock.tick(fps)