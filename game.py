import curses
from random import randint

from ball import Ball
from player import Player
from soundplayrrr import Bump, Hit
from vector import Vector
from willy import Willy


class Game:

    score_size = 3

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.screen_y, self.screen_x = self.stdscr.getmaxyx()
        self.gamescr = curses.newwin(self.screen_y - self.score_size,
                                     self.screen_x,
                                     0, 0)
        self.scorescr = curses.newwin(self.score_size, self.screen_x,
                                      self.screen_y - self.score_size, 0)
        self._player = Player()
        self._ball = Ball(self.gamescr)
        self._willy = Willy(self.gamescr)

        self.initPlatforms()
        self.gobjects = []

        self._wind = Vector(0.01, 0)
        self._gravity = Vector(0, 0.1)

    def initPlatforms(self):
        self.platforms = {}
        for p in range(5):
            self.platforms[p] = Vector(randint(10, self.screen_y - 10),
                                       randint(4, self.screen_x - 10))

    def updateScore(self, screen):
        screen.addstr(1, 2, "LIVES:: {0}".format(self._willy.lives))

    def drawBorders(self, screen):
        y, x = screen.getmaxyx()
        for i in range(y - 1):
            screen.addstr(i, 0, str("|"))
            screen.addstr(i, x - 3, str("|"))
        for i in range(x - 1):
            screen.addstr(0, i, str("="))
            screen.addstr(y - 1, i, str("="))

    def drawPlatforms(self, screen):
        y, x = screen.getmaxyx()
        for p in self.platforms:
            screen.addstr(self.platforms[p].y,
                          self.platforms[p].x, str("====="))

    def resize(self):
        # HAS WINDOW BEEN RESIZED?
        resize = curses.is_term_resized(self.screen_y, self.screen_x)
        if resize is True:
            self.screen_y, self.screen_x = self.stdscr.getmaxyx()
            self.stdscr.clear()
            curses.resizeterm(self.screen_y, self.screen_x)

    def draw(self):
        self.gamescr.erase()
        self.scorescr.erase()
        self.resize()
        self.drawBorders(self.gamescr)
        self.drawBorders(self.scorescr)
        self.drawPlatforms(self.gamescr)

        self.updateScore(self.scorescr)

        self._ball.applyForce(self._wind)
        # self._ball.applyForce(self._gravity)

        self._ball.update(self.gamescr, self._willy)
        self._ball.draw(self.gamescr)

        willyOnFloor = self.checkFloors(self._willy, self.platforms)
        self._willy.update(self.gamescr, willyOnFloor)
        self._willy.draw(self.gamescr)

        self.checkCollisions(self._willy, self._ball)

        # self.stdscr.refresh()
        self.gamescr.noutrefresh()
        self.scorescr.noutrefresh()
        curses.doupdate()

    def checkFloors(self, willy, platforms):
        for p in platforms:
            if willy.location.y == (platforms[p].y - 1):
                if ((platforms[p].x - 2) <= willy.location.x) and \
                   (willy.location.x + len(willy.shape) <=
                   (platforms[p].x + 7)):
                    return True

    def checkCollisions(self, willy, ball):
        if ball.location.checkCollide(willy.location):
            s = Bump()
            s.start()
            willy.lives -= 1
            willy.reset()
            ball.reset()
        for b in willy.bullets:
            if b.location.checkCollide(ball.location):
                s = Hit()
                s.start()
                ball.reset()

    def handle_key(self, keychar):
        self._player.handle_key(keychar, self._willy)

    def addGobj(self, new_object):
        self.gobjects.append(new_object)
