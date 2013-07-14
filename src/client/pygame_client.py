import pygame, sys,os
import pygame_client_funcs, pygame_client_classes
import socket
from pygame.locals import * 


server_ip = input("Serveradresse:")
direction = ""
logged_in = "False"
porg_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
porg_socket.connect((server_ip, 50000))
# Logging in as special user
try:
    while "False"==logged_in:
        user = input("Username:")
        passwd = input("Password:")
        message = user + " " + passwd
        message = message.encode("utf-8")
        porg_socket.send(message)
        logged_in = porg_socket.recv(1024).decode()
        if logged_in=="False":
            print("Unable to login with given user and password")
        else:
            print("Welcome on the PORG-server,",user)
            my_position = [0,0]

    pygame.init() 

    window = pygame.display.set_mode((600, 600)) 
    pygame.display.set_caption('PORG Client') 
    screen = pygame.display.get_surface() 
    clock = pygame.time.Clock()


    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    screen.blit(background, (0, 0))

    pygame.display.flip() 

    while True: 
        clock.tick(30)
        events = pygame.event.get()
        pygame_client_funcs.input(events, porg_socket)
        character_list = pygame_client_funcs.get_screendata(porg_socket)
        allsprites = pygame_client_funcs.update_screen(character_list)
        screen.blit(background, (0, 0))
        print(allsprites)
        allsprites.update()
        allsprites.draw(screen)
        pygame.display.flip()

 
finally:
    porg_socket.close()