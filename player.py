import curses


class Player():

    def __init__(self):
        pass

    def handle_key(self, keychar, willy):

        if keychar == curses.KEY_UP:
            willy.fire()
        elif keychar == curses.KEY_DOWN:
            willy.direction = 999999  # random

        if keychar == curses.KEY_LEFT:
            willy.direction = 0
            willy.location.x -= 1
        elif keychar == curses.KEY_RIGHT:
            willy.direction = 1
            willy.location.x += 1

        if keychar == ord(' '):
            willy.jump()
            # willy.fire()
