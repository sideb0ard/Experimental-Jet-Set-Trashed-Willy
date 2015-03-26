import curses

from gameObject import gameObject


class Player(gameObject):
    _x = 2
    _shape = "==="

    def __init__(self, gameobject):
        super(Player, self).__init__(gameobject)

    def handle_key(self, keychar):
        # MOVEMENT
        if keychar == curses.KEY_UP:
            self._ySpeed = -3
        elif keychar == curses.KEY_DOWN:
            self._ySpeed = 3
        if keychar == curses.KEY_LEFT:
            self._xSpeed = -3
        elif keychar == curses.KEY_RIGHT:
            self._xSpeed = 3
