import copy
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

        def __init__(self, screen):
            self.height, self.width = screen.getmaxyx()
            self.screen = screen

            self.location = Vector(2, self.width // 2)
            self._velocity = Vector(0, 0)
            self._acceleration = Vector(0.01, 0.01)
            self._topspeed = 1
            self._mass = 1

            curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
            self.last_time = time.time()

        def reset(self):
            height, width = self.screen.getmaxyx()
            self.location = Vector(2, width // 2)

        def update(self, screen, willy):
            if time.time() > self.last_time + self._FPS:
                self.last_time = time.time()

                height, width = screen.getmaxyx()

                direction = Vector(willy.location.y - self.location.y,
                                   willy.location.x - self.location.x)
                direction.normalize()
                direction.mult(0.2)

                self._velocity = direction
                # self._velocity.add(self._acceleration)

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

                # logger.info('Location x - {0}'.format(int(self.location.x)))
                # logger.info('Location y - {0}'.format(int(self.location.y)))
                # logger.info('A x:{0} y:{1}'.format(self._acceleration.x,
                #                                    self._acceleration.y))
                # logger.info('V x:{0} y:{1}'.format(self._velocity.x,
                #                                    self._velocity.y))

                # self._acceleration.mult(0)

        def applyForce(self, force):
            f = copy.copy(force)
            f.div(self._mass)
            self._acceleration.add(f)

        def checkBorder(self, screen):
            height, width = screen.getmaxyx()
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

        def draw(self, screen):
            try:
                screen.addstr(int(self.location.y),
                              int(self.location.x),
                              self._shape, curses.color_pair(1))
            except Exception, e:
                logger.info('y:{0}/x:{1}/{2}||{3}'.format(self.location.y,
                                                          self.location.x, e,
                                                          screen.getmaxyx()))
