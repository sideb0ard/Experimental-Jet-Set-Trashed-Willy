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
    currentLevel = 1

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

        self.gobjects = []  # UNUSED FOR THE MOMENT

        self._wind = Vector(0.01, 0)
        self._gravity = Vector(0, 0.1)

        self.newLevel()

    def newLevel(self):
        self.initPlatforms(self.gamescr)
        self.initDoorways(self.gamescr)
        self._willy.reset()
        self._ball.reset()

    def nextLevel(self):
        gy, gx = self.gamescr.getmaxyx()
        self.initPlatforms(self.gamescr)
        for d in self.doorways:
            if self.doorways[d].x == 0:
                self.doorways[d].x = gx - 2
            else:
                self.doorways[d].x = 0
        if self._willy.location.x == 0:
            self._willy.location.x = gx - len(self._willy.shape)
        else:
            self._willy.location.x = 1
        self._ball.reset()

    def initDoorways(self, screen):
        y, x = screen.getmaxyx()
        self.doorways = {}
        for d in range(1):
            dx = 0 if randint(0, 1) == 0 else x - 2  # left or right side
            self.doorways[d] = Vector(randint(10, y - 10), dx)

    def initPlatforms(self, screen):
        y, x = screen.getmaxyx()
        self.platforms = {}
        for p in range(5):
            self.platforms[p] = Vector(randint(10, y - 10),
                                       randint(2, x - 11))

    def updateScore(self, screen):
        y, x = screen.getmaxyx()
        screen.addstr(1, 2, "LIVES:: {0}".format(self._willy.lives),
                      curses.color_pair(4))
        screen.addstr(1, (x // 2) - (len(self.score_msg.txt) // 2),
                      self.score_msg.txt, curses.color_pair(4))
        screen.addstr(1, x - 15, "SCORE:: {0}".format(self.score),
                      curses.color_pair(4))

    def checkInDoorway(self, vector):
        for d in self.doorways:
            if self.doorways[d].y <= vector.y < (self.doorways[d].y + 3) \
                    and self.doorways[d].x == int(vector.x):
                return True

    def drawBorders(self, screen):
        y, x = screen.getmaxyx()
        for i in range(y - 1):
            if self.checkInDoorway(Vector(i, 0)) is not True:
                screen.addstr(i, 0, str("|"))
            if self.checkInDoorway(Vector(i, x - 2)) is not True:
                screen.addstr(i, x - 2, str("|"))
        for i in range(x - 1):
            screen.addstr(0, i, str("="))
            screen.addstr(y - 1, i, str("="))

    def drawPlatforms(self, screen):
        y, x = screen.getmaxyx()
        for p in self.platforms:
            screen.addstr(self.platforms[p].y,
                          self.platforms[p].x, str("=========="),
                          curses.color_pair(5))

    def resize(self):
        # HAS WINDOW BEEN RESIZED?
        resize = curses.is_term_resized(self.screen_y, self.screen_x)
        if resize is True:
            self.screen_y, self.screen_x = self.stdscr.getmaxyx()
            self.stdscr.clear()
            curses.resizeterm(self.screen_y, self.screen_x)

    # MAIN LOOP HERE
    def draw(self):
        self.gamescr.erase()
        self.scorescr.erase()
        self.resize()

        self.drawBorders(self.gamescr)
        self.drawBorders(self.scorescr)

        self.drawPlatforms(self.gamescr)
        self.updateScore(self.scorescr)

        # self._ball.applyForce(self._wind)
        # self._ball.applyForce(self._gravity)
        ballHitsPlatform = self.checkPlatform(self._ball)
        self._ball.update(self.gamescr, self._willy, ballHitsPlatform)
        self._ball.draw(self.gamescr)

        if self.checkInDoorway(self._willy.location):
            self.score_msg.update("MAGIC WURLD!!!!")
            self.score_msg.timedUpdate(3, self.gname)
            self.currentLevel += 1
            self.nextLevel()

        willyOnPlatform = self.checkPlatform(self._willy)
        self._willy.update(self.gamescr, willyOnPlatform)
        self._willy.draw(self.gamescr)

        self.checkCollisions(self._willy, self._ball)

        self.gamescr.noutrefresh()
        self.scorescr.noutrefresh()
        curses.doupdate()

    def checkPlatform(self, gobject):
        for p in self.platforms:
            # print 'gobjectY:{0} / pY:{1}'.format(gobject.location.y,
            #                                      self.platforms[p].y - 1)
            if int(gobject.location.y) == ((self.platforms[p].y) or
                                           (self.platforms[p].y + 2)):
                if ((self.platforms[p].x - 2) <= gobject.location.x) and \
                   gobject.location.x <= (self.platforms[p].x + 10):
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
                b.spent = True
            if self.checkPlatform(b):
                b.spent = True

    def handle_key(self, keychar):
        self._player.handle_key(keychar, self._willy, self.gamescr)

    def addGobj(self, new_object):
        self.gobjects.append(new_object)
