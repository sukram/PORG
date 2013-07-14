import pygame, sys,os
from pygame.locals import *
import pygame_client_funcs, pygame_client_classes

class Character(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = pygame_client_funcs.load_image("marker.bmp")
        self.name = player
        self.position = (20,20)

    def update(self):
        self.rect.topleft = self.position
        print("position changed to ", self.rect.midtop, " because of ", self.position)

    def get_position(self):
        return self.position

    def walk(self, coordinates):
        self.position = coordinates