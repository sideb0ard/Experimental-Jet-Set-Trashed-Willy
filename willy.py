import curses
import time
from bullet import Bullet
from soundplayrrr import Fire, Jump
from vector import Vector


class Willy():

        shape = '<o>'
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
                b.update(screen)
            if time.time() > self.last_time + self._FPS:
                self.last_time = time.time()
                height, width = screen.getmaxyx()
                if self.direction == 0:
                    self.location.x -= self.velocity.x
                if self.direction == 1:
                    self.location.x += self.velocity.x
                if grounded is None:
                    if self.location.y < height - 2:
                        self.location.y += 1
                else:
                    pass

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
                    b.draw(screen)

                for yy, line in enumerate(self.shape.splitlines(),
                                          self.location.y):
                    screen.addstr(yy, self.location.x,
                                  line, curses.color_pair(2))
            except Exception, e:
                print 'y:{0} / x:{1} / {2} || {3}'.format(self.location.y,
                                                          self.location.x, e,
                                                          screen.getmaxyx())
