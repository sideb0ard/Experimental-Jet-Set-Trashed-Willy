import curses
import random
import time
from vector import Vector


class Walker():

        _shape = '*'
        _FPS = 0.1

        def __init__(self, height, width):

            self._location = Vector(height // 2, width // 2)
            self._velocity = Vector(1, 1)
            self._acceleration = Vector(0.015, 0.015)

            curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
            self.last_time = time.time()

        def take_step(self, stdscr):
            if time.time() > self.last_time + self._FPS:
                self.last_time = time.time()

                # self._velocity.add(self._acceleration)
                self._velocity.add(Vector(random.random(), random.random()))
                self._location.add(self._velocity)

        def check_edges(self, stdscr):
                scr_y, scr_x = stdscr.getmaxyx()
                if self._location.y > scr_y - 2:
                    self._location.y = 0
                elif self._location.y < 0:
                    self._location.y = scr_y - 2

                if self._location.x > scr_x - 2:
                    self._location.x = 0
                elif self._location.x < 0:
                    self._location.x = 0

        def draw(self, stdscr):
            try:
                stdscr.addstr(int(self._location.y),
                              int(self._location.x),
                              self._shape, curses.color_pair(1))
            except Exception, e:
                print 'y:{0} / x:{1} / {2} || {3}'.format(self._location.y,
                                                          self._location.x, e,
                                                          stdscr.getmaxyx())
