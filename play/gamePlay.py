EMPTY = 0
BLACK = 1
WHITE = 2

ROW = 10
COL = 10


# every game will have a ChessBoard
class ChessBoard(object):
    def __init__(self):
        # init ChessBoard
        self.board = [[EMPTY for i in range(COL)] for j in range(ROW)]

    def move(self, row, col, color):
        # player move
        if self.board[row][col] == EMPTY:
            self.board[row][col] = BLACK if color == 'Black' else WHITE
            return True
        return False

    def win(self, row, col, color):
        # check if new move will win the game
        left_border = col - 4 if col >= 4 else 0
        right_border = col + 4 if col + 4 <= COL - 1 else COL -1
        top_border = row - 4 if row >= 4 else 0
        down_border = row + 4 if row + 4 <= ROW - 1 else ROW - 1

        count_horizon = 0
        count_vertical = 0
        count_slash = 0
        count_backslach = 0

        # check if there are 5 continuous steps in horizon direction
        j = left_border
        while left_border <= j <= right_border:
            count_horizon = count_horizon + 1 if self.board[row][j] == color else 0
            if count_horizon == 5:
                return True
            j += 1

        # check if there are 5 continuous steps in vertical direction
        i = top_border
        while top_border <= i <= down_border:
            count_vertical = count_vertical + 1 if self.board[i][col] == color else 0
            if count_vertical == 5:
                return True
            i += 1

        # check if there are 5 continuous steps in \ direction
        tl_col = dl_col = left_border  # top-left col; down-left col
        tl_row = tr_row = top_border   # top-left row; down-left row
        dr_col = tr_col = right_border  # down-right col; top-right col
        dr_row = dl_row = down_border   # down-right row; top-right row
        if col - left_border > row - top_border:
            tl_col = col - (row - top_border)
        else:
            tl_row = row - (col - left_border)

        if right_border - col > down_border - row:
            dr_col = col + (down_border - row)
        else:
            dr_row = row + (right_border - col)

        i = tl_row
        j = tl_col
        while tl_col <= j <= dr_col and tl_row <= i <= dr_row:
            count_backslach = count_backslach + 1 if self.board[i][j] == color else 0
            if count_backslach == 5:
                return True
            i += 1
            j += 1

        # check if there are 5 continuous steps in / direction
        if right_border - col > row - top_border:
            tr_col = col + (row - top_border)
        else:
            tr_row = row - (right_border - col)

        if col - left_border > down_border - row:
            dl_col = col - (down_border - row)
        else:
            dl_row = row + (col - left_border)

        i = tr_row
        j = tr_col
        while dl_col <= j <= tr_col and tr_row <= i <= dl_row:
            count_slash = count_slash + 1 if self.board[i][j] == color else 0
            if count_slash == 5:
                return True
            i += 1
            j -= 1

        return False


    # def win(self):
    #     for row in range(ROW):
    #         flag_black = 0
    #         flag_white = 0
    #         for col in range(COL):
    #             if self.board[row][col] == BLACK:
    #                 flag_black += 1
    #                 flag_white = 0
    #             elif self.board[row][col] == WHITE:
    #                 flag_white += 1
    #                 flag_black = 0
    #             else:
    #                 flag_white = 0
    #                 flag_black = 0
    #             if flag_white == 5:
    #                 return "Black win"
    #             elif flag_white == 5:
    #                 return "White win"
    #
    # def blackWin(self):
    #     for row in range(ROW):
    #         flag_black = 0
    #         for col in range(COL):
    #             if self.board[row][col] == BLACK:
    #                 flag_black += 1
    #             else:
    #                 flag_black = 0
    #             if flag_black == 5:
    #                 return True


    # def reset(self):
    #     for row in range(len(self.board)):
    #         self.board[row] = [EMPTY for i in range(COL)]
