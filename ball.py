import curses
import logging
import time
from vector import Vector

logger = logging.getLogger('ball')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('./bouncyball.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s ' +
                              '- %(levelname)s - %(message)s')

fh.setFormatter(formatter)
logger.addHandler(fh)


class Ball():

        _shape = '*'
        _FPS = 0.04

        def __init__(self, height, width):

            self._location = Vector(height // 2, width // 2)
            # self._location = Vector(height - 1, width - 2)
            self._velocity = Vector(0, 0)
            self._acceleration = Vector(0.01, 0.01)
            self._topspeed = 1

            curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
            self.last_time = time.time()

        def take_step(self, stdscr, willy):
            if time.time() > self.last_time + self._FPS:
                self.last_time = time.time()

                height, width = stdscr.getmaxyx()

                direction = Vector(willy._location.y - self._location.y,
                                   willy._location.x - self._location.x)
                direction.normalize()
                direction.mult(0.2)

                self._velocity = direction

                next_x = self._location.x + self._velocity.x
                if next_x >= width - 2 or next_x < 1:
                    self._velocity.x *= -1
                else:
                    self._location.x += self._velocity.x

                next_y = self._location.y + self._velocity.y
                if next_y >= height or next_y < 1:
                    self._velocity.y *= -1
                else:
                    self._location.y += self._velocity.y

                logger.info('Location x - {0}'.format(int(self._location.x)))
                logger.info('Location y - {0}'.format(int(self._location.y)))
                logger.info('A x:{0} y:{1}'.format(self._acceleration.x,
                                                   self._acceleration.y))
                logger.info('V x:{0} y:{1}'.format(self._velocity.x,
                                                   self._velocity.y))

        def draw(self, stdscr):
            try:
                stdscr.addstr(int(self._location.y),
                              int(self._location.x),
                              self._shape, curses.color_pair(1))
            except Exception, e:
                logger.info('y:{0}/x:{1}/{2}||{3}'.format(self._location.y,
                                                          self._location.x, e,
                                                          stdscr.getmaxyx()))
