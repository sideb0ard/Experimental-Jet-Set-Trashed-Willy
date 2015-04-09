import copy
import curses
import time
import threading
from random import randint
from vector import Vector


class Ball():

        shape = '*'
        _FPS = 0.04
        bouncing = 0

        def __init__(self, screen):
            self.height, self.width = screen.getmaxyx()
            self.screen = screen

            self.location = Vector(2, randint(0, self.width))
            self._velocity = Vector(0, 0)
            self._acceleration = Vector(0.01, 0.01)
            self._topspeed = 1
            self._mass = 1

            self.last_time = time.time()

        def reset(self):
            height, width = self.screen.getmaxyx()
            self.location = Vector(2, randint(0, width))

        def timedBounceRelease(self, secondsToWait):
            time.sleep(secondsToWait)
            self.bouncing = 0

        def bounceRelease(self, secondsToWait):
            t = threading.Thread(target=self.timedBounceRelease,
                                 args=(secondsToWait,))
            t.start()

        def update(self, screen, willy, bounce=None):
            if time.time() > self.last_time + self._FPS:
                self.last_time = time.time()

                height, width = screen.getmaxyx()

                if bounce:
                    self.bouncing = 1
                    self.bounceRelease(1)
                    self._velocity.y *= -1
                elif self.bouncing == 1:
                    pass
                else:
                    direction = Vector(willy.location.y - self.location.y,
                                       willy.location.x - self.location.x)
                    direction.normalize()
                    direction.mult(0.2)
                    self._velocity = direction

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
            elif self.location.x < 2:
                self.location.x = 2

        def draw(self, screen):
            self.checkBorder(screen)
            try:
                screen.addstr(int(self.location.y),
                              int(self.location.x),
                              self.shape, curses.color_pair(1))
            except Exception, e:
                print 'BALL:: y:{0}/x:{1}/{2}||{3}'.format(self.location.y,
                                                           self.location.x, e,
                                                           screen.getmaxyx())
