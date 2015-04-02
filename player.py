import curses


class Player():

    def __init__(self):
        pass

    def handle_key(self, keychar, willy):
        if keychar == curses.KEY_UP:
            willy.jump()
        elif keychar == curses.KEY_DOWN:
            pass
        if keychar == curses.KEY_LEFT:
            willy.location.x -= 1
            willy.direction = 'LEFT'
        elif keychar == curses.KEY_RIGHT:
            willy.location.x += 1
            willy.direction = 'RIGHT'
