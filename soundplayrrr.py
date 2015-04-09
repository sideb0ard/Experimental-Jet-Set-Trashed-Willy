import subprocess
import threading
from random import randint


class Fire(threading.Thread):
    def run(self):
        subprocess.call(["afplay", "wavs/fire.wav"])
        return


class Hit(threading.Thread):
    def run(self):
        subprocess.call(["afplay", "wavs/hit.wav"])
        return


class Bump(threading.Thread):
    def run(self):
        subprocess.call(["afplay", "wavs/bump.wav"])
        return


class Jump(threading.Thread):
    def run(self):
        subprocess.call(["afplay", "wavs/jump.wav"])
        return


class Whoosh1(threading.Thread):
    def run(self):
        subprocess.call(["afplay", "wavs/whoosh1.wav"])
        return


class Whirr(threading.Thread):
    def run(self):
        subprocess.call(["afplay", "wavs/whirr.wav"])
        return


class Snik(threading.Thread):
    def run(self):
        subprocess.call(["afplay", "wavs/snik.wav"])
        return


class IntroLoop(threading.Thread):
    def run(self):
        subprocess.call(["play", "-q", "wavs/bullloop2.wav", "repeat", "999"])
        return


class BeatLoop(threading.Thread):
    loop = True
    loops = ["wavs/jayzishloop.wav"]

    def run(self):
        while self.loop is True:
            subprocess.call(["play", "-q",
                            self.loops[randint(0, len(self.loops) - 1)]])
        return
