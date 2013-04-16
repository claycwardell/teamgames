import pdb
from chess import consts

def func1(i):
    return i + 1
def func2(i):
    return i - 1

class Board(object):
    def __init__(self):
        self.piece_map  = {}
        for i in xrange(1, 9):
            for j in xrange(1, 9):
                self.piece_map[i, j] = None


    def set_up_pieces(self):
        # White pieces
        self.piece_map[(1, 1)] = Rook((1, 1), consts.WHITE_COLOR)
        self.piece_map[(2, 1)] = Knight((2, 1), consts.WHITE_COLOR)
        self.piece_map[(3, 1)] = Bishop((3, 1), consts.WHITE_COLOR)
        self.piece_map[(4, 1)] = Queen((4, 1), consts.WHITE_COLOR)
        self.piece_map[(5, 1)] = King((5, 1), consts.WHITE_COLOR)
        self.piece_map[(6, 1)] = Bishop((6, 1), consts.WHITE_COLOR)
        self.piece_map[(7, 1)] = Knight((7, 1), consts.WHITE_COLOR)
        self.piece_map[(8, 1)] = Rook((8, 1), consts.WHITE_COLOR)

        # Black pieces
        self.piece_map[(1, 8)] = Rook((1, 8), consts.BLACK_COLOR)
        self.piece_map[(2, 8)] = Knight((2, 8), consts.BLACK_COLOR)
        self.piece_map[(3, 8)] = Bishop((3, 8), consts.BLACK_COLOR)
        self.piece_map[(4, 8)] = Queen((4, 8), consts.BLACK_COLOR)
        self.piece_map[(5, 8)] = King((5, 8), consts.BLACK_COLOR)
        self.piece_map[(6, 8)] = Bishop((6, 8), consts.BLACK_COLOR)
        self.piece_map[(7, 8)] = Knight((7, 8), consts.BLACK_COLOR)
        self.piece_map[(8, 8)] = Rook((8, 8), consts.BLACK_COLOR)


        for i in xrange(1, 9):
            self.piece_map[(i, 2)] = Pawn((i, 2), consts.WHITE_COLOR)
            self.piece_map[(i, 7)] = Pawn((i, 7), consts.BLACK_COLOR)


    def get_piece(self, coords):
        return self.piece_map[coords]

    def set_piece(self, piece, coords):
        self.piece_map[coords] = piece



    def show(self):
        piece_list = []
        for y in reversed(xrange(1, 9)):
            for x in xrange(1, 9):
                piece = self.get_piece((x, y))
                if piece is None:
                    piece_list.append("--")
                else:
                    piece_list.append(piece.display_str)

        piece_tuple = tuple(piece_list)
        print

        board_string = \
        """
        %s %s %s %s %s %s %s %s
        %s %s %s %s %s %s %s %s
        %s %s %s %s %s %s %s %s
        %s %s %s %s %s %s %s %s
        %s %s %s %s %s %s %s %s
        %s %s %s %s %s %s %s %s
        %s %s %s %s %s %s %s %s
        %s %s %s %s %s %s %s %s

        """ % piece_tuple

        print board_string


    def make_move(self, origin, destination):
        piece = self.get_piece(origin)
        if piece is None:
            raise ValueError("No piece at origin")
        if destination not in piece.get_possible_moves():
            raise ValueError("Illegal move for that piece")





class Piece(object):
    def __init__(self, position, color):
        self._position = position
        self._color = color

    @property
    def display_str(self):
        if self._color == consts.WHITE_COLOR:
            return "%s%s" % ("w", self._letter)
        elif self._color == consts.BLACK_COLOR:
            return "%s%s" % ("b", self._letter)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, destination):
        self._position = destination



class DiagonalMovingPiece(object):
    def get_diagonal_moves(self):
        """
        This gets the possible moves as defined by the pieces type. For example, a king's base moves are
        1 square in any direction
        """
        possible_move_set = set()

        y_funcs = x_funcs = [func1, func2]

        for y_func in y_funcs:
            print "first loop"
            for x_func in x_funcs:
                x, y = self._position
                print "second loop"
                while (1 <= x <= 8 and 1 <= y <= 8):
                    possible_move_set.add((x, y))
                    print "adding %s, %s" % (x, y)
                    x = x_func(x)
                    y = y_func(y)

        possible_move_set.remove(self._position)
        return possible_move_set



