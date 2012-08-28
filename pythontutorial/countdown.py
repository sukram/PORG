"""
Dieses Programm führt 4 verschiedene Countdowns aus.
Die Art des Countdowns wird über eine an den Countdown angehängten
Optionsparameter bestimmt.
1) Countdown(ohne Optionsparameter): Der Coundtdown läuft eine bestimmte Anzahl von
Schleifendurchläufen. Dies kann je nach System unterschiedlich lange sein.
2) Sekunden-Countdown(-se): Der Countdown läuft eine bestimmte Anzahl an Sekunden.
3) Verbose-Countdown(-v): Der Countdown zeigt jede Sekunde an, wie lange er noch
läuft. Allerdings gibt es einige Probleme sollten mehrere Countdowns laufen.
4) Sicherer Countdown(-sa): Auch mehrere Countdowns funktionieren ohne Probleme.
"""

"""
Nötige Importe für Parallelprogrammierung und Zeitverwaltung.
"""
import thread
import time

"""
Eine Besonderheit von Python ist, dass nicht zwangsläufig eine Klasse und eine
Main-Methode benötigt werden.
Pythonvariablen brauchen keinen Datentyp, da es sich eigentlich lediglich um 
eine Referenz auf eine Instanz handelt. variable.type() gibt den Typ des 
Objekts wieder, dass von variable refernziert wird, aus.
"""

"""
Initialisierung einiger wichtiger Variablen. Pythonvariablen brauchen keinen
>counter< entspricht der id des nächsten Prozesses. ~ -1 entspricht der Anzahl
der laufenden Countdowns.
>input_command< speichert den vom Benutzer eingegebenden Befehl.Initialisierung
mit 1 damit die Menü-Schleife anläuft
>counter_lock< synchronisiert den Zugriff auf die Variable counter
>write_lock< synchronisiert die Ausgabe auf der Kommandozeile
"""

counter = 1
input_command = 1
counter_lock = thread.allocate_lock()
write_lock = thread.allocate_lock()

"""
In Python werden Funktionen mit def <Funktionsname>(<Parameter>): definiert.
Wichtig bei Python ist, dass die Einrückung eine Bedeutung hat. Statt Klammern
oder ähnlichem die einen Block beschränken benutzt Python die Einrückung als
Blockdefinition. Sobald die Einrückung aufgehoben wird, endet der jeweilige
Block.
"""

"""
Funktion des einfachen Countdown der als Übergabe die Anzahl der Schritte
bekommt.
"""

def countdown(time):
    countdown = time
    while countdown >= 0:
#Mehrfache Verschachtelung wird einfach durch weitere Einrückung gehandhabt.
        countdown -= 1
    print "Countdown abgelaufen"

"""
Funktion des Sekunden-Countdowns.
>seconds< entspricht der Anzahl der Sekunden, die der Countdown laufen soll.
"""

def second_countdown(seconds):
#Zugriffe auf importierte Funktionen funktionieren mit Paketname.Funktionsname()
    """
    time.time() gibt die seit einem systemabhängigen Zeitpunkt 0 in Sekunden als
    float aus.
    """
    countdown = time.time() + seconds
    while countdown - time.time() >= 0:
        pass
    print "Countdown abgelaufen"

"""
Funktion des Verbose-Countdowns.
>seconds< entspricht der Anzahl der Sekunden, die der Countdown laufen soll.
>iden< entspricht der ID des Countdown
"""

def verbose_countdown(seconds, iden):
    identification = iden
    countdown = time.time() + seconds
    last_note = time.time()
    """Globale Variable in der Funktion sichtbar machen"""
    global counter
    while countdown - time.time() >= 0:
        if time.time() - last_note >= 1:
            print "Countdown", identification
            print "Restzeit", int(countdown - time.time()) + 1, "Sekunden"
            last_note = time.time()
    print "Countdown abgelaufen"
    """Nach Ende des Countdowns wird der globale Zähler herabgesetzt. -= o.ä.
    kennt Python, allerdings gibt es kein ++ oder -- das um eine Varaible um 1
    hoch oder runterzählt"""
    counter -= 1

"""Funktion des Safe Countdowns.
>seconds< entspricht der Anzahl der Sekunden, die der Countdown laufen soll.
>iden< entspricht der ID des Countdown
"""

def safe_countdown(seconds, iden):
    identification = iden
    countdown = time.time() + seconds
    last_note = time.time()
    global counter
    while countdown - time.time() >= 0:
        if time.time() - last_note >= 1:
            """Lock auf das Schreiben im Terminal wird gesperrt, sodass kein
            anderer parallel laufender Prozess etwas dazwischen schreiben kann
            """
            write_lock.acquire()
            print "Countdown", identification
            print "Restzeit", int(countdown - time.time()) + 1, "Sekunden"
            """Lock wird wieder freigegeben, sodass andere parallel laufende
            Prozesse wieder schreiben können
            """
            write_lock.release()
            last_note = time.time()
    print "Countdown abgelaufen"
    """Lock zu Veränderung der globalen Variable counter wird wie das
    Schreib-Lock gesperrt und wieder entsperrt. So wird verhindert, dass ein
    Prozess die Variable ausliest, dann ein anderer sie ausliest und schreibt,
    bevor der Erste die Variable ausgehend von seinem inzwischen veralteten
    Wert verändert und schreibt, sodass die Änderung des zweiten Prozesses
    verloren geht.
    """
    counter_lock.acquire()
    counter -= 1
    counter_lock.release()

