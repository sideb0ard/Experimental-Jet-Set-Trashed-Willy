import curses
import logging
import time
from bullet import Bullet
from soundplayrrr import Fire, Jump
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
        direction = 0  # 0 = left, 1 = right
        _FPS = 0.02
        gravity = 0.5
        lives = 3
        bullets = []

        def __init__(self, screen):

            self.screen = screen
            height, width = screen.getmaxyx()
            self.location = Vector(height - 2, width // 2)
            self.velocity = Vector(1, 1)
            self._topspeed = 2
            self._jumping = False

            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            # self.shape = curses.ACS_DEGREE
            self.last_time = time.time()

        def reset(self):
            height, width = self.screen.getmaxyx()
            self.location = Vector(height - 2, width // 2)

        def fire(self):
            bully = Bullet(self.location.y, self.location.x)
            self.bullets.append(bully)
            f = Fire()
            f.start()

        def jump(self):
            self.location.y = 5
            j = Jump()  # sound
            j.start()
            if self.direction == 1:  # right
                self.location.x += 10
            elif self.direction == 0:  # left
                self.location.x -= 10

        def update(self, screen, grounded=None):
            for b in self.bullets:
                # logger.info('Bullt {0}'.format(b))
                b.update(screen)
            if time.time() > self.last_time + self._FPS:
                self.last_time = time.time()
                height, width = screen.getmaxyx()
                # logger.info('Loc:{0},{1} / dir: {2}'.format(self.location.x,
                #                                             self.location.y,
                #                                             self.direction))
                # logger.info('Location y - {0}'.format(int(self.location.y)))
                if self.direction == 0:
                    self.location.x -= self.velocity.x
                if self.direction == 1:
                    self.location.x += self.velocity.x
                # self.location.y += self.gravity
                if grounded is None:
                    if self.location.y < height - 2:
                        self.location.y += 1
                else:
                    pass
                    # b = Bump()
                    # b.start()

        def checkBorder(self, screen):

            height, width = screen.getmaxyx()

            if self.location.y > height - 2:
                self.location.y = height - 2
            elif self.location.y < 2:
                self.location.y = 2

            if self.location.x > ((width - 3) - len(self.shape)):
                self.location.x = ((width - 3) - len(self.shape))
                self.velocity.x *= -1
            elif self.location.x < 1:
                self.location.x = 1
                self.velocity.x *= -1

        def draw(self, screen):
            self.checkBorder(screen)
            try:
                for b in self.bullets:
                    # logger.info('Bullt {0}'.format(b))
                    # b.update(screen)
                    b.draw(screen)

                for yy, line in enumerate(self.shape.splitlines(),
                                          self.location.y):
                    screen.addstr(yy, self.location.x,
                                  line, curses.color_pair(2))
            except Exception, e:
                print 'y:{0} / x:{1} / {2} || {3}'.format(self.location.y,
                                                          self.location.x, e,
                                                          screen.getmaxyx())
