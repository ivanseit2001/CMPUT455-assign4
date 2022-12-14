#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

#!/usr/bin/python3
# Set the path to your python3 above



from gtp_connection import GtpConnection
from board_base import DEFAULT_SIZE, GO_POINT, GO_COLOR
from board import GoBoard
from board_util import GoBoardUtil
from engine import GoEngine


class NoGo:
    def __init__(self):
        """
        Go player that selects moves randomly from the set of legal moves.
        Does not use the fill-eye filter.
        Passes only if there is no other legal move.

        Parameters
        ----------
        name : str
            name of the player (used by the GTP interface).
        version : float
            version number (used by the GTP interface).
        """
        GoEngine.__init__(self, "NoGo4", 1.0)
        self.weight = self.read_file()

    def get_move(self, board: GoBoard, color: GO_COLOR) -> GO_POINT:
        return GoBoardUtil.generate_random_move(board, color,
                                                use_eye_filter=False)

    def read_file(self):
        file = open('weights.txt','r')
        weight_list = {}
        lines = file.readlines()
        for line in lines:
            line = line.split()
            number = int(line[0])
            weight = float(line[1])
            weight_list[number] = weight
        file.close()
        return weight_list

    def get_block(self, board, move):
        NS = board.NS
        block = [move-NS-1, move-NS, move-NS+1,
                 move-1,             move+1,
                 move+NS-1, move+NS, move+NS+1]
        return block

    def calculate_block_weight_sum(self,board,block):   # base 4
        sum = 0
        for num in range(len(block)):
            prob = board.board[block[num]]
            sum = sum + (prob*(4**num))
        return sum

    def find_probability(self, board):
        current = board.current_player
        moves = GoBoardUtil.generate_legal_moves(board,current)
        weight_total = []
        for move in moves:
            block = self.get_block(board, move)
            calculate = self.calculate_block_weight_sum(board,block)
            prob_in_dic = self.weight_list[calculate]
            weight_total.append(prob_in_dic)
        weight_sum = sum(weight_total)
        prob_total = []
        for prob in weight_total:
            prob_total.append(prob/weight_sum)
        # return the list containing the probability of each move
        return prob_total




def run() -> None:
    """
    start the gtp connection and wait for commands.
    """
    board: GoBoard = GoBoard(DEFAULT_SIZE)
    con: GtpConnection = GtpConnection(NoGo(), board)
    con.start_connection()


if __name__ == "__main__":
    run()
