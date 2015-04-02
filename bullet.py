import curses
import time
from vector import Vector
from gobject import Gobject


class Bullet(Gobject):

        FPS = 0.01
        # shape = '0'

        def __init__(self, y, x):

            self.location = Vector(y, x)
            self.velocity = Vector(-1, 0)
            self.acceleration = Vector(0.01, -0.01)
            self.topspeed = 1
            self.mass = 1
            self.last_time = time.time()
            self.drawMe = True
            curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
            self.shape = curses.ACS_DEGREE

        def update(self, stdscr):
            if time.time() > self.last_time + self.FPS:
                self.last_time = time.time()
                self.location.y += self.velocity.y

        def checkBorder(self, stdscr):
            height, width = stdscr.getmaxyx()
            if self.location.y > height - 2:
                self.location.y = height - 2
            elif self.location.y < 2:
                self.drawMe = False

            if self.location.x > width - 3:
                self.location.x = width - 3
                self.velocity.x *= -1
            elif self.location.x < 2:
                self.location.x = 2
                self.velocity.x *= -1

        def draw(self, stdscr):
            self.checkBorder(stdscr)
            if self.drawMe is True:
                try:
                    stdscr.addch(int(self.location.y),
                                 int(self.location.x),
                                 self.shape, curses.color_pair(3))
                except Exception, e:
                    print 'Error:{0} - x:{1},y:{2}'.format(e,
                                                           self.location.x,
                                                           self.location.y)
