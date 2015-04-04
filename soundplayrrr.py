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
