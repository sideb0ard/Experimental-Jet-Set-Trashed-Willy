import time
import threading


class Message():
    def __init__(self, txt):
        self.txt = txt

    def update(self, txt):
        self.txt = txt

    def timey(self, secondsToWait, txt):
        time.sleep(secondsToWait)
        self.txt = txt

    def timedUpdate(self, secondsToWait, txt):
        t = threading.Thread(target=self.timey, args=(secondsToWait, txt))
        t.start()
