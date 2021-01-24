import sys
import configparser

# This is the configuration file
myConfig = configparser.ConfigParser()
myConfig.read("settings.ini")

# number of tiles (for both rows and columns)
BSIZE = int(myConfig['Constants']['board_size'])

# the maximum search depth. on standard 3 x 3 board, should be set to 9.
# however if you increase the board size, you will need to decrease the search depth.
MAX_DEPTH = int(myConfig['Constants']['max_search_depth'])

# making the board.
board = [0] * BSIZE
bdimm = len(board)
for _ in range(bdimm):
    board[_] = [0] * BSIZE

display_w = display_h = int(myConfig['Constants']['display_size'])  # size of the display
cube_size = display_w / BSIZE  # the size of each cube

# infinities used for minimax
INF = sys.maxsize
NEG_INF = -(sys.maxsize - 1)

# color rgb values
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
