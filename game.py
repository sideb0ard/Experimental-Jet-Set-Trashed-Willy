import curses

from player import Player
from ball import Ball
from willy import Willy
from vector import Vector


class Game:

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self._screen_y, self._screen_x = self.stdscr.getmaxyx()

        self._player = Player()
        self._ball = Ball(self._screen_y, self._screen_x)
        self._willy = Willy(self._screen_y, self._screen_x)

        self.gobjects = []

        self._wind = Vector(0.01, 0)
        self._gravity = Vector(0, 0.1)

    def draw(self):
        self.stdscr.erase()

        # HAS WINDOW BEEN RESIZED?
        resize = curses.is_term_resized(self._screen_y, self._screen_x)
        if resize is True:
            self._screen_y, self._screen_x = self.stdscr.getmaxyx()
            self.stdscr.clear()
            curses.resizeterm(self._screen_y, self._screen_x)

        # BORDERZ
        for i in range(self._screen_y - 1):
            self.stdscr.addstr(i, 0, str("||"))
            self.stdscr.addstr(i, self._screen_x - 3, str("||"))

        for i in range(self._screen_x - 1):
            self.stdscr.addstr(0, i, str("="))
            self.stdscr.addstr(self._screen_y - 1, i, str("="))
        # END BORDERZ

        self._ball.applyForce(self._wind)
        # self._ball.applyForce(self._gravity)

        self._ball.take_step(self.stdscr, self._willy)
        self._ball.draw(self.stdscr)

        self._willy.update(self.stdscr)
        self._willy.draw(self.stdscr)

        self.stdscr.refresh()

    def handle_key(self, keychar):
        self._player.handle_key(keychar, self._willy)

    def addGobj(self, new_object):
        self.gobjects.append(new_object)
