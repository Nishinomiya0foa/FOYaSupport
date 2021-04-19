from threading import Timer


def printd():
    print(123)


while True:
    t = Timer(5, function=printd)

    t.setDaemon(True)
    t.start()
    t.join()
