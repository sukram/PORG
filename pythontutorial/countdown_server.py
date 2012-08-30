# coding=utf-8

import SocketServer
import countdown_package
import thread

class Variable_transporter:
    """Diese Klasse transportiert die beiden Locks und den globalen counter. Das
    ist nicht die eleganteste Lösung, soll aber zeigen, wie die Übergabe von
    Klassen wirkt. def __init__ ist dabei der Kontruktor einer Klasse in dem
    alle Attribute mit self.Variablenname initialisiert werden.
    """
    def __init__(self):
        self.counter = 1
        self.counter_lock = thread.allocate_lock()
        self.write_lock = thread.allocate_lock()


class Countdown_request_handler(SocketServer.BaseRequestHandler):
    """ Diese Klasse bearbeitet unsere eingehenden Anfragen an den Server. Die
    Methoden dazu werden von SocketServer.BaseRequestHandler geerbt.
    Für jede eingehende Verbindung wird später eine neue Instanz erzeugt.
    Vererbungen stehen bei Python in der Klammer nach dem Namen einer Klasse.
    """
    def handle(self):
        """Diese Funktion ist im BaseRequestHandler als abstract definiert und
        wird hier jetzt spezifiziert. Sie wird immer aufgerufen, wenn eine
        Netzwerkanfrage eingeht.
        """
        """Es wird für diese Verbindung eine Instanz der wichtigen Variablen
        erzeugt.
        """
        transporter = Variable_transporter()
        """self.client_adress[] enthält ein Tupel der Form
        (<IP-Adresse>,<Port>) des Clienten, der die Verbindung geöffnet hat.
        """
        client_address = self.client_address[0]
        print "[%s] Verbindung hergestellt" % client_address
        """Endlosschleife, die alle eingehenden Nachrichten bearbeitet"""
        while True:
            """Empfange eine Nachricht, die maximal 1024 Byte groß ist"""
            message = self.request.recv(1024)
            """Wenn exit empfangen wird, schließt der Client die Verbindung,
            deswegen kann die Schleife beendet werden.
            """
            if message == "exit":
                print "[%s] Verbindung geschlossen" % client_address
                break
            else : 
                """Dies ist im groben und ganzen die gleiche Implementierung
                der Countdown, die schon aus dem Countdownprogramm bekannt ist
                nur das jetzt auch die Transporter-Klasse mit übergeben wird
                sobald nötig.
                """
                commands = message.split(" ")
                time_set = False
                counter_time = 0
                for c in commands:
                    if c.isalnum() and not time_set:
# TODO : Überprüfung ob es sich um einen anderen Zahlendatentyp handelt (float)
                        counter_time = int(c)
                        time_set = True
                        if c == commands[-1]:
                            thread.start_new_thread(countdown_package.countdown, (counter_time,))
                    elif c == "-se":
                        thread.start_new_thread(countdown_package.second_countdown, (counter_time,))
                        transporter.counter_lock.acquire()
                        transporter.counter += 1
                        transporter.counter_lock.release()
                    elif c == "-v":
                        thread.start_new_thread(countdown_package.verbose_countdown, (counter_time,
                                                                                      transporter.counter,
                                                                                      transporter,))
                        transporter.counter_lock.acquire()
                        transporter.counter += 1
                        transporter.counter_lock.release()
                    elif c== "-sa":
                        thread.start_new_thread(countdown_package.safe_countdown, (counter_time,
                                                                                   transporter.counter,
                                                                                   transporter,))
                        transporter.counter_lock.acquire()
                        transporter.counter += 1
                        transporter.counter_lock.release()

"""Erstellt das Server-Socket. ThreadingTCPServer steht dabei für einen
TCP-Server, der eingehende Verbindungen von mehreren Clienten akzeptieren kann
und für jede einen Handler aufruft. Der erste Parameter ist ein Tupel, dass die
IP-Adressen für die der Prozess Anfragen entnehmen soll und seinen Port
enthält. Ist der String für die IP-Adressen leer, so werden alle lokalen wie
z.B. 127.0.0.1 und localhost verwendet.
"""
countdown_server = SocketServer.ThreadingTCPServer(("", 50000), 
                                                    Countdown_request_handler,)
"""serve_forever() weisst den Server an eine unbestimmte Zahl von Verbindungen
einzugehen und hört erst damit auf wenn shutdown() aufgerufen wird. Da
shutdown() hier nicht benutzt wird muss das Programm mit STRG+C beendet werden.
"""
countdown_server.serve_forever()
