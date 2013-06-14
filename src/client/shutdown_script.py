# coding=utf-8
import socket

server_ip = "localhost"
message = ""
logged_in = "False"
porg_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
porg_socket.connect((server_ip, 50000))
# Logging in as special user
while "False"==logged_in:
    user = "admin"
    passwd = "superpassword"
    message = user + " " + passwd
    porg_socket.send(message.encode('utf-8'))
    logged_in = porg_socket.recv(1024)
    if logged_in=="False":
        print("Unable to login with given user and password")
    else:
        print("Logged in as",user)
try:
    """Solange der Benutzer nicht "exit" als Nachricht eingibt wird die
    Nachricht immer von dem socket verschickt.
    """
    message = "shutdown"
    porg_socket.send(message.encode('utf-8'))
    message = "exit"
    porg_socket.close()
finally:
    pass