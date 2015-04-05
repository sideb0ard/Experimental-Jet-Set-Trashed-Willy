import curses
from random import randint

from ball import Ball
from player import Player
from soundplayrrr import Bump, Hit
from message import Message
from vector import Vector
from willy import Willy


class Game:

    score_size = 3
    score = 0
    gname = "JETSET TRASHED WILLY!!"

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

        self.score_msg = Message(self.gname)

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
        y, x = screen.getmaxyx()
        screen.addstr(1, 2, "LIVES:: {0}".format(self._willy.lives),
                      curses.color_pair(4))
        screen.addstr(1, (x // 2) - (len(self.score_msg.txt) // 2),
                      self.score_msg.txt, curses.color_pair(4))
        screen.addstr(1, x - 15, "SCORE:: {0}".format(self.score),
                      curses.color_pair(4))

    def drawBorders(self, screen):
        y, x = screen.getmaxyx()
        for i in range(y - 1):
            screen.addstr(i, 0, str("|"))
            screen.addstr(i, x - 2, str("|"))
        for i in range(x - 1):
            screen.addstr(0, i, str("="))
            screen.addstr(y - 1, i, str("="))

    def drawPlatforms(self, screen):
        y, x = screen.getmaxyx()
        for p in self.platforms:
            screen.addstr(self.platforms[p].y,
                          self.platforms[p].x, str("====="),
                          curses.color_pair(5))

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
        ballHitsPlatform = self.checkPlatform(self._ball)
        self._ball.update(self.gamescr, self._willy, ballHitsPlatform)
        self._ball.draw(self.gamescr)

        willyOnPlatform = self.checkPlatform(self._willy)
        self._willy.update(self.gamescr, willyOnPlatform)
        self._willy.draw(self.gamescr)

        self.checkCollisions(self._willy, self._ball)

        self.gamescr.noutrefresh()
        self.scorescr.noutrefresh()
        curses.doupdate()

    def checkPlatform(self, gobject):
        for p in self.platforms:
            if gobject.location.y == (self.platforms[p].y - 1):
                if ((self.platforms[p].x - 2) <= gobject.location.x) and \
                   (gobject.location.x + len(gobject.shape) <=
                   (self.platforms[p].x + 7)):
                    self.score_msg.update("BINK!")
                    self.score_msg.timedUpdate(1, self.gname)
                    return True

    def checkCollisions(self, willy, ball):
        if ball.location.checkCollide(willy.location):
            s = Bump()
            s.start()
            willy.lives -= 1
            willy.reset()
            ball.reset()
            self.score_msg.update("SCHMUCK! YOU DIED!!")
            self.score_msg.timedUpdate(3, self.gname)
        for b in willy.bullets:
            if b.location.checkCollide(ball.location):
                s = Hit()
                s.start()
                self.score += 1
                ball.reset()

    def handle_key(self, keychar):
        self._player.handle_key(keychar, self._willy)

    def addGobj(self, new_object):
        self.gobjects.append(new_object)
