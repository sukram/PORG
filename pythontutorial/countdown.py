import thread
import time

counter = 1
input_command = 1
counter_lock = thread.allocate_lock()
write_lock = thread.allocate_lock()

def countdown(time):
    countdown = time
    while countdown >= 0:
        countdown -= 1
    print "Countdown abgelaufen"

def second_countdown(seconds):
    countdown = time.time() + seconds
    while countdown - time.time() >= 0:
        pass
    print "Countdown abgelaufen"

def verbose_countdown(seconds, iden):
    identification = iden
    countdown = time.time() + seconds
    last_note = time.time()
    global counter
    while countdown - time.time() >= 0:
        if time.time() - last_note >= 1:
            print "Countdown", identification
            print "Restzeit", int(countdown - time.time()) + 1, "Sekunden"
            last_note = time.time()
    print "Countdown abgelaufen"
    counter -= 1

def safe_countdown(seconds, iden):
    identification = iden
    countdown = time.time() + seconds
    last_note = time.time()
    global counter
    while countdown - time.time() >= 0:
        if time.time() - last_note >= 1:
            write_lock.acquire()
            print "Countdown", identification
            print "Restzeit", int(countdown - time.time()) + 1, "Sekunden"
            last_note = time.time()
            write_lock.release()
    print "Countdown abgelaufen"
    counter_lock.acquire()
    counter -= 1
    counter_lock.release()


while input_command != "exit":
    input_command = raw_input ("Countdownlaenge: ")
    commands = input_command.split(" ")
    time_set = False
    counter_time = 0
    for c in commands:
        if c.isalnum() and not time_set:
            counter_time = int(c)
            time_set = True
            if c == commands[-1]:
                thread.start_new_thread(countdown, (counter_time,))
        elif c.startswith("-"):
            if c == "-se":
                thread.start_new_thread(second_countdown, (counter_time,))
                counter_lock.acquire()
                counter += 1
                counter_lock.release()
            elif c == "-v":
                thread.start_new_thread(verbose_countdown, (counter_time,
                                                            counter))
                counter_lock.acquire()
                counter += 1
                counter_lock.release()
            elif c== "-sa":
                thread.start_new_thread(safe_countdown, (counter_time,
                                                         counter))
                counter_lock.acquire()
                counter += 1
                counter_lock.release()
    counter_lock.acquire()
    counter += 1
    counter_lock.release()

