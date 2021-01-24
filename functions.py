from c import *
import copy
import pygame


def row_and_open_check(myBoard, row):
    ttl = 0
    free = False
    for j in range(bdimm):
        if myBoard[row][j] == 0:
            free = True
            break  # if there is an opening, there is no victor.
        else:
            ttl += myBoard[row][j]
    else:
        if ttl == bdimm:
            return 1, free
        elif ttl == -bdimm:
            return -1, free
        else:
            return 0, free

    return 0, free


def col_check(myBoard, col):
    ttl = 0
    for i in range(bdimm):
        ttl += myBoard[i][col]

    if ttl == bdimm:
        return 1
    elif ttl == -bdimm:
        return -1
    else:
        return 0


# checks the board, and sees if someone has won.
def evaluate(myBoard):
    # walk along main diagonal, check rows and columns as you go.
    w1 = 0
    w2 = bdimm - 1
    maind = 0
    minord = 0
    opening = False
    while w1 < bdimm:

        # first checking given row
        res, free = row_and_open_check(myBoard, w1)

        if free:
            opening = True

        # if the tile is zero, there can be no winner in the row or column or main diagonal.
        if myBoard[w1][w1] == 0:
            minord += myBoard[w1][w2]  # keeping track of minor diagonal as we go.
            w1 += 1
            w2 -= 1
            continue
        else:

            # this is still the row result
            if res != 0:
                return res

            # now checking given column
            res = col_check(myBoard, w1)

            if res != 0:
                return res

            # adding main diagonal, then minor diagonal.
            maind += myBoard[w1][w1]
            minord += myBoard[w1][w2]
            w1 += 1
            w2 -= 1

    # now checking main and minor sums
    if maind == bdimm:
        return 1
    elif maind == -bdimm:
        return -1

    elif minord == bdimm:
        return 1
    elif minord == -bdimm:
        return -1

    # if we reach this point, and there is no winner, and there is an opening
    # the game is not decided yet.
    if opening:
        return None

    # however, if we reach this point, and there is no winner, and there isn't an opening
    # then the game is drawn.
    else:
        return 0


# recursively plays the game, keeping track of important values.
# returns the current evaluation for the board state.
# the greater the number, the more likely x wins.
# the smaller the number, the more likely o wins.
def minimax(myBoard, depth, alpha, beta, maximizingPlayer):
    myEval = evaluate(myBoard)

    if myEval is not None:
        return myEval

    # if we have reached maximum depth
    if depth <= 0:
        if myEval is not None:
            return myEval
        else:
            return 0

    # now we are finding all of the legal moves from this position
    moves = []
    for i in range(bdimm):
        for j in range(bdimm):
            if myBoard[i][j] == 0:
                moves.append((i, j))

    if maximizingPlayer:
        maxEval = NEG_INF  # negative infinity
        # now we need to check each possible move from the given position
        for item in moves:
            newBoard = copy.deepcopy(myBoard)
            r, c = item
            newBoard[r][c] = 1  # setting the position to an x
            ans = minimax(newBoard, depth-1, alpha, beta, False)

            maxEval = max(maxEval, ans)
            alpha = max(alpha, ans)

            if beta <= alpha:
                break

        return maxEval

    # if we are not the maximizing player
    else:
        minEval = INF  # positive infinity
        # now we need to check each possible move from the given position
        for item in moves:
            newBoard = copy.deepcopy(myBoard)
            r, c = item
            newBoard[r][c] = -1  # setting the position to an o
            ans = minimax(newBoard, depth-1, alpha, beta, True)
            minEval = min(minEval, ans)
            beta = min(beta, ans)

            if beta <= alpha:
                break

        return minEval


