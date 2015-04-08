import curses


class Player():

    def __init__(self):
        pass

    def handle_key(self, keychar, willy, screen):

        if keychar == curses.KEY_UP:
            # willy.velocity.y -= 1
            # willy.location.y -= 1
            # willy.directionUpDown = 0
            willy.jump()
        elif keychar == curses.KEY_DOWN:
            willy.velocity.x = 0
            # willy.location.y += 1
            # willy.directionUpDown = 1
            # willy.jump()

        if keychar == curses.KEY_LEFT:
            willy.velocity.x -= 0.5
            # willy.location.x -= 1
            # willy.directionLeftRight = -1
            # willy.jump()
        elif keychar == curses.KEY_RIGHT:
            willy.velocity.x += 0.5
            # willy.location.x += 1
            # willy.directionLeftRight = 1
            # willy.jump()

        if keychar == ord(' '):
            willy.fire()
