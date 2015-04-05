import curses
import traceback

from game import Game
from soundplayrrr import IntroLoop


def runner(stdscr):

    stdscr.timeout(0)
    stdscr.nodelay(1)
    curses.nl()
    curses.curs_set(0)
    game = Game(stdscr)
    game.draw()

    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
    # m = IntroLoop()  # music loop
    # m.start()

    while True:
        ch = stdscr.getch()
        if ch == ord('q') or ch == ord('Q'):
            return 0
        else:
            game.handle_key(ch)
        game.draw()

if __name__ == '__main__':
    try:
        curses.wrapper(runner)
    except:
        traceback.print_exc()