# takes board state, looks at all availible moves, makes the moves,
# then passes board to minimax. minimax returns the value of that move.
# depending on whose turn it is, we take either the move with the highest, or lowest value.
def choose_best(myBoard, x_player, turns_left):

    moves = []
    for i in range(bdimm):
        for j in range(bdimm):
            if myBoard[i][j] == 0:
                moves.append((i, j))

    if x_player:
        best_move = None
        best_val = NEG_INF

        # now we need to check each possible move from the given position
        for idx, move in enumerate(moves):

            # print('Evaluating move:', idx + 1)

            newBoard = copy.deepcopy(myBoard)
            r, c = move
            newBoard[r][c] = 1  # setting the position to an x
            ans = minimax(newBoard, turns_left - 1, NEG_INF, INF, False)

            if ans > best_val:
                best_val = ans
                best_move = move

        return best_move

    else:
        best_move = None
        best_val = INF

        # now we need to check each possible move from the given position
        for idx, move in enumerate(moves):

            # print('Evaluating move:', idx + 1)

            newBoard = copy.deepcopy(myBoard)
            r, c = move
            newBoard[r][c] = -1  # setting the position to an x
            ans = minimax(newBoard, turns_left - 1, NEG_INF, INF, True)

            if ans < best_val:
                best_val = ans
                best_move = move

        return best_move


def from_linear_to_2d(idx):
    # so the way we store the rectangles that are displayed goes as follows:
    # (0, 1, 2, 3, ... , (BSIZE * BSIZE) - 1)
    # however, the actual board that we are doing calculations on is a 2d list.
    # so we need to convert the aforementioned values to their respective 2d counterpart.
    modulo = idx % BSIZE
    div = idx // BSIZE
    return div, modulo


def from_2d_to_linear(row, col):
    # similar to the above function, we also want to go from 2d to linear.
    row_component = row * bdimm
    col_component = col
    return row_component + col_component


# Below are the functions relating to the screen drawing!


# creates a tile for each tile on screen, so we can see which tile the user clicks.
def make_tiles(myCubeSize, myDisplayDimm):
    myTiles = []
    for i in range(BSIZE):
        for j in range(BSIZE):
            x = (myDisplayDimm / BSIZE) * j
            y = (myDisplayDimm / BSIZE) * i

            new = pygame.Rect(x, y, myCubeSize, myCubeSize)
            myTiles.append(new)
    return myTiles


# draws the separating lines between each tile.
def draw_sep_lines(myScreen, myCubeSize, mySdimm):
    # drawing vertical lines
    for i in range(1, BSIZE):
        start = myCubeSize * i
        pygame.draw.line(myScreen, black,
                         (start, 0),
                         (start, mySdimm))

    # drawing vertical lines
    for j in range(1, BSIZE):
        start = myCubeSize * j
        pygame.draw.line(myScreen, black,
                         (0, start),
                         (mySdimm, start))


# draws a circle on a given tile.
def draw_circle(myScreen, myRect):
    center = myRect.center
    pygame.draw.circle(myScreen, black, center, int(cube_size//2) - 5, 5)


# draws an x on a given tile.
def draw_x(myScreen, myRect):
    pygame.draw.line(myScreen, black, myRect.topleft, myRect.bottomright, 5)
    pygame.draw.line(myScreen, black, myRect.topright, myRect.bottomleft, 5)


# draws the starting menu. returns the top and bottom tiles.
def draw_menu(myScreen, myDisplayDimm):
    half = myDisplayDimm // 2
    rad = int(cube_size // 2) - 5
    center_c = (half, half + (half // 2))
    center_x = (half, half - (half // 2))

    tmp1, tmp2 = center_x
    start_x = tmp1 - rad // 2
    start_y = tmp2 - rad // 2

    # draw mid line
    pygame.draw.line(myScreen, black, (0, half), (myDisplayDimm, half))

    # in top half, draw an 'x'
    pygame.draw.line(myScreen, black, (start_x, start_y), (start_x + rad, start_y + rad), 8)
    pygame.draw.line(myScreen, black, (start_x, start_y + rad), (start_x + rad, start_y), 8)

    # in bottom, draw an 'o'
    pygame.draw.circle(myScreen, black, center_c, rad, 5)

    # now make rectangles for hit detection
    top = pygame.Rect(0, 0, myDisplayDimm, half)
    bottom = pygame.Rect(0, half, myDisplayDimm, myDisplayDimm)

    return top, bottom  # where top is x and bottom is o
