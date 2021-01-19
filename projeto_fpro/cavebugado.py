from GameClasses import Mapa, Nave
import pygame
import time
import pytmx

pygame.init()

# Set clock
clock = pygame.time.Clock()

# screen
pygame.display.set_caption('Cave Prototype')
WINDOWSIZE = (1000, 600)
screen = pygame.display.set_mode(WINDOWSIZE, 0, 32)


# Display -- tudo vai ser feito no display depois dou render do display no screen
DISPLAYSIZE = (450, 300)
display = pygame.Surface(DISPLAYSIZE, 0, 32)

# Possivelmente acrescentar à class da nave e tomar como argumento o display e as coordenadas


def fuel_bar(nave):
    def color(nave):
        if nave.fuel < (1/4) * nave.maxfuel:
            return (255, 0, 0)
        elif nave.fuel < (1/2) * nave.maxfuel:
            return (254, 226, 62)
        return (0, 255, 0)
    bar_color = color(nave)
    return pygame.Rect(360, 10, (80/nave.maxfuel)*nave.fuel, 10,), color(nave)


def score_bar(score):
    ''' Create a display surface object using display.set_mode() method of pygame.
        Create a Font object using fony.Font() method of pygame.
        Create a Text surface object i.e.surface object in which Text is drawn on it, using render() method of pygame font object.
        Create a rectangular object for the text surface object using get_rect() method of pygame text surface object.
        Set the position of the Rectangular object by setting the value of the center property of pygame rectangular object.
        Copying the Text surface object to the display surface object using blit() method of pygame display surface object.
        Show the display surface object on the pygame window using the display.update() method of pygame.'''
    font = pygame.font.SysFont('freesansbold.ttf', 45)
    text = font.render(str(score), True, (255, 255, 255, 255))
    return text


def highest_score_bar(score):
    font = pygame.font.SysFont('freesansbold.ttf', 20)

    f = open('highest.txt', 'r')
    highest = f.read()
    if int(highest) > score:
        return font.render(f'Highest Score: {highest}', True, (255, 255, 255, 255))
    else:
        f.close()
        f = open('highest.txt', 'w')
        f.write(str(score))
        return font.render(f'Highest Score: {score}', True, (255, 255, 255, 255))


# Criar a nave
nave = Nave()

# Criar o Mapa
mapa = Mapa("mapa1.tmx")


# Inicializar o estado de movimento
up = False
left = False
right = False
RUNNING = True
scroll = [0, 0]

c = 0
# Game Main Loop
while RUNNING and nave.vida > 0:  # GAME MAINLOOP
    # Em cada frame damos refresh ao display
    display.fill((1, 1, 1))
    # Este 200 e 150 é o centro do display  retirarmos isso a camera fica em relação ao display
    scroll[0] += (nave.x - scroll[0]-200)/10
    scroll[1] += (nave.y - scroll[1]-150)/10
    # poem o mapa no dispay conforme o scroll e retorna uma lista para as colisoes
    lista_teste_colisoes = mapa.blits(display, scroll)

    # obtenho e dou render à barra em função do combustivel
    # futuramente alterar isto para uma só funcão que aceita o display como arg
    fuel_bar_rect, bar_color = fuel_bar(nave)
    pygame.draw.rect(display, bar_color, fuel_bar_rect)

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

    # Lidar com o movimento da Nave
    nave.gravity()
    if up:
        nave.move('up')

    if left and right:
        nave.move('up')
    elif left:
        nave.move('left')

    elif right:
        nave.move('right')

    nave.upadate_coordinates(lista_teste_colisoes)
    # Depois de incrementada a velocidade ou seja do efeito da aceleração
    # atualizamos a posicção e testamos as colisoes com este ultimo metodo

    display.blit(nave.get_image(), (nave.x-scroll[0], nave.y-scroll[1]))
    screen.blit(pygame.transform.scale(display, WINDOWSIZE), (0, 0))
    screen.blit(score_bar(c), (500, 50))
    screen.blit(highest_score_bar(c), (470, 80))

    pygame.display.update()
    c = c + 1
    clock.tick(60)


time.sleep(2)
pygame.quit()
