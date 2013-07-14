import pygame, sys,os
import socket
import pygame_client_funcs, pygame_client_classes
from pygame.locals import *

known_chars = list()
allsprites = list()

def input(events, socket): 
    for event in events:
        direction = ""
        if event.type == QUIT: 
            sys.exit(0) 
        else:
            if(event.type == KEYDOWN):
                if event.key == 118:
                    direction = "s"
                elif event.key == 117:
                    direction = "a"
                elif event.key == 105:
                    direction = "w"
                elif event.key == 97:
                    direction = "d"
                elif event.key == 27:
                    direction = "exit"
            elif(event.type == KEYUP):
                pass
            else:
                print(event)
            if direction == "exit":
                socket.send(direction.encode('utf-8'))
                sys.exit(0)
            elif direction == "":
                pass        
            else:
                socket.send(("position " + direction).encode('utf-8'))
                
def get_screendata(socket):
    socket.send("screendata".encode('utf-8'))
    server_chars = socket.recv(1024).decode().split("#")
    character_list = list()
    del server_chars[-1]
    for line in server_chars:
        character = line.split("|")
        character_list.append(character)
    return character_list

def update_screen(character_list):
    renderer = pygame.sprite.RenderPlain(allsprites)
    for character in character_list:
        char_known = False
        for known_char in known_chars:
            if known_char.name == character[0]:
                known_char.walk((int(character[1]),int(character[2])))
                char_known = True
            print(known_char.name, " has position ", known_char.rect.midtop)
        if char_known == False:
            new_char = pygame_client_classes.Character(character[0])
            new_char.walk((int(character[1]),int(character[2])))
            known_chars.append(new_char)
            allsprites.append(new_char)
            renderer = pygame.sprite.RenderPlain(allsprites)

        print("Character ",character[0]," on field (",character[1],"/",character[2],")")

    return renderer

def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print("Cannot load image:", name)
        raise SystemExit
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()