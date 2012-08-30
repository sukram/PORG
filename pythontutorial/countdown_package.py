# coding=utf-8
"""
Dieses Packet enthält Funktionen für 4 verschiedene Countdowns.
1) Countdown(countdown(time)): Der Coundtdown läuft eine bestimmte Anzahl von
Schleifendurchläufen. Dies kann je nach System unterschiedlich lange sein.
2) Sekunden-Countdown(second_countdown(time)): Der Countdown läuft eine 
bestimmte Anzahl an Sekunden.
3) Verbose-Countdown(verbose_countdown(time,id)): Der Countdown zeigt jede 
Sekunde an, wie lange er noch läuft. Allerdings gibt es einige Probleme 
sollten mehrere Countdowns laufen.
4) Sicherer Countdown(safe_countdown(time,id)): Auch mehrere Countdowns 
funktionieren ohne Probleme.
"""

"""
Nötiger Import für Zeitverwaltung.
"""
import time

"""
Eine Besonderheit von Python ist, dass nicht zwangsläufig eine Klasse und eine
Main-Methode benötigt werden.
Pythonvariablen brauchen keinen Datentyp, da es sich eigentlich lediglich um 
eine Referenz auf eine Instanz handelt. variable.type() gibt den Typ des 
Objekts wieder, dass von variable refernziert wird, aus.
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
>iden< entspricht der ID des Countdown.
>handler< ist die globale Klasse, die einige gemeinsame Variablen
transportiert.
"""

def verbose_countdown(seconds, iden, handler):
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
    handler.counter -= 1

"""Funktion des Safe Countdowns.
>seconds< entspricht der Anzahl der Sekunden, die der Countdown laufen soll.
>iden< entspricht der ID des Countdown
>handler< ist die globale Klasse, die einige gemeinsame Variablen
transportiert.
"""

def safe_countdown(seconds, iden, handler):
    identification = iden
    countdown = time.time() + seconds
    last_note = time.time()
    while countdown - time.time() >= 0:
        if time.time() - last_note >= 1:
            """Lock auf das Schreiben im Terminal wird gesperrt, sodass kein
            anderer parallel laufender Prozess etwas dazwischen schreiben kann
            """
            handler.write_lock.acquire()
            print "Countdown", identification
            print "Restzeit", int(countdown - time.time()) + 1, "Sekunden"
            """Lock wird wieder freigegeben, sodass andere parallel laufende
            Prozesse wieder schreiben können
            """
            handler.write_lock.release()
            last_note = time.time()
    print "Countdown abgelaufen"
    """Lock zu Veränderung der globalen Variable counter wird wie das
    Schreib-Lock gesperrt und wieder entsperrt. So wird verhindert, dass ein
    Prozess die Variable ausliest, dann ein anderer sie ausliest und schreibt,
    bevor der Erste die Variable ausgehend von seinem inzwischen veralteten
    Wert verändert und schreibt, sodass die Änderung des zweiten Prozesses
    verloren geht.
    """
    handler.counter_lock.acquire()
    handler.counter -= 1
    handler.counter_lock.release()
