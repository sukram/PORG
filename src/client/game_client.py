# coding=utf-8
import socket

server_ip = input("Serveradresse:")
direction = ""
logged_in = "False"
porg_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
porg_socket.connect((server_ip, 50000))
# Logging in as special user
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
try:
    """Solange der Benutzer nicht "exit" als Nachricht eingibt wird die
    Nachricht immer von dem socket verschickt.
    """
    my_position = [0,0]
    while direction != "exit":
        direction = input("Move:")
        if direction == "exit":
            porg_socket.send(direction.encode('utf-8'))        
        else:
            porg_socket.send(("position " + direction).encode('utf-8'))
            active_chars = porg_socket.recv(1024).decode().split("#")
            character_list = list()
            del active_chars[-1]
            for line in active_chars:
                character = line.split("|")
                character_list.append(character)
            for character in character_list:
                print("Character ",character[0]," on field (",character[1],"/",character[2],")")
finally:
    porg_socket.close()