"""Diese Menü-Schleife wiederholt sich immer wieder bis das Kommando "exit"
eingegeben wird. Je nach Eingabe wird ein anderer Countdown gestartet.
"""
# TODO : Fehlermeldung bei fehlerhafter Eingabe
while input_command != "exit":
    """raw_input() liest einen String ein, während input() die Eingabe in einen
    passenden Datentypen umwandelt
    """
    input_command = raw_input ("Countdownlaenge: ")
    """Die Funktion String.split(<Parameter>) gibt eine Liste aus die alle
    Teilstrings des ursprünglichen Strings enthält wenn man ihn an allen
    Stellen teilt an denen der String <Parameter> vorkommt.
    >commands< refernziert eine Liste die die nach Leerzeichen gesplitteten
    Eingabe enthält. Bei einer korrekten Eingabe ist jeder Eintrag entweder die
    Zeitangabe für den Countdown oder ein Parameter, der die Art des Countdown
    bestimmt
    >time_set< refernziert einen Boolean, der sicherstellt, dass die Zeiteingabe
    nur einmal eindeutig durchgeführt wird
    >counter_time< referenziert die Zeitangabe für den Countdown, da diese
    außerhalb der for-Schleife definiert sein muss um kein Schleifenvariable zu
    sein
    """
    commands = input_command.split(" ")
    time_set = False
    counter_time = 0
    """In Python gibt es sogenannte foreach-Schleifen, also Schleifen, die
    ihren Block für jedes Element in einer Liste durchgehen und dieses Element
    in einer vorher definierten Variable verfügbar machen. In diesem Beispiel
    wird die Liste der gesplitteten Eingabe durchgegangen. Da bei korrekter
    Eingabe jeder Eintrag einen Parameter für den Countdown enthalten sollte
    muss jeweils entschieden werden um welchen Parameter es sich handelt.
    """
    for c in commands:
        """Es gibt verschiedene Funktionen die Wahrheitswerte über
        Eigenschaften eines Strings liefern. String.isalnum() ist wahr, wenn
        der String nur aus Nummern besteht. In unserem Beispiel ist die
        einziege Zahl die übergeben wird die Dauer des Countdowns. Da der
        Countdown in einer korrekten Eingabe nur einmal gesetzt werden soll,
        wird überprüft ob time_set noch falsch ist.
        """
        if c.isalnum() and not time_set:
            """Datentyp(<Parameter>) castet Parameter wenn möglich in den
            Datentypen. Da wir hier bereits wissen, dass der String nur aus
            Zahlen besteht ist es bei korrekter Eingabe immer möglich den
            String umzuwandeln.
            """
# TODO : Überprüfung ob es sich um einen anderen Zahlendatentyp handelt (float)
            counter_time = int(c)
            time_set = True
            """Listen können mit negativen Werten von hinten aufgerufen.
            Achtung bei der Nummerierung: 0 ist der erste Eintrag einer Liste
            von vorne, aber der erste Eintrag einer Liste von hinten ist -1 und
            nicht 0.
            Hier wird geprüft ob der aktuelle Listeneintrag der letzte ist.
            Sollte dies der Fall sein wurde nur eine Dauer für den Countdown
            eingegeben. In diesem Fall soll der einfache Countdown gestartet
            werden.
            """
            if c == commands[-1]:
                """thread.start_new_thread(<funktion>, <argumentliste>) erzeugt
                einen neuen Thread in dem die angegebene Funktionen mit ihren
                Argumenten ausgeführt wird. Auf diese Weise werden allerdings
                nur Funktionsthreads erzeugt. Objektthreads werden auf andere
                Weise gestartet.
                """
                thread.start_new_thread(countdown, (counter_time,))
            """elif hat die gleiche Wirkung wie ein else gefolgt von einem if.
            Falls der momentane Listeneintrag keine reine Zahl war, wird hier
            darauf geprüft, ob der Parameter für einen Sekunden-Countdown angegeben
            wurde.
            """
        elif c == "-se":
            thread.start_new_thread(second_countdown, (counter_time,))
            counter_lock.acquire()
            counter += 1
            counter_lock.release()
            """Hier wird nach gleichem Muster der Verbose-Countdown initiiert
            nur das diesmal counter als Parameter mit übergeben werden muss.
            """
        elif c == "-v":
            thread.start_new_thread(verbose_countdown, (counter_time,
                                                        counter))
            counter_lock.acquire()
            counter += 1
            counter_lock.release()
            """Last but not least der sichere Countdown nach gleichem Schema.
            """
        elif c== "-sa":
            thread.start_new_thread(safe_countdown, (counter_time,
                                                     counter))
            counter_lock.acquire()
            counter += 1
            counter_lock.release()
