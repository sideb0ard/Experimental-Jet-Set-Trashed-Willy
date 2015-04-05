import curses
import math
import time
import threading
from bullet import Bullet
from soundplayrrr import Fire, Whoosh1
from vector import Vector


class Willy():

        shape = '<o>'
        directionUpDown = 0  
        directionLeftRight = 0
        _FPS = 0.01
        gravity = 0.5
        lives = 3
        bullets = []
        jumping = False

        def __init__(self, screen):

            self.screen = screen
            height, width = screen.getmaxyx()
            self.location = Vector(height - 2, width // 2)
            self.velocity = Vector(0.5, 0.5)
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
            self.jumping = False

        def timedJump(self, secondsToWait):
            t = threading.Thread(target=self.jumpFinish, args=(secondsToWait,))
            t.start()

        def jump(self):
            self.jumping = True
            self.timedJump(0.5)
            # self.location.y = 5
            j = Whoosh1()  # sound
            j.start()
            # if self.direction == 1:  # right
            #    self.location.x += 10
            # elif self.direction == 0:  # left
            #    self.location.x -= 10

        def update(self, screen, grounded=None):
            for b in self.bullets:
                b.update(screen)
            if time.time() > self.last_time + self._FPS:
                self.last_time = time.time()
                if grounded:
                    self.velocity.y *= -1

                if self.directionUpDown == 0:
                    self.location.y -= self.gravity  # up
                elif self.directionUpDown == 1:
                    self.location.y += self.gravity  # down

                if self.directionLeftRight == 0:  # left
                    self.location.x -= self.gravity
                elif self.directionLeftRight == 1:  # right
                    self.location.x += self.gravity

                # if self.jumping is True:
                #     self.location.y -= 1
                # elif grounded is None:
                #     if self.location.y < height - 2:
                #         self.location.y += 1

        def checkBorder(self, screen):

            height, width = screen.getmaxyx()

            if self.location.y > height - 2:
                self.location.y = height - 2
            elif self.location.y < 2:
                self.location.y = 1

            if self.location.x > (width - len(self.shape)):
                self.location.x = (width - len(self.shape))
                self.velocity.x *= -2
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
