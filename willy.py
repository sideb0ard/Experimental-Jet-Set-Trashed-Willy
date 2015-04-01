import curses
import logging
import time
from vector import Vector

logger = logging.getLogger('willy')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('./ewilly.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s ' +
                              '- %(levelname)s - %(message)s')

fh.setFormatter(formatter)
logger.addHandler(fh)


class Willy():

        shape = '<O>'
        _FPS = 0.02

        def __init__(self, height, width):

            self._location = Vector(height - 2, 10)
            self._velocity = Vector(0, 0)
            self._topspeed = 2
            self._jumping = False

            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            # self.shape = curses.ACS_DEGREE
            self.last_time = time.time()

        def jump(self):
            self._location.y = 5

        def update(self, stdscr):
            if time.time() > self.last_time + self._FPS:
                self.last_time = time.time()
                height, width = stdscr.getmaxyx()
                # logger.info('Location x - {0}'.format(int(self._location.x)))
                # logger.info('Location y - {0}'.format(int(self._location.y)))
                if self._location.y < height - 2:
                    self._location.y += 1

        def check_edges(self, stdscr):
            height, width = stdscr.getmaxyx()
            if self._location.y > height - 1:
                self._location.y -= 1
            elif self._location.y < 0:
                self._location.y += 1

            if self._location.x > width - 1:
                self._location.x -= 1
            elif self._location.x < 0:
                self._location.x += 1

        def draw(self, stdscr):
            try:
                for yy, line in enumerate(self.shape.splitlines(),
                                          self._location.y):
                    stdscr.addstr(yy, self._location.x,
                                  line, curses.color_pair(2))
            except Exception, e:
                print 'y:{0} / x:{1} / {2} || {3}'.format(self._location.y,
                                                          self._location.x, e,
                                                          stdscr.getmaxyx())
