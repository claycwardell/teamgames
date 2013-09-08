import pdb
from chess import consts, utils
from chess.exceptions import IllegalMoveException, InsaneBoardStateException
import logging

logging.basicConfig(level='DEBUG')


class Board(object):
    def __init__(self):
        self.piece_map  = {}
        for i in xrange(1, 9):
            for j in xrange(1, 9):
                self.piece_map[i, j] = None


    def set_up_pieces(self):
        # White pieces
        self.piece_map[(1, 1)] = Rook(      (1, 1),     consts.WHITE_COLOR)
        self.piece_map[(2, 1)] = Knight(    (2, 1),     consts.WHITE_COLOR)
        self.piece_map[(3, 1)] = Bishop(    (3, 1),     consts.WHITE_COLOR)
        self.piece_map[(4, 1)] = Queen(     (4, 1),     consts.WHITE_COLOR)
        self.piece_map[(5, 1)] = King(      (5, 1),     consts.WHITE_COLOR)
        self.piece_map[(6, 1)] = Bishop(    (6, 1),     consts.WHITE_COLOR)
        self.piece_map[(7, 1)] = Knight(    (7, 1),     consts.WHITE_COLOR)
        self.piece_map[(8, 1)] = Rook(      (8, 1),     consts.WHITE_COLOR)

        # Black pieces
        self.piece_map[(1, 8)] = Rook(      (1, 8),     consts.BLACK_COLOR)
        self.piece_map[(2, 8)] = Knight(    (2, 8),     consts.BLACK_COLOR)
        self.piece_map[(3, 8)] = Bishop(    (3, 8),     consts.BLACK_COLOR)
        self.piece_map[(4, 8)] = Queen(     (4, 8),     consts.BLACK_COLOR)
        self.piece_map[(5, 8)] = King(      (5, 8),     consts.BLACK_COLOR)
        self.piece_map[(6, 8)] = Bishop(    (6, 8),     consts.BLACK_COLOR)
        self.piece_map[(7, 8)] = Knight(    (7, 8),     consts.BLACK_COLOR)
        self.piece_map[(8, 8)] = Rook(      (8, 8),     consts.BLACK_COLOR)


        for i in xrange(1, 9):
            self.piece_map[(i, 2)] = Pawn((i, 2), consts.WHITE_COLOR)
            self.piece_map[(i, 7)] = Pawn((i, 7), consts.BLACK_COLOR)


    def get_piece(self, coords):
        coords = utils.get_coord_tuple(coords)
        return self.piece_map[coords]

    def set_piece(self, piece, coords):
        potential_captured_piece = self.get_piece(coords)
        self.piece_map[coords] = piece
        piece.position = coords
        return potential_captured_piece


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

#######################################################################################################################
#TODO: Sort through this mess
    def make_move(self, origin, destination):
        piece = self.get_piece(origin)
        if piece is None:
            raise ValueError("No piece at origin")
        if destination not in piece.get_possible_moves():
            raise ValueError("Illegal move for that piece")

    def make_move(self, moving_piece, destination):
        moving_piece.rollback_position = moving_piece.position
        potential_captured_piece = self.set_piece(moving_piece, destination)
        try:
            self.validate_did_not_move_into_check(moving_piece.color)
        except IllegalMoveException:
            self.set_piece(moving_piece, moving_piece.rollback_position)
            self.set_piece(potential_captured_piece, potential_captured_piece.position)

