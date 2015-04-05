import curses


class Player():

    def __init__(self):
        pass

    def handle_key(self, keychar, willy, screen):

        if keychar == curses.KEY_UP:
            willy.location.y -= 2
            willy.directionUpDown = 0
        elif keychar == curses.KEY_DOWN:
            willy.location.y += 2
            willy.directionUpDown = 1

        if keychar == curses.KEY_LEFT:
            willy.location.x -= 2
            willy.directionLeftRight = 0
        elif keychar == curses.KEY_RIGHT:
            y, x = screen.getmaxyx()
            if x - len(willy.shape) <= willy.location.x < x:
                willy.location.x += 1
            else:
                willy.location.x += 2
            willy.directionLeftRight = 1

        if keychar == ord(' '):
            willy.fire()
