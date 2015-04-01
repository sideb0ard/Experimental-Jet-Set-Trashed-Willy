import curses
from vector import Vector


class Player():

    def __init__(self):
        pass

    def handle_key(self, keychar, willy):
        # MOVEMENT
        if keychar == curses.KEY_UP:
            willy.jump()
            # willy._location.sub(Vector(13, 0))
        elif keychar == curses.KEY_DOWN:
            pass
        if keychar == curses.KEY_LEFT:
            willy._location.sub(Vector(0, 1))
        elif keychar == curses.KEY_RIGHT:
            willy._location.add(Vector(0, 1))
