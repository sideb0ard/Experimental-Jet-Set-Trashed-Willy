import curses
import math
import time
import threading
from bullet import Bullet
from soundplayrrr import Fire
from vector import Vector


class Willy():

        shape = '<o>'
        directionUpDown = 0
        directionLeftRight = 0
        _FPS = 0.02
        gravity = 0.2
        lives = 3
        bullets = []
        jumping = False
        onGround = False

        def __init__(self, screen):

            self.screen = screen
            height, width = screen.getmaxyx()
            self.location = Vector(height - 2, width // 2)
            self.velocity = Vector(0, 1)
            self._topspeed = 2
            self._jumping = False
            self.last_time = time.time()

        def reset(self):
            height, width = self.screen.getmaxyx()
            self.location = Vector(height - 2, width // 2)

        def fire(self):
            bully = Bullet(self.location.y, self.location.x)
            self.bullets.append(bully)
            f = Fire()
            f.start()

        def jumpFinish(self, secondsToWait):
            time.sleep(secondsToWait)
            if self.velocity.y < -6:
                self.velocity.y = -6
            # self.jumping = False
            # self.velocity.x *= -0.5
            # self.velocity.y = 0

        def timedJump(self, secondsToWait):
            t = threading.Thread(target=self.jumpFinish, args=(secondsToWait,))
            t.start()

        def jump(self):
            if self.onGround is True:
                self.velocity.y = (-2.45 * abs(self.velocity.x))
                self.onGround = False
            # self.jumping = True
            self.timedJump(0)

        def update(self, screen, grounded=None):
            for b in self.bullets:
                b.update(screen)
            if time.time() > self.last_time + self._FPS:
                self.last_time = time.time()
                height, width = screen.getmaxyx()

                self.velocity.y += self.gravity
                if grounded:
                    self.onGround = True
                    self.velocity.y = 0
                else:
                    self.location.y += self.velocity.y

                if self.velocity.x >= 1:
                    self.velocity.x = 1
                elif self.velocity.x <= -1:
                    self.velocity.x = -1

                self.location.x += self.velocity.x

                if self.location.y > height - 2:
                    self.location.y = height - 2
                    self.velocity.y = 0
                    self.onGround = True

        def checkBorder(self, screen):

            height, width = screen.getmaxyx()

            if self.location.y > height - 2:
                self.location.y = height - 2
                self.velocity.y = 0
            elif self.location.y < 2:
                self.location.y = 1
                # self.velocity.y *= -1

            if self.location.x > (width - len(self.shape)):
                self.location.x = (width - len(self.shape))
                self.velocity.x *= -1
            elif self.location.x < 0:
                self.location.x = 0
                self.velocity.x *= -1

        def draw(self, screen):
            self.checkBorder(screen)
            try:
                for b in self.bullets:
                    b.draw(screen)

                for yy, line in enumerate(self.shape.splitlines(),
                                          int(math.floor(self.location.y))):
                    screen.addstr(yy, int(math.floor(self.location.x)),
                                  line, curses.color_pair(2))
            except Exception, e:
                print 'y:{0} / x:{1} / {2} || {3}'.format(self.location.y,
                                                          self.location.x, e,
                                                          screen.getmaxyx())
