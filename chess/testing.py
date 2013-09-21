from redis_db.managers import *



from chess.models import Board

board = Board()
board.set_up_pieces()
rook = board.get_piece((1, 1))
knight = board.get_piece((2, 1))
bishop = board.get_piece((3, 1))
queen = board.get_piece((4, 1))
king = board.get_piece((5, 1))
pawn = board.get_piece((5, 2))
def test_rook():
    return rook.get_base_possible_moves()

def test_bishop():
    return bishop.get_base_possible_moves()

def test_queen():
    return queen.get_base_possible_moves()

def test_king():
    return king.get_base_possible_moves()

def test_knight():
    return knight.get_base_possible_moves()

def test_pawn():
    return pawn.get_base_possible_moves()


def test():
    knight = board.get_piece("g1")
    board.make_move(knight, 'f3')




