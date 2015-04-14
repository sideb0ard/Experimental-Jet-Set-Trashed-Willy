import curses


class Player():

    def __init__(self):
        pass

    def handle_key(self, keychar, willy, screen):

        if keychar == curses.KEY_UP:
            willy.jump()
        elif keychar == curses.KEY_DOWN:
            # willy.velocity.x = 0
            pass

        if keychar == curses.KEY_LEFT:
            willy.velocity.x -= 0.5
        elif keychar == curses.KEY_RIGHT:
            willy.velocity.x += 0.5

        if keychar == ord(' '):
            willy.fire()
