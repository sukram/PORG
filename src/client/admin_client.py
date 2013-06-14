# coding=utf-8
import socket

server_ip = input("Serveradresse:")
message = ""
logged_in = "False"
porg_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
porg_socket.connect((server_ip, 50000))
# Logging in as special user
while "False"==logged_in:
    user = input("Username:")
    passwd = input("Password:")
    message = user + " " + passwd
    porg_socket.send(message.encode('utf-8'))
    logged_in = porg_socket.recv(1024).decode()
    if logged_in=="False":
        print("Unable to login with given user and password")
    else:
        print("Logged in as ",user)
try:
    """Solange der Benutzer nicht "exit" als Nachricht eingibt wird die
    Nachricht immer von dem socket verschickt.
    """
    while message != "exit":
        message = input("Command:")
        porg_socket.send(message.encode('utf-8'))
finally:
    porg_socket.close()
