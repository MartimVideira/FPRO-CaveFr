from functools import reduce
import functools
import pygame
from pygame.locals import *
pygame.init()

# Clock Inicializador para manter os frames
clock = pygame.time.Clock()

# Sobre a janela principal
WINDOWSIZE = (600, 400)
pygame.display.set_caption('PlataForma')
screen = pygame.display.set_mode(WINDOWSIZE, 0, 32)  # Iniciar ecra
DISPLAYSIZE = (300, 200)
display = pygame.Surface(DISPLAYSIZE)
"""Como as imagens são um pouco pequenas vamos por as imagens no display de res 300X200
depois vamos dar render ao display no scren mas scaled up assim as imagens tambem ficam maiores
Isto permite-nos mostrar imagens dentro de outras imagens
Basicamente vamos por tudo primeiro no display e no final de cada loop damos render ao display
no era"""


# Sobre o Jogador
player_image = pygame.image.load('images/mario.png')
# Estamos a por o bg do modelo do player a transparente
player_image.set_colorkey((255, 255, 255))

player_location = [50, 50]

# ciar retangulo sobre o player para testar colisões futuramente
player_rect = pygame.Rect(
    player_location[0], player_location[1], player_image.get_width(), player_image.get_height())


# Relva
grass_image = pygame.image.load('images/grass.png')

# Terra
dirt_image = pygame.image.load('images/dirt.png')
BLOCOSIZE = grass_image.get_width()
#  MOVIMENTO E MAPA
moving_left = False
moving_right = False
jump = False
player_velocity = [0, 0]
air_timer = 0
player_y_momentum = 0
collision_types = {'top': False, 'bottom': False,
                   'left': False, 'right': False}


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)

    return hit_list