#######################################################################################################################

    def determine_move_direction(self, moving_piece, destination):
        sx = moving_piece.position[0]
        sy = moving_piece.position[1]
        dx = destination[0]
        dy = destination[1]

        if dx > sx:
            if dy > sy:
                return "ne"
            elif dy == sy:
                return "e"
            elif dy < sy:
                return "se"
        elif sx < sx:
            if dy > sy:
                return "nw"
            if dy == sy:
                return "w"
            if dy < sy:
                return "sw"
        elif sx == sy:
            if dy > sy:
                return "n"
            elif dy < sy:
                return "s"
            elif dy == sy:
                raise ValueError("cannot move to current position")


    def _validate_move(self, moving_piece, destination, king_capture=False):
        destination = utils.get_coord_tuple(destination)
        if destination not in moving_piece.get_base_possible_moves():
            return False
        direction = self.determine_move_direction(moving_piece, destination)
        current_x = moving_piece.position[0]
        current_y = moving_piece.position[1]

        if direction == 'ne':
            while (current_x, current_y) != destination:
                current_x += 1
                current_y += 1
                self.check_square_is_available(moving_piece, (current_x, current_y), allow_capture=False)

        elif direction == 'e':
            while (current_x, current_y) != destination:
                current_x += 1
                self.check_square_is_available(moving_piece, (current_x, current_y), allow_capture=False)

        elif direction == 'se':
            while (current_x, current_y) != destination:
                current_x += 1
                current_y -= 1
                self.check_square_is_available(moving_piece, (current_x, current_y), allow_capture=False)

        elif direction == 's':
            while (current_x, current_y) != destination:
                current_y -= 1
                self.check_square_is_available(moving_piece, (current_x, current_y), allow_capture=False)

        elif direction == 'sw':
            while (current_x, current_y) != destination:
                current_x -= 1
                current_y -= 1
                self.check_square_is_available(moving_piece, (current_x, current_y), allow_capture=False)

        elif direction == 'w':
            while (current_x, current_y) != destination:
                current_x -= 1
                self.check_square_is_available(moving_piece, (current_x, current_y), allow_capture=False)

        elif direction == 'nw':
            while (current_x, current_y) != destination:
                current_x -= 1
                current_y += 1
                self.check_square_is_available(moving_piece, (current_x, current_y), allow_capture=False)

        self.check_square_is_available(moving_piece, (current_x, current_y), allow_capture=True)

        opposing_color = self.get_opposing_color(moving_piece.color)
        self.validate_did_not_move_into_check(opposing_color, king_capture)



    def _validate_jump(self, moving_piece, destination, king_capture=False):
        if moving_piece.__class__ != Knight:
            raise ValueError("Can only jump with knights")
        self.check_square_is_available(moving_piece, destination)

        opposing_color = self.get_opposing_color(moving_piece.color)
        self.validate_did_not_move_into_check(opposing_color, king_capture)


    def _validate_pawn_move(self, moving_piece, destination, king_capture=False):
        if moving_piece.__class__ != Pawn:
            raise ValueError("Validate Pawn Move called with non-pawn piece")
        self.check_square_is_available(moving_piece, destination)

        #TODO: Finish this

        opposing_color = self.get_opposing_color(moving_piece.color)



    def validate_did_not_move_into_check(self, color_to_play, king_capture=False):
        """
        Checks that the moving player did not move into check.  Returns None if he did not, otherwise
        raises IllegalMoveException
        """
        if not king_capture:
            opposing_color = self.get_opposing_color(color_to_play)
            opposing_king = self.get_king(opposing_color)
            for square in self.piece_map:
                possible_piece = self.get_piece(square)
                logging.info("Validating piece: %s", possible_piece)
                if possible_piece is not None and possible_piece.color == color_to_play:
                    if self.validate_play(possible_piece, opposing_king.position):
                        raise IllegalMoveException


    def validate_play(self, playing_piece, destination):
        """
        Allows piece agnostic play validation.  Routes knights to _validate_jump and other pieces to _validate_move
        """
        king_capture = False
        possible_piece = self.get_piece(destination)
        if possible_piece is not None and possible_piece.__class__ == King:
            king_capture = True

        if playing_piece.__class__ == Knight:
            return self._validate_jump(playing_piece, destination, king_capture)
        else:
            return self._validate_move(playing_piece, destination, king_capture)


    def check_square_is_available(self, moving_piece, square_coords, allow_capture=False):
        """
        Checks that the passed in square does not contain a piece of the same color as the moving piece.
        """
        possible_piece = self.get_piece(square_coords)
        if possible_piece is None:
            square_allowed = True
        else:
            if not allow_capture:
                square_allowed = not possible_piece
            else:
                square_allowed = not (possible_piece.color == moving_piece.color)

        if not square_allowed:
            raise IllegalMoveException


    def get_king(self, color):
        """
        Convenience method to get the king of a given color
        """
        for square in self.piece_map:
            possible_piece = self.get_piece(square)
            if possible_piece is not None and possible_piece.__class__ == King and possible_piece.color == color:
                return possible_piece
        raise InsaneBoardStateException("Color %s has no king!", consts.COLOR_MAP[color])


    @staticmethod
    def get_opposing_color(color):
        """
        Convenience method to return opposite color of the one passed in.
        """
        if color == consts.BLACK_COLOR:
            return consts.WHITE_COLOR
        if color == consts.WHITE_COLOR:
            return consts.BLACK_COLOR




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


    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    def __repr__(self):
        display_str = self.display_str
        position = self.position
        column = consts.LETTER_AND_INT_MAP[position[0]]
        row = position[1]
        ret_str = "%s on %s%s" % (display_str, column, row)
        return ret_str



class MovingPiece(Piece):
#    __move_method__ = Board.move
    pass


class JumpingPiece(Piece):
#    __move_method__ = Board.jump
    pass


class DiagonalMovingMixin(object):
    def get_diagonal_moves(self):
        possible_move_set = set()

        y_funcs = x_funcs = [utils.increment, utils.decrement]

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



class PerpendicularMovingMixin(object):
    def get_perpendicular_moves(self):
        possible_move_set = set()
        funcs = [utils.increment, utils.decrement]
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


class Bishop(MovingPiece, DiagonalMovingMixin):
    def __init__(self, position, color):
        super(Bishop, self).__init__(position, color)
        self._letter = "B"

    def get_base_possible_moves(self):
        return self.get_diagonal_moves()


class Rook(MovingPiece, PerpendicularMovingMixin):
    def __init__(self, position, color):
        super(Rook, self).__init__(position, color)
        self._letter = "R"


    def get_base_possible_moves(self):
        return self.get_perpendicular_moves()



class Knight(JumpingPiece):
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




class Queen(MovingPiece, PerpendicularMovingMixin, DiagonalMovingMixin):
    def __init__(self, position, color):
        super(Queen, self).__init__(position, color)
        self._letter = "Q"


    def get_base_possible_moves(self):
        return self.get_diagonal_moves() | self.get_perpendicular_moves()

class King(MovingPiece, PerpendicularMovingMixin, DiagonalMovingMixin):
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
        self._vulnerable_to_en_passant = False


    def get_base_possible_moves(self):
#        pdb.set_trace()
        possible_move_set = set()
        if self.color == consts.WHITE_COLOR:
            y_move_func = utils.increment
        else:
            y_move_func = utils.decrement
        x, y = self._position
        if not self._has_moved:
            possible_move_set.add((x,
                                   y_move_func( y_move_func(y)) )
            )
        possible_move_set.add((x, y_move_func(y)))
        possible_move_set.add((x-1, y_move_func(y)))
        possible_move_set.add((x+1, y_move_func(y)))
        return possible_move_set




