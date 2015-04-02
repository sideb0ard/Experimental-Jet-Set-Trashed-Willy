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
        direction = None
        _FPS = 0.02
        gravity = 0.5

        def __init__(self, height, width):

            # self.location = Vector(height - 2, 10)
            self.location = Vector(height // 2, 10)
            self.velocity = Vector(1, 1)
            self._topspeed = 2
            self._jumping = False

            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            # self.shape = curses.ACS_DEGREE
            self.last_time = time.time()

        def jump(self):
            self.location.y = 5
            if self.direction == 'RIGHT':
                self.location.x += 15
            elif self.direction == 'LEFT':
                self.location.x -= 15

        def update(self, stdscr):
            if time.time() > self.last_time + self._FPS:
                self.last_time = time.time()
                height, width = stdscr.getmaxyx()
                logger.info('Loc:{0},{1} / dir: {2}'.format(self.location.x,
                                                            self.location.y,
                                                            self.direction))
                # logger.info('Location y - {0}'.format(int(self.location.y)))
                if self.direction == 'LEFT':
                    self.location.x -= self.velocity.x
                if self.direction == 'RIGHT':
                    self.location.x += self.velocity.x
                # self.location.y += self.gravity
                if self.location.y < height - 2:
                    self.location.y += 1

        def checkBorder(self, stdscr):
            height, width = stdscr.getmaxyx()
            if self.location.y > height - 2:
                self.location.y = height - 2
            elif self.location.y < 2:
                self.location.y = 2

            if self.location.x > ((width - 3) - len(self.shape)):
                self.location.x = ((width - 3) - len(self.shape))
            elif self.location.x < 2:
                self.location.x = 2

        def draw(self, stdscr):
            self.checkBorder(stdscr)
            try:
                for yy, line in enumerate(self.shape.splitlines(),
                                          self.location.y):
                    stdscr.addstr(yy, self.location.x,
                                  line, curses.color_pair(2))
            except Exception, e:
                print 'y:{0} / x:{1} / {2} || {3}'.format(self.location.y,
                                                          self.location.x, e,
                                                          stdscr.getmaxyx())
