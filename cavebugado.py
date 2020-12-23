import pygame

pygame.init()

# Set clock
clock = pygame.time.Clock()

# screen
pygame.display.set_caption('Cave Prototype')
WINDOWSIZE = (900, 600)
screen = pygame.display.set_mode(WINDOWSIZE, 0, 32)


# Display -- tudo vai ser feito no display depois dou render do display no screen
DISPLAYSIZE = (450, 300)
display = pygame.Surface(DISPLAYSIZE, 0, 32)

# Classe da nave


class Nave():
    def __init__(self):
        self.x = 100
        self.y = 100

        self.goingleft = False
        self.goingright = False

        self.maxfuel = 600
        self.fuel = self.maxfuel

        self.velocidade = [0, 0]

        self.limitedownvelocity = 7
        self.limitevx = 1
        self.limiteupvelocity = 1

        self.gravityacc = 0.05
        self.single_propulsor = 0.15
        self.double_propulsor = 0.3

        self.image = pygame.image.load('images/spaceship1.png')

    def coordinates(self):
        return self.x, self.y

    def upadate_coordinates(self):
        self.x = self.x + self.velocidade[0]
        self.y = self.y + self.velocidade[1]

    def gravity(self):
        if self.velocidade[1] < 1:
            self.velocidade[1] += self.gravityacc

    def up(self):
        if self.velocidade[1] > -self.limiteupvelocity:
            self.velocidade[1] -= self.double_propulsor
        self.goingleft = False
        self.goingright = False

    def left(self):
        if self.velocidade[0] > - self.limitevx:
            self.velocidade[0] -= self.single_propulsor

        if self.velocidade[1] > -self.limiteupvelocity:
            self.velocidade[1] -= self.single_propulsor

        self.goingleft = True
        self.goingright = False

    def right(self):
        if self.velocidade[0] < self.limitevx:
            self.velocidade[0] += self.single_propulsor
        if self.velocidade[1] > - self.limiteupvelocity:
            self.velocidade[1] -= self.single_propulsor

        self.goingleft = False
        self.goingright = True

    def move(self, direcao):

        if self.fuel > 0:
            if direcao == 'up':
                self.up()
            elif direcao == 'left':
                self.left()
            elif direcao == 'right':
                self.right()
            self.fuel -= 1

    def get_image(self):
        if self.goingleft:
            y = pygame.transform.rotate(self.image, 30)
            return y
        elif self.goingright:
            return pygame.transform.rotate(self.image, -30)
        return self.image


def fuel_bar(nave):
    def color(nave):
        if nave.fuel < (1/4) * nave.maxfuel:
            return (255, 0, 0)
        elif nave.fuel < (1/2) * nave.maxfuel:
            return (254, 226, 62)
        return (0, 255, 0)
    bar_color = color(nave)
    return pygame.Rect(360, 10, (80/nave.maxfuel)*nave.fuel, 10,), color(nave)


nave = Nave()
up = False
left = False
right = False
RUNNING = True
while RUNNING:  # GAME MAINLOOP
    display.fill((175, 130, 209))
    fuel_bar_rect, bar_color = fuel_bar(nave)
    pygame.draw.rect(display, bar_color, fuel_bar_rect, )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                up = True
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                up = False
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False

    if up:
        nave.move('up')

    if left:
        nave.move('left')

    if right:
        nave.move('right')
    else:
        nave.gravity()

    nave.upadate_coordinates()
    display.blit(nave.get_image(), (nave.x, nave.y))
    screen.blit(pygame.transform.scale(display, WINDOWSIZE), (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
