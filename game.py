import curses

from player import Player
from walker import Walker


class Game:

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self._screen_y, self._screen_x = self.stdscr.getmaxyx()

        self._player = Player()
        self._walker = Walker(self._screen_y, self._screen_x)

    def draw(self):
        self.stdscr.erase()

        # HAS WINDOW BEEN RESIZED?
        resize = curses.is_term_resized(self._screen_y, self._screen_x)
        if resize is True:
            self._screen_y, self._screen_x = self.stdscr.getmaxyx()
            self.stdscr.clear()
            curses.resizeterm(self._screen_y, self._screen_x)

        # BORDERZ
        for i in range(self._screen_y - 1):
            self.stdscr.addstr(i, 0, str("||"))
            self.stdscr.addstr(i, self._screen_x - 3, str("||"))

        for i in range(self._screen_x - 1):
            self.stdscr.addstr(0, i, str("="))
            self.stdscr.addstr(self._screen_y - 1, i, str("="))
        # END BORDERZ

        self._walker.take_step(self.stdscr)
        # self._walker.check_edges(self.stdscr)
        self._walker.draw(self.stdscr)

        self.stdscr.refresh()

    def handle_key(self, keychar):
        self._player.handle_key(keychar)
