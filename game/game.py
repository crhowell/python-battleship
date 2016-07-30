from .board import Board
from .player import Player
from .ship import Ship


class Game:
    MAX_PLAYERS = 2
    FLEET = [
        ("Aircraft Carrier", 5),
        ("Battleship", 4),
        ("Submarine", 3),
        ("Cruiser", 3),
        ("Patrol Boat", 2)
    ]

    def __init__(self):
        self.print_intro()
        self.players = self.initialize_players()
        self.place_ships()
        self.game_over = False

    def play(self):
        """Game Loop

        ** Needs Refactoring **
        """
        print('Game Running')
        board = self.enemy_board()
        while not self.game_over:
            self.clear_screen()
            self.prompt_to_continue('\n\n{} it is your turn.'.format(self.players[0]['player']))
            self.print_game_board()
            move = self.get_player_move()
            while not board.check_move(move):
                print('{} is an invalid move, try again.'.format(move))
                move = self.get_player_move()
            cell = board.move_pos(move)
            token = board.get_indicator(cell)
            if token == Board.INDICATORS['hit']:
                ship = self.get_ship(move)
                ship.hit()
                print('Ship: {} hits: {} sunk: {}'.format(ship, ship.hits_taken, ship.is_sunk()))
                if ship.is_sunk():
                    token = Board.INDICATORS['sunk']
                    for pos in ship.pos:
                        self.update_boards(board.move_pos(pos), token)
                    self.sunk_ship()
                    self.is_game_over()
                else:
                    self.update_boards(cell, token)
            else:
                self.update_boards(cell, token)

            board.remove_move(move)
            self.switch_players()
            board = self.enemy_board()
            self.clear_screen()
            self.print_game_board()
            self.prompt_to_continue('\nMove placed.\nBefore changing players:')

        print('\nGame Over\n')
        print('Winner is {}'.format(self.players[1]['player']))

    def update_boards(self, cell, token):
        """Updates current and opposing player's boards."""
        self.players[1]['board'].place_token(cell, token)
        self.players[0]['moves'].place_token(cell, token)

    def current_board(self):
        """Return the current player board."""
        return self.players[0]['board']

    def enemy_board(self):
        """Return the opposing players board."""
        return self.players[1]['board']

    def sunk_ship(self):
        """Increment player ship sunk count by 1."""
        self.players[1]['sunk'] += 1

    def get_player_move(self):
        """Prompts player for a move on board."""
        return self.players[0]['player'].move()

    def get_player_name(self, num):
        """Prompts player for name, returns the name.

        Keyword arguments:
        num -- Number placeholder for a user
        """
        return input('Player {} enter your name: '.format(num))

    def switch_players(self):
        """Remove 1st player and append to end."""
        self.players.append(self.players.pop(0))

    def place_ships(self):
        """Placement of all Game Players ships."""
        for player in self.players:
            self.clear_screen()
            self.prompt_to_continue(
                '\n{} you will now place your ships.\n'.format(player['player'])
            )
            board = player['board']
            for ship in player['fleet']:
                placed = False
                self.print_placement_header(player['player'])
                while not placed:
                    self.print_board(player['board'])
                    print('\nThe {} takes {} spots'.format(ship, ship.size))
                    move = player['player'].prompt_for('place {} at'.format(ship))
                    angle = player['player'].prompt_for('(H)oriztal or (V)ertical')[0]
                    self.clear_screen()
                    placed = board.place_ship(ship, move, angle)

    def get_ship(self, loc):
        """Return a ship, by a given location.

        Keyword arguments:
        loc -- Grid location, Ex. 'A3'
        """
        for battleship in self.players[1]['fleet']:
            if loc in battleship.pos:
                return battleship
        return None

    def is_game_over(self):
        """Sets game_over flag.
        True, If all opposing players ships are sunk.
        """
        sunken_ships = self.players[1]['sunk']
        total_ships = len(self.players[1]['fleet'])
        self.game_over = True if sunken_ships >= total_ships else False

    def clear_screen(self):
        """Clears the terminal screen."""
        print("\033c", end="")

    def prompt_to_continue(self, message=''):
        """Prompts user to press ENTER with any given message.

        Keyword arguments:
        message -- a string message to be displayed
        """
        input('{} {}'.format(message, 'Press ENTER to continue...'))

    def print_placement_header(self, player):
        """Displays the ship placement header for a given player.

        Keyword arguments:
        player -- a Player()
        """
        print('-' * 25, '\n')
        print('{} PLACE YOUR BATTLESHIPS\n'.format(player))
        print('-' * 25, '\n')

    def print_board_heading(self, board):
        """Displays the heading section of the board."""
        print("   " + " ".join(board.board['heading']))

    def print_board(self, board):
        """Displays entire game board of the current player.

        Keyword arguments:
        board -- a player's Board().
        hide -- if pieces should be hidden from display.
        """
        self.print_board_heading(board)
        row_num = 1
        for row in board.board['rows']:
            print(str(row_num).rjust(2) + " " + (" ".join(row)))
            row_num += 1

    def print_intro(self):
        print(' ', '-'*25)
        print('  |', ' '*21, '|')
        print('  |', '   WELCOME TO        ', '|')
        print('  | B A T T L E S H I P   |')
        print('  |', ' ' * 21, '|')
        print(' ', '-'*25)

    def print_game_board(self):
        """Displays both boards for current player."""
        print('-' * 25, '\n', 'Shots at Enemy\n', '-' * 25, '\n')
        print(self.print_board(self.players[0]['moves']))
        print('=' * 25)
        print(self.print_board(self.players[0]['board']))
        print('-' * 25, '\nShots at You\n', '-' * 25)

    def initialize_players(self):
        """Sets up initial state for all game players."""
        players = []
        for i in range(Game.MAX_PLAYERS):
            name = Player(self.get_player_name(i + 1))
            players.append({
                'player': name,
                'board': Board(),
                'moves': Board(),
                'fleet': self.build_new_fleet(),
                'sunk': 0
            })
        return players

    def build_new_fleet(self):
        """Return a list of Battleships from FLEET"""
        return [Ship(ship[0], ship[1]) for ship in Game.FLEET]
