import curses
import time

# FILES
from player import Player
from ball import Ball
from defines import GameDefines


class Game:
    pongSpeed = -1
    pongYSpeed = 1
    pongXSpeed = 1

    playerScore = 0

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self._screen_y, self._screen_x = self.stdscr.getmaxyx()

        self._ball = Ball(self)
        self._player = Player(self)

        self._gameobjects = []
        self.addObj(self._player)
        self.addObj(self._ball)

        self.lastTime = time.time()

    def draw(self):
        self.stdscr.erase()
        resize = curses.is_term_resized(self._screen_y, self._screen_x)
        if resize is True:
            self._screen_y, self._screen_x = self.stdscr.getmaxyx()
            self.stdscr.clear()
            curses.resizeterm(self._screen_y, self._screen_x)

        # DRAW MAP
        for i in range(self._screen_y - 1):
            self.stdscr.addstr(i, 0, str("||"))
            self.stdscr.addstr(i, self._screen_x - 3, str("||"))

        for i in range(self._screen_x - 1):
            self.stdscr.addstr(0, i, str("="))
            self.stdscr.addstr(self._screen_y - 1, i, str("="))

        # DRAW GAME ITSELF
        self.moveBall()
        for gameobject in self._gameobjects:
            gameobject.move()
            gameobject.draw(self.stdscr)

        self.stdscr.refresh()

    def handle_key(self, keychar):
        self._player.handle_key(keychar)

    def moveBall(self):
        if time.time() > self.lastTime + GameDefines._ballFPS:
            self._ball._xSpeed = self.pongSpeed
            self.lastTime = time.time()
            if self._ball._y > self._screen_y - 2:
                self.pongYSpeed = -1
            elif self._ball._y < 1:
                self.pongYSpeed = 1
            self._ball._ySpeed = self.pongYSpeed
            if self._ball._x > self._screen_x - 2:
                self.pongXSpeed = -1
            elif self._ball._x < 1:
                self.pongXSpeed = 1
            self._ball._xSpeed = self.pongXSpeed

    def addObj(self, new_object):
        self._gameobjects.append(new_object)
