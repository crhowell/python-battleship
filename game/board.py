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
                      if 'board' not in kwargs else kwargs['board'])
        self.available_moves = (self.build_initial_moves()
                                if 'moves_left' not in kwargs else kwargs['moves_left'])

    def place_token(self, cell, token):
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

    def place_ship(self, ship, move, angle):
        if move in self.available_moves:
            cell = self.move_pos(move)
            pos_groups = self.placement_cells(ship.size, cell, angle)
            if self.collision_check(pos_groups):
                for i in range(ship.size):
                    if angle == 'V':
                        self.board['rows'][cell[1] + i][cell[0]] = Board.INDICATORS['vship']
                    elif angle == 'H':
                        self.board['rows'][cell[1]][cell[0] + i] = Board.INDICATORS['hship']
                return True
            else:
                print('\n**You cannot place a ship across another ship.**\n')
        else:
            print('\n**Invalid grid position.**\n')
        return False

    def collision_check(self, pos_groups=[]):
        checks = []
        for pos in pos_groups:
            indicator = self.indicator_at_cell(pos)
            check = True if indicator == Board.INDICATORS['empty'] else False
            checks.append(check)

        return False if False in checks else True

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
        elif (indicator == Board.INDICATORS['vship']
              or indicator == Board.INDICATORS['hship']):
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
            rows.append([Board.INDICATORS['empty'] for col in range(self.size)])

        return rows
