import curses
import time
from vector import Vector


class Gobject():

        FPS = 0.04

        def __init__(self, height, width):

            self.location = Vector(2, width // 2)
            self.velocity = Vector(0, 0)
            self.acceleration = Vector(0.01, 0.01)
            self.topspeed = 1
            self.mass = 1
            self.last_time = time.time()

        def update(self, stdscr):
            if time.time() > self.last_time + self.FPS:
                self.last_time = time.time()

                height, width = stdscr.getmaxyx()

                next_x = self.location.x + self._velocity.x
                if next_x >= width - 2 or next_x < 1:
                    self._velocity.x *= -1
                else:
                    self.location.x += self._velocity.x

                next_y = self.location.y + self._velocity.y
                if next_y >= height or next_y < 1:
                    self._velocity.y *= -1
                else:
                    self.location.y += self._velocity.y

        def checkBorder(self, stdscr):
            height, width = stdscr.getmaxyx()
            if self.location.y > height - 2:
                self.location.y = height - 2
            elif self.location.y < 2:
                self.location.y = 2

            if self.location.x > ((width - 3) - len(self.shape)):
                self.location.x = ((width - 3) - len(self.shape))
                self.velocity.x *= -1
                # self.direction = 1 - self.direction  # binary flip
            elif self.location.x < 2:
                self.location.x = 2
                self.velocity.x *= -1
                # self.direction = 1 - self.direction  # binary flip

        def draw(self, stdscr):
            self.checkBorder(stdscr)
            try:
                stdscr.addstr(int(self.location.y),
                              int(self.location.x),
                              self._shape, curses.color_pair(1))
            except Exception, e:
                print 'y:{0}/x:{1}/{2}||{3}'.format(self.location.y,
                                                    self.location.x, e,
                                                    stdscr.getmaxyx())
