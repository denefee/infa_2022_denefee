import pygame
import math
import numpy as np
from pygame.draw import *
from random import randint
pygame.init()


dt = 0.1
N = 0
FPS = 100
height = 700
width = 1200
screen = pygame.display.set_mode((width, height))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

number_of_balls = 3
#         x  y  vx vy r
balls = [[0, 0, 0, 0, 0, COLORS[0]] for i in range(number_of_balls)]
#          x  y  vx A  B  d
squares = [0, 0, 0, 0, 0, 0]


def new_square(square):
    square[3] = 300
    square[4] = 300
    x0 = randint(100, 700)
    y0 = randint(100, 500)
    vx = randint(10, 70)
    d = 100
    rect(screen, BLUE, pygame.Rect(x0, y0, d/2, d/2), 5)
    square[0] = x0
    square[1] = y0
    square[2] = vx
    square[5] = d


def new_ball(ball):
    ball[0] = randint(100, 700)
    ball[1] = randint(100, 500)
    ball[2] = randint(-70, 70)
    ball[3] = randint(-50, 50)
    ball[4] = randint(30, 40)
    ball[5] = COLORS[randint(0, 5)]
    circle(screen, ball[5], (ball[0], ball[1]), ball[4])


def move_ball(ball):
    global dt, width, height

    if (ball[4] >= ball[0]) or (ball[0] >= width - ball[4]):
        ball[2] = -ball[2] + randint(-10, 10)
        ball[3] = randint(-70, 70)

    ball[0] += ball[2]*dt

    if (ball[4] >= ball[1]) or (ball[1] >= height - ball[4]):
        ball[3] = -ball[3]
        ball[2] = randint(-50, 50)
    ball[1] += ball[3]*dt

    draw_ball(ball)


def draw_ball(ball):
    circle(screen, ball[5], (ball[0], ball[1]), ball[4])


def draw_square(square):
    x0 = square[0]
    y0 = square[1]
    d = square[5]
    rect(screen, BLUE, pygame.Rect(x0, y0, d/2, d/2), 5)


def move_square(square):
    global dt

    if (square[0] <= 0) or (square[0] >= width - square[5]/2):
        square[2] = -square[2]

    square[0] += square[2]*dt
    square[1] = square[3]*np.sin(square[0]/70) + square[4]
    draw_square(square)


def click(click_event):
    global finished, N, balls, squares
    x0, y0 = click_event.pos
    for ball in balls:
        if ((ball[0]-x0)**2+(ball[1]-y0)**2) <= ball[4]**2:
            N = N + 1
            print('SCORE', N)
    if ((squares[0] - x0) ** 2 + (squares[1] - y0) ** 2) <= squares[5] ** 2:
        N = N + 3
        print('SCORE', N)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

font = pygame.font.Font(None, 72)

for i in range(number_of_balls):
    new_ball(balls[i])

new_square(squares)

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
    for i in range(number_of_balls):
        move_ball(balls[i])

    move_square(squares)
    text = font.render(str(N), True, (0, 100, 0))
    place = text.get_rect(center=(30, 30))
    screen.blit(text, place)

    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
