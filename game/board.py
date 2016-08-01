class Board:
    INDICATORS = {
        'vship': '|',
        'hship': '-',
        'empty': 'O',
        'miss': '.',
        'hit': '*',
        'sunk': '#'
    }

    def __init__(self, size=10, **kwargs):
        self.size = size
        self.board = (self.build_empty_board()
                      if 'board' not in kwargs
                      else kwargs['board'])
        self.available_moves = (self.build_initial_moves()
                                if 'moves_left' not in kwargs
                                else kwargs['moves_left'])

    def place_token(self, cell, token):
        """Places a 'token' at a given cell location.

        Keyword arguments:
        cell -- the indices of grid position
        token -- A character to be represented on board.
        """
        self.board['rows'][cell[1]][cell[0]] = token

    def parse_move(self, move):
        """Parse string input into position indices list.

        Keyword arguments:
        move -- a move input string from player
        """
        return [move[0], int(move[1:])]

    def move_pos(self, move):
        """Return a list containing cell position

        Keyword arguments:
        cell -- a two item list, contains grid position.
        """
        cell = self.parse_move(move)
        col = self.board['heading'].index(cell[0])
        row = cell[1] - 1
        return [col, row]

    def placement_cells(self, size, cell, angle):
        cells = []
        for i in range(size):
            if angle == 'V':
                cells.append([cell[0], cell[1] + i])
            elif angle == 'H':
                cells.append([cell[0] + i, cell[1]])

        return cells

    def is_sunk(self, ship, start, angle):
        sunk_check = []
        cell = self.move_pos(start)
        ship_pos = self.placement_cells(ship.size, cell, angle)
        for pos in ship_pos:
            if pos == Board.INDICATORS['hit']:
                sunk_check.append(True)
            else:
                sunk_check.append(False)

        return all(sunk_check)

    def place_ship(self, ship, move='', angle=''):
        if move in self.available_moves:
            if self.angle_check(angle):
                cell = self.move_pos(move)
                pos_groups = self.placement_cells(ship.size, cell, angle)
                coll_check = self.collision_check(pos_groups)
                if coll_check:
                    v_ship = Board.INDICATORS['vship']
                    h_ship = Board.INDICATORS['hship']
                    for pos in pos_groups:
                        if angle == 'V':
                            self.board['rows'][pos[1]][pos[0]] = v_ship
                        elif angle == 'H':
                            self.board['rows'][pos[1]][pos[0]] = h_ship

                    ship.set_pos(self.get_location(pos_groups))
                    ship.set_angle(angle)
                    return True
                elif coll_check is None:
                    self.print_error('''
                        Your ship has to be placed inside the board.''')
                else:
                    self.print_error('''
                        You cannot place a ship across another ship.''')
            else:
                self.print_error('''
                    Invalid direction, Horizontal or Vertical.''')
        else:
            self.print_error('Invalid grid position.')
        return False

    def angle_check(self, angle=''):
        return True if angle == 'V' or angle == 'H' else False

    def collision_check(self, pos_groups=[]):
        checks = []
        for pos in pos_groups:
            if not self.valid_size(pos):
                return None
            else:
                indicator = self.indicator_at_cell(pos)
                check = (True if indicator == Board.INDICATORS['empty']
                         else False)
                checks.append(check)

        return False if False in checks else True

    def valid_size(self, cell):
        size = self.size - 1
        if cell[0] > size or cell[1] > size:
            return False
        else:
            return True

    def get_location(self, pos_groups):
        locations = []
        for pos in pos_groups:
            head = self.board['heading'][pos[0]]
            row = pos[1] + 1
            locations.append('{}{}'.format(head, row))
        return locations

    def remove_move(self, move):
        if move in self.available_moves:
            self.available_moves.remove(move)

    def print_error(self, message='Error.'):
        print('\n**{}**\n'.format(message))

    def check_move(self, move):
        """Validate a player move on the board.

        Keyword arguments:
        move -- a move input string from player
        """
        return True if move in self.available_moves else False

    def indicator_at_cell(self, cell):
        """Returns the indicator value at index positions

        Keyword arguments:
        cell -- list containing board index positions
        """
        return self.board['rows'][cell[1]][cell[0]]

    def get_indicator(self, cell):
        """Return an indicator based on 'hit' or 'miss'

        Keyword arguments:
        cell -- list of 2 items, move position indices
        """
        indicator = self.indicator_at_cell(cell)
        if indicator == Board.INDICATORS['empty']:
            return Board.INDICATORS['miss']
        elif (indicator == Board.INDICATORS['vship'] or
                indicator == Board.INDICATORS['hship']):
            return Board.INDICATORS['hit']
        else:
            return False

    def build_initial_moves(self):
        """Return a list of all possible moves"""
        moves = []
        for col in self.board['heading']:
            for i in range(self.size):
                moves.append('{}'.format(col + str(i + 1)))
        return moves

    def build_empty_board(self):
        """Return an empty board Dict

        Keyword arguments:
        size -- the integer size of the board.
        """
        return {
            'heading': self.build_board_heading(),
            'rows': self.build_board_rows()
        }

    def build_board_heading(self):
        """Return a list of alphabetical heading letters.

        Keyword arguments:
        size -- the integer size of the board.
        """
        return [chr(c) for c in range(ord('A'), ord('A') + self.size)]

    def build_board_rows(self):
        """Return a list filled with INDICATOR['empty'] values

        Keyword arguments:
        size -- the integer size of the board.
        """
        rows = []
        for row in range(self.size):
            rows.append(
                [Board.INDICATORS['empty'] for col in range(self.size)]
            )

        return rows
