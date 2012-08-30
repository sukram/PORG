# coding=utf-8
"""socket ist das Modul, dass es erlaubt einen Socket zur Netzwerkkommunikation zu
erzeugen.
"""
import socket

server_ip = raw_input("Serveradresse:")
message = ""
"""Zuerst wird der Socket erzeugt über den der Prozess mit dem Netzwerk
kommuniziert. Dabei steht AF_INET für IPv4 und SOCK_STREAM für TCP. Danach wird
eine Verbindung zu dem Prozess hergestellt, der bei der eingegeben IP_Adresse
auf Port 50000 lauscht.
"""
countdown_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
countdown_socket.connect((server_ip, 50000))
"""Dieses try-finally sorgt dafür, dass die Verbindung in jedem Fall
geschlossen wird, egal, wie die Schleife verlassen wird. (Solange der Rechner
nicht abstürzt und der Prozess dazu kommt die finally-Anweisung auszuführen)
"""
try :
    """Solange der Benutzer nicht "exit" als Nachricht eingibt wird die
    Nachricht immer von dem socket verschickt.
    """
    while message != "exit":
        message = raw_input("Countdown:")
        countdown_socket.send(message)
finally :
    countdown_socket.close()