def move(rect, movement, tiles):
    ''' rect é o rectangulo do jogador
    movement = [x,y]  é como se está a mover
    tiles é a lista das coisas com as quais podemos colidir
    tenho que definir no corpo da função os tipos de colisões
    ses for uma colisão com bloco à esquerda o player recebe a posição mais à direita do bloco
    se for uma colisão com bloco à direita o player recebe a posição mais À esquerda do bloco
    se for uma colisão com bloco em cima o player recebe a posição mais em baixo do bloco
    e por fim  se for uma colisão em baixo o player recebe a posição mais a cima do bloco

    É recomendado tratar o movimento dos eixos separadamente
    e é o que faço, primeiro dou update à posição do player segundo o x e faco o teste de
    colisões etc etc
    faço o mesmo para o eixo do y

    '''

    collision_types = {'top': False, 'bottom': False,
                       'left': False, 'right': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:  # entra no loop com os blocos que colidimos
        if movement[0] >= 0:  # se velocidade for positiva estamos a ir para a direita
            rect.right = tile.left  # como descrevi na docstrin
            collision_types['right'] = True
        elif movement[0] <= 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:  # eixo y é invertidos  significa que estamos a cair
            rect.bottom = tile.top
            collision_types['bottom'] = True
        if movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True

    return rect, collision_types


'''
# Dou render ao map antes do game loop para diminuir a complexidade e aumentar a performance
# em cada loop do jogo dou blit ao map_disply no display
# Mudei o mapa para um ficheiro de texto

def loadmap(path):
    f = open(path + '.txt', 'r')
    dados = f.read()
    f.close()
    dados = dados.split('\n')
    game_map = []
    y = 0
    for camada in dados:
        game_map.append(camada)

    return game_map
'''

game_map = loadmap('mapa1')

scroll = [0, 0]
map_display = pygame.Surface(DISPLAYSIZE)

# NAVE


class nave():
    def __init__(self):
        self.x = 100
        self.y = 100
        self.height = 10
        self.width = 10
        self.color = (255, 0, 0)
        self.goingleft = False
        self.goingright = False
        self.fuel = 1000

        self.limitedownvelocity = 7
        self.gravityacc = 0.05

        self.limitevx = 3
        self.xacc = 0.05

        self.limiteupvelocity = 3
        self.yacc = 0.05

        self.velocidade = [0, 0]
        self.image = pygame.image.load('images/mario.png')

    def coordinates(self):
        return self.x, self.y

    def upadate_coordinates(self):
        self.x = self.x + self.velocidade[0]
        self.y = self.y + self.velocidade[1]

    def gravity(self):
        if self.velocidade[1] < 7:
            self.velocidade[1] += self.gravityacc

    def up(self):
        if self.velocidade[1] > -3:
            self.velocidade[1] -= 0.3
        self.goingleft = False
        self.goingriht = False

    def left(self):
        if self.velocidade[0] > - self.limitevx:
            self.velocidade[0] -= self.xacc
        self.goingleft = True
        self.goingriht = False

    def right(self):
        if self.velocidade[0] < self.limitevx:
            self.velocidade[0] += self.xacc
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


nave = nave()
up = False
left = False
right = False
RUNNING = True
while RUNNING:  # GAME MAIN LOOP
    # estamos sempre a dar refresh ao display  com esta cor que é o bg

    map_display.fill((146, 244, 255))
    # Sobre a CAMARA // SCROLL TEMOS a camara nos xx e nos yy
    # a cada itreracção acrescentamos uma fração entre a posição da camara e do player
    # o 152 e o 106 é para centrá-los em relção ao display
    # ao acrescentarmos fração à camara e ao player temos que apenas aplicar ao blit das imagens
    # senão trará problemas nos rects, teria que dar update a tudo

    scroll[0] += (nave.x - scroll[0]-152)/10
    scroll[1] += (nave.y - scroll[1]-106)/10

    blocos_rect = []
    n_camada = 0
    for camada in game_map:
        n_coluna = 0
        for bloco in camada:
            # Neste caso os blocos têm o mesmo tamanho logo cria-se uma variavel geral
            posicão_bloco = (n_coluna*BLOCOSIZE, n_camada * BLOCOSIZE)
            posicão_blit = posicão_bloco[0] - \
                scroll[0], posicão_bloco[1]-scroll[1]
            if bloco == '1':
                map_display.blit(dirt_image, posicão_blit)
            elif bloco == '2':
                map_display.blit(grass_image, posicão_blit)
            if bloco != '0':
                x = pygame.Rect(
                    posicão_bloco[0], posicão_bloco[1], BLOCOSIZE, BLOCOSIZE)
                blocos_rect.append(x)
            n_coluna += 1
        n_camada += 1
    display.blit(map_display, (0, 0))

    # Handles the player movement
    player_velocity = [0, 0]

    if moving_right:
        player_velocity[0] += 2
    if moving_left:
        player_velocity[0] -= 2
    player_velocity[1] += player_y_momentum

    on_ground = collision_types['bottom']
    if on_ground:
        player_y_momentum = 0
        air_timer = 0
        was_on_ground = True
    else:
        air_timer += 1
    jump_condition = jump and air_timer < 8 and was_on_ground
    if jump_condition:
        player_y_momentum = -3.3
        was_on_ground = False
        jump = False

    on_air = collision_types['top']
    if on_air:
        player_y_momentum = 0
    player_y_momentum += 0.20
    if player_y_momentum > 3:
        player_y_momentum = 3

    player_velocity[1] += player_y_momentum
    , collision_types = move(
        player_rect, player_velocity, blocos_rect)

    display.blit(player_image, (player_rect.x -
                                scroll[0], player_rect.y - scroll[1]))
    for event in pygame.event.get():  # loop dos eventos:
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
                right = True
            if event.key == K_LEFT:
                moving_left = True
                left = True
            if event.key == K_UP:
                jump = True
                up = True
            if event.key == K_SPACE:
                up = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
                right = False
            if event.key == K_LEFT:
                moving_left = False
                left = False
            if event.key == K_UP:
                jump = False
                up = False
            if event.key == K_SPACE:
                up = False
    if up:
        nave.move('up')
    else:
        nave.gravity()
    if left:
        nave.move('left')
    if right:
        nave.move('right')
    nave.upadate_coordinates()
    display.blit(nave.get_image(), (nave.x-scroll[0], nave.y - scroll[1]))

    screen.blit(pygame.transform.scale(display, WINDOWSIZE), (0, 0))
    pygame.display.update()  # dá update ao que fizesmos numa iteração do loop
    clock.tick(60)  # sets the frame rate to 60

pygame.quit()
