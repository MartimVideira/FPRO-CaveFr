import pygame
import sys

import pathlib
from pathlib import Path


BACKGROUNDCOULOR = (202, 83, 182)


def image_flip(image, xflip=False, yflip=False, cor=(255, 255, 255)):
    final = pygame.transform.flip(image, xflip, yflip)
    final.set_colorkey(cor)
    return final


def image_rotations(image, cor=(255, 255, 255)):
    rotacoes = []
    for c in range(1, 4):
        final = pygame.transform.rotate(image, c*90)
        final.set_colorkey(cor)
        rotacoes.append(final)
    return rotacoes


def transformations_dir(target='maptiles'):
    targetdir = Path(target)
    if not(targetdir.exists()):
        targetdir.mkdir()

    return target


diretorio = transformations_dir()  # diretorio final
path = Path('images')  # diretorio de onde tirar as imagens

# Põem as imagens e as transformações no novo diretorio

contador1 = 0
for imagem in (path.glob('*.png')):
    imagename = imagem.name[:-4]
    image = pygame.image.load(str(imagem))
    pixels = pygame.PixelArray(image)
    pixels = pixels.replace((255, 255, 255), (202, 83, 182))
    contador = 0
    newdir = (diretorio + '\\' + imagename)
    Path(newdir).mkdir()
    for c in range(0, 2):

        for i in range(0, 2):
            flipped = image_flip(image, i, c)
            pygame.image.save(flipped, newdir+'\\'+str(contador)+'.png')
            contador += 1

    for c in image_rotations(image):
        pygame.image.save(c, newdir+'\\'+str(contador)+'.png')
        contador += 1
    contador1 += 1


def image_flip(image, xflip=False, yflip=False, cor=(255, 255, 255)):
    final = pygame.transform.flip(image, xflip, yflip)
    final.set_colorkey(cor)
    return final
