import math
from random import choice
from random import randint as rnd
import pygame


FPS = 30
g = 2.5
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.r > self.x or self.x > WIDTH - self.r:
            self.vx = -self.vx

        if self.y > HEIGHT:
            self.vy = -self.vy
        self.vy -= g

        self.vx *= 0.97
        self.vy *= 0.97

        if self.y > HEIGHT - self.r:
            self.y = HEIGHT - self.r
            if self.vy < 0:
                self.vy = -self.vy - 2*g

        
        self.x += self.vx
        self.y -= self.vy

        if (self.vx <= 0.01):
            self.live -= 1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):

        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            return True

        return False
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """

class Gun:
    def __init__(self, screen):
        self.width = 10
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.f2_power*10*math.cos (self.an), HEIGHT - self.f2_power*10*math.sin (self.an))
        new_ball.r += 5
        an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power*2 * math.cos(an)
        new_ball.vy = - self.f2_power*2 * math.sin(an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((HEIGHT - event.pos[1]) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        x0 = 20
        y0 = HEIGHT - 20
        x1 = self.f2_power*10*math.cos (self.an)
        y1 = HEIGHT - self.f2_power*10*math.sin (self.an)
        pygame.draw.polygon (self.screen, self.color,  [[x0, y0], [x1 + self.width*math.sin(self.an), y1 + self.width*math.cos(self.an)], 
                                                        [x1, y1], [x0 - self.width*math.sin(self.an), y0 - self.width*math.cos(self.an)]])

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 30:
                self.f2_power += 0.5
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self):
        global targets
        targets.append (self)
        self.live = 1
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.balls_count = 1
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        vy = self.vy = rnd(-10, 10)
        delta = self.delta = rnd (HEIGHT/4, HEIGHT/2)
        r = self.r = rnd(2, 50)
        color = self.color = RED
        self.live = 1

    def move (self):
        if (math.fabs (HEIGHT/2 - self.y) > self.delta):
            self.vy = -self.vy
        self.y += self.vy

    def hit(self, point=1):
        global points
        points += point

    def draw(self):
        pygame.draw.circle (screen, self.color, (self.x, self.y), self.r)

def draw_score(points):
    font = pygame.font.Font(None, 72)
    text = font.render(str(points), True, CYAN)
    place = text.get_rect(center=(50, 50))
    screen.blit(text, place)

def draw_count (bullet):
    font = pygame.font.Font(None, 12)
    text = font.render("Вы уничтожили цель за " + str(bullet) + " выстрела",  True, BLACK)
    place = text.get_rect(center=(HEIGHT/2, WIDTH/2))
    screen.blit(text, place)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
points = 0
balls = []
targets = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target()
target12 = Target()
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    for target in targets:
        target.draw()
    for b in balls:
        b.draw()
    draw_score (points)
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for target in targets:
        target.move ()
        for b in balls:
            b.move()
            if b.hittest(target) and target.live:
                target.live = 0
                target.hit()
                target.new_target()
                balls.remove (b)
            if (b.live < 0):
                target.balls_count += 1
                balls.remove (b)
    gun.power_up()

pygame.quit()
