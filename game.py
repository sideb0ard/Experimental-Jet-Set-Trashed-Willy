import curses
from random import randint

from player import Player
from ball import Ball
from willy import Willy
from soundplayrrr import Hit
from vector import Vector


class Game:

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self._screen_y, self._screen_x = self.stdscr.getmaxyx()

        self._player = Player()
        self._ball = Ball(self._screen_y, self._screen_x)
        self._willy = Willy(self._screen_y, self._screen_x)

        self.initPlatforms()
        self.gobjects = []

        self._wind = Vector(0.01, 0)
        self._gravity = Vector(0, 0.1)

    def initPlatforms(self):
        self.platforms = {}
        for p in range(5):
            self.platforms[p] = Vector(randint(10, self._screen_y - 10),
                                       randint(4, self._screen_x - 10))

    def drawBorders(self):
        for i in range(self._screen_y - 1):
            self.stdscr.addstr(i, 0, str("||"))
            self.stdscr.addstr(i, self._screen_x - 3, str("||"))
        for i in range(self._screen_x - 1):
            self.stdscr.addstr(0, i, str("="))
            self.stdscr.addstr(self._screen_y - 1, i, str("="))

    def drawPlatforms(self):
        for p in self.platforms:
            self.stdscr.addstr(self.platforms[p].y,
                               self.platforms[p].x, str("====="))

    def resize(self):
        # HAS WINDOW BEEN RESIZED?
        resize = curses.is_term_resized(self._screen_y, self._screen_x)
        if resize is True:
            self._screen_y, self._screen_x = self.stdscr.getmaxyx()
            self.stdscr.clear()
            curses.resizeterm(self._screen_y, self._screen_x)

    def draw(self):
        self.stdscr.erase()
        self.resize()
        self.drawBorders()
        self.drawPlatforms()

        self._ball.applyForce(self._wind)
        # self._ball.applyForce(self._gravity)

        self._ball.update(self.stdscr, self._willy)
        self._ball.draw(self.stdscr)

        willyOnFloor = self.checkFloors(self._willy, self.platforms)
        self._willy.update(self.stdscr, willyOnFloor)
        self._willy.draw(self.stdscr)

        self.checkCollisions(self._willy, self._ball, self.stdscr)

        self.stdscr.refresh()

    def checkFloors(self, willy, platforms):
        for p in platforms:
            if willy.location.y == (platforms[p].y - 1):
                if ((platforms[p].x - 2) <= willy.location.x) and \
                   (willy.location.x + len(willy.shape) <=
                   (platforms[p].x + 7)):
                    return True

    def checkCollisions(self, willy, ball, stdscr):
        if ball.location.checkCollide(willy.location):
            # print "DEID!"
            pass
        for b in willy.bullets:
            if b.location.checkCollide(ball.location):
                s = Hit()
                s.start()
                ball.reset(self.stdscr)

    def handle_key(self, keychar):
        self._player.handle_key(keychar, self._willy)

    def addGobj(self, new_object):
        self.gobjects.append(new_object)
