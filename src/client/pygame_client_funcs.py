import pygame, sys,os
import socket
from pygame.locals import * 

def input(events, socket): 
    for event in events:
        direction = ""
        if event.type == QUIT: 
            sys.exit(0) 
        else:
            if(event.type == KEYDOWN):
                if event.key == 118:
                    direction = "w"
                elif event.key == 117:
                    direction = "a"
                elif event.key == 105:
                    direction = "s"
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
                active_chars = socket.recv(1024).decode().split("#")
                character_list = list()
                del active_chars[-1]
                for line in active_chars:
                    character = line.split("|")
                    character_list.append(character)
                for character in character_list:
                    print("Character ",character[0]," on field (",character[1],"/",character[2],")")