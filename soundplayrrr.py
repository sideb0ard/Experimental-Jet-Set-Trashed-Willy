import subprocess
import threading


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


class IntroLoop(threading.Thread):
    def run(self):
        subprocess.call(["play", "-q", "wavs/bullloop2.wav", "repeat", "999"])
        return
