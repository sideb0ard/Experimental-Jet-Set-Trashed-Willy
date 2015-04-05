import curses
import traceback

from game import Game
from soundplayrrr import BeatLoop


def runner(stdscr):

    stdscr.timeout(0)
    stdscr.nodelay(1)
    curses.nl()
    curses.curs_set(0)
    game = Game(stdscr)
    game.draw()

    # m = BeatLoop()  # music loop
    # m.setDaemon(True)
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
