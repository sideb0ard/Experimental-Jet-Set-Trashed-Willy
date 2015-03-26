import curses

# FILES


class gameObject(object):
    _xSpeed = 0
    _ySpeed = 0
    _x = 1
    _y = 1
    _shape = ""

    # PLAYER INFO?
    _plrGold = 2

    def __init__(self, gameobject):
        self._gameobject = gameobject

        # COLORS
        # - Player
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)

    def draw(self, stdscr):
        stdscr.addstr(self._y, self._x, self._shape, curses.color_pair(1))

    def checkCollision(self):
        if self._y < 1:
            self._ySpeed = 1

        if self._y > self._gameobject._screen_y - 1:
            self._ySpeed = -1

        if self._x < 1:
            self._xSpeed = 1

        if self._x > self._gameobject._screen_x:
            self._xSpeed = -1

        return True

    def move(self):
        if self._xSpeed != 0 or self._ySpeed != 0:
            if self.checkCollision() is True:
                self._x += self._xSpeed
                self._y += self._ySpeed
        self._xSpeed = 0
        self._ySpeed = 0
