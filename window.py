from functions import *
import time

screen = pygame.display.set_mode((display_w, display_h))
screen.fill(white)
pygame.display.set_caption('Tic Tac Toe')
x_rect, o_rect = draw_menu(screen, display_w)
pygame.display.flip()
menu = True
bot_is_x = True
while menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            if x_rect.collidepoint(pos):
                # make the player x
                bot_is_x = False
                menu = False

            elif o_rect.collidepoint(pos):
                # make the player o
                bot_is_x = True
                menu = False


del x_rect, o_rect
screen.fill(white)  # wiping screen

# drawing the lines separating the tiles
draw_sep_lines(screen, cube_size, display_w)

# these are the tiles that will be drawn to the screen
tiles = make_tiles(cube_size, display_w)

# updating the display
pygame.display.flip()
user_turn = not bot_is_x  # if the bot is x, then it is not the users turn first.

first = True
running = True

# main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            quit()

        if user_turn:
            if first:
                print('Now it is your turn. Click a tile to make a move.\n')
                first = False

            # user clicks screen
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for idx, item in enumerate(tiles):
                    if item.collidepoint(pos):
                        # now 'item' is the rectangle selected by the player

                        r, c = from_linear_to_2d(idx)
                        if board[r][c] == 0:  # first check if the tile is occupied
                            if not bot_is_x:
                                board[r][c] = 1
                                draw_x(screen, item)
                            else:
                                board[r][c] = -1
                                draw_circle(screen, item)

                            # if we get here, the turn is successful
                            pygame.display.flip()
                            ev = evaluate(board)

                            if ev is None:  # if the game is undecided:
                                user_turn = not user_turn
                                first = True

                            else:  # game is over
                                print('Game over.')
                                running = False
                        else:  # if user selects tile that is occupied
                            print('Tile is already occupied. Try again.')

        else:  # this is the bots turn
            print('The bot in now making its turn.\n')
            bot_move = choose_best(board, bot_is_x, MAX_DEPTH)
            r, c = bot_move
            if bot_is_x:
                board[r][c] = 1
                myIdx = from_2d_to_linear(r, c)
                draw_x(screen, tiles[myIdx])
            else:
                board[r][c] = -1
                myIdx = from_2d_to_linear(r, c)
                draw_circle(screen, tiles[myIdx])

            pygame.display.flip()
            ev = evaluate(board)
            if ev is None:
                user_turn = not user_turn
                first = True
            else:
                # game is over
                print('Game over.')
                running = False

time.sleep(3)  # this is so user can see board before game closes.
