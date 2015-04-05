import curses


class Field():

    score_size = 3

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.screen_y, self.screen_x = self.stdscr.getmaxyx()
        self.gamescr = curses.newwin(self.screen_y - self.score_size,
                                     self.screen_x,
                                     0, 0)
        self.scorescr = curses.newwin(self.score_size, self.screen_x,
                                      self.screen_y - self.score_size, 0)
