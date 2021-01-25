import pytmx
import pygame


class Image():
    def __init__(self, image):
        self.image = image

    def tup_rect_image(self, position):
        image_rect = self.image.get_rect()
        pg_Rect = pygame.Rect(
            position[0], position[1], image_rect.width, image_rect.height)
        return (pg_Rect, self.image)


class Mapa():
    def __init__(self, tmx_file):
        # loads our map
        self.tmxdata = pytmx.load_pygame(tmx_file)

    def get_map_properties(self):
        pass

    def blits(self, surface, scroll=(0, 0)):
        tile_image = self.tmxdata.get_tile_image_by_gid
        collision_test_list = []
        fuel_list = []
        for layer in self.tmxdata.visible_layers:  # Vamos percorrer todas as layers visiveis
            # há varios tipos de layers nós queremos as tiles layers
            if isinstance(layer, pytmx.TiledTileLayer):

                for x, y, gid in layer:
                    tile = tile_image(gid)
                    if tile:
                        # Damos blit ao tile na posicao dele no mapa mas tendo em conta as suas dimensoes
                        surface.blit(
                            tile,
                            (x * self.tmxdata.tilewidth - scroll[0], y * self.tmxdata.tileheight-scroll[1]))
                        propriedades = self.tmxdata.get_tile_properties_by_gid(
                            gid)
                        if propriedades['fuel']:
                            my_fuel = Image(tile)
                            fuel_list.append(my_fuel.tup_rect_image((x*self.tmxdata.tilewidth,
                                                                     y*self.tmxdata.tileheight,)))
                        if propriedades['solid']:
                            my_tile = Image(tile)
                            collision_test_list.append(my_tile.tup_rect_image((x*self.tmxdata.tilewidth,
                                                                               y*self.tmxdata.tileheight,)))
        return collision_test_list, fuel_list


class Nave():
    def __init__(self):
        # Posições em que o objeto é colocado no ecrã
        self.x = 320
        self.y = 100

        # vê a orientação do movimento para rodar a nave
        self.goingleft = False
        self.goingright = False

        # Sobre o Combustível
        self.maxfuel = 600
        self.fuel = self.maxfuel

        # Atributos do Objeto Para o movimento assim novas naves podem ter outros atributos
        # Bem como podem ser feitas melhorias a uma especifica nave
        # NOTA: QUANDO implementar uma memoria vou ter que criar um construidor de objetos para guardar
        # os dados num txt e depois construílo
        self.velocidade = [0, 0]

        self.limitedownvelocity = 4  # Limite da velocidade a que pode descer
        self.limitevx = 1  # liimite da velocidade a que pode ir para os lados
        self.limiteupvelocity = 3  # limite da velocidade a que pode subir

        # Aceleração
        self.gravityacc = 0.1  # incremento da downwards velocity //gravidade
        # Quando se usa apenas um propulsor(->/<-)
        self.single_propulsor = 0.16
        self.double_propulsor = 0.16  # quando se usa os dois propulsores( up)

        self.vida = 3

        self.image = pygame.image.load('images/spaceship1.png')

    def coordinates(self):
        return self.x, self.y

    def rect(self):
        return pygame.Rect(
            self.x, self.y, self.image.get_width(), self.image.get_height())

    def upadate_coordinates(self, lista_teste_colisoes, lista_fuel):
        self.check_collisions(lista_teste_colisoes)
        self.check_collisions(lista_fuel, True)
        self.x = self.x + self.velocidade[0]
        self.y = self.y + self.velocidade[1]

    def gravity(self):
        if self.velocidade[1] < self.limitedownvelocity:
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

    # Move a nave
    def move(self, direcao,):
        move_funcs = {'up': self.up, 'left': self.left, 'right': self.right}
        if self.fuel > 0:
            move_funcs[direcao]()
            self.fuel -= 1

    def check_collisions(self, lista_teste_colisoes, fuel=False):
        # Cada elemento da lista é um tuplo do tipo (rect,imageSurface)
        for elemento in lista_teste_colisoes:
            # Se estiver nesta colisão passo ao outro tipo de deteção
            # Falso ou o tipo de colisão que está a decorrer
            collision_type = self.typecollision(elemento[0])

            if collision_type:
                obstacle_temp = pygame.Surface.copy(elemento[1])
                obstacle_temp.set_colorkey((202, 83, 182))
                obstacle_mask = pygame.mask.from_surface(obstacle_temp)
                nave_mask = pygame.mask.from_surface(self.image)

                offset = (int(self.x - elemento[0].topleft[0]),
                          int(self.y - elemento[0].topleft[1]))

                if obstacle_mask.overlap(nave_mask, offset):

                    if fuel and collision_type == 'corner':
                        self.fuel = self.maxfuel

                    self.velocidade[0] *= -0.7
                    self.velocidade[1] *= -0.7
                    self.x = self.x + self.velocidade[0]
                    self.y = self.y + self.velocidade[1]
                    if not fuel:
                        self.vida -= 1
                    break

    def typecollision(self, test_rect):
        if not(self.rect().colliderect(test_rect)):
            return False

        canto1 = test_rect.collidepoint(self.rect().topleft)
        canto2 = test_rect.collidepoint(self.rect().topright)
        canto3 = test_rect.collidepoint(self.rect().bottomleft)
        canto4 = test_rect.collidepoint(self.rect().bottomright)

        mid1 = self.rect().collidepoint(test_rect.midtop)
        m1d2 = self.rect().collidepoint(test_rect.midbottom)
        m1d3 = self.rect().collidepoint(test_rect.midright)
        mid4 = self.rect().collidepoint(test_rect.midleft)
        if canto1 and canto2:
            return 'bottom'
        elif canto3 and canto4:
            return 'top'
        elif canto1 and canto3:
            return 'right'
        elif canto2 and canto4:
            return 'right'

        else:
            return 'corner'

    # retorna a um pygame.Surface da nave
    def get_image(self):
        if self.goingleft:
            y = pygame.transform.rotate(self.image, 30)
            return y
        elif self.goingright:
            return pygame.transform.rotate(self.image, -30)
        return self.image