class PerpendicularMovingPiece(object):
    def get_perpendicular_moves(self):
        possible_move_set = set()
        funcs = [func1, func2]
        for func in funcs:
            x, y = self._position
            while (1 <= x <= 8):
                possible_move_set.add((x, y))
                print "adding %s, %s" % (x, y)
                x = func(x)
            x, y = self._position
            while (1 <= y <= 8):
                possible_move_set.add((x, y))
                print "adding %s, %s" % (x, y)
                y = func(y)

        possible_move_set.remove(self._position)
        return possible_move_set


class Bishop(Piece, DiagonalMovingPiece):
    def __init__(self, position, color):
        super(Bishop, self).__init__(position, color)
        self._letter = "B"

    def get_base_possible_moves(self):
        return self.get_diagonal_moves()


class Rook(Piece, PerpendicularMovingPiece):
    def __init__(self, position, color):
        super(Rook, self).__init__(position, color)
        self._letter = "R"


    def get_base_possible_moves(self):
        return self.get_perpendicular_moves()



class Knight(Piece):
    def __init__(self, position, color):
        super(Knight, self).__init__(position, color)
        self._letter = "N"

    def get_base_possible_moves(self):
        def big_move1(x, y):
            return (x + 2, y)

        def big_move2(x, y):
            return (x-2, y)

        def big_move3(x, y):
            return (x, y+2)

        def big_move4(x, y):
            return (x, y-2)

        def little_move1(x, y):
            return (x + 1, y)

        def little_move2(x, y):
            return (x-1, y)

        def little_move3(x, y):
            return (x, y-1)

        def little_move4(x, y):
            return (x, y+1)


        possible_move_set = set()
        for big_func in [big_move1, big_move2, big_move3, big_move4]:
            if big_func == big_move1 or big_func == big_move2:
                for little_func in [little_move3, little_move4]:
                    x, y = self._position
                    x, y = big_func(x, y)
                    x, y = little_func(x, y)
                    if 1 <= x <= 8 and 1 <= y <= 8:
                        print "adding %s, %s" % (x, y)
                        possible_move_set.add((x, y))

            elif big_func == big_move3 or big_func == big_move4:
                for little_func in [little_move1, little_move2]:
                    x, y = self._position
                    x, y = big_func(x, y)
                    x, y = little_func(x, y)
                    if 1 <= x <= 8 and 1 <= y <= 8:
                        print "adding %s, %s" % (x, y)
                        possible_move_set.add((x, y))

        return possible_move_set




class Queen(Piece, PerpendicularMovingPiece, DiagonalMovingPiece):
    def __init__(self, position, color):
        super(Queen, self).__init__(position, color)
        self._letter = "Q"


    def get_base_possible_moves(self):
        return self.get_diagonal_moves() | self.get_perpendicular_moves()

class King(Piece, PerpendicularMovingPiece, DiagonalMovingPiece):
    def __init__(self, position, color):
            super(King, self).__init__(position, color)
            self._letter = "K"


    def get_base_possible_moves(self):
        queen_set = self.get_perpendicular_moves() | self.get_diagonal_moves()
        possible_move_set = set()
        for tup in queen_set:
            mov_x, mov_y = tup
            self_x, self_y = self._position
            if abs(mov_x - self_x) <= 1 and abs(mov_y - self_y) <= 1:
                possible_move_set.add(tup)

        return possible_move_set


class Pawn(Piece):
    def __init__(self, position, color):
        super(Pawn, self).__init__(position, color)
        self._letter = "p"
        self._has_moved = False
        self._may_en_passant = False


    def get_base_possible_moves(self):
        possible_move_set = set()
        x, y = self._position
        if not self._has_moved:
            possible_move_set.add((x, y+2))
        possible_move_set.add((x, y+1))
        possible_move_set.add((x-1, y+1))
        possible_move_set.add((x+1, y+1))
        return possible_move_set




