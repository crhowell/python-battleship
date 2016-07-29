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
        self.players = self.initialize_players()
        self.clear_screen()
        self.place_ships()
        self.game_over = False

    def play(self):
        print('Game Running')
        board = self.enemy_board()
        i = 0
        while not self.game_over:
            self.print_game_board()
            move = self.get_player_move()
            while not board.check_move(move):
                print('{} is an invalid move, try again.'.format(move))
                move = self.get_player_move()
            cell = board.move_pos(move)
            token = board.get_indicator(cell)
            self.update_boards(cell, token)
            self.switch_players()
            board = self.enemy_board()
            if i == 10:
                self.game_over = True
            i += 1


        print('Game Over')

    def update_boards(self, cell, token):
        self.players[1]['board'].place_token(cell, token)
        self.players[0]['moves'].place_token(cell, token)


    def current_board(self):
        return self.players[0]['board']

    def enemy_board(self):
        enemy = self.players[1]
        return enemy['board']

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
        for player in self.players:
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


    def mask_row(self, row):
        mask_pieces = [
            Board.INDICATORS['vship'],
            Board.INDICATORS['hship']
        ]
        new_row = [cell if cell not in mask_pieces else
                   Board.INDICATORS['empty'] for cell in row]
        return new_row

    def clear_screen(self):
        """Clears the terminal screen."""
        print("\033c", end="")

    def prompt_to_continue(self, message):
        input('{} {}'.format(message, 'Press ENTER to continue...'))

    def print_placement_header(self, player):
        print('-' * 25, '\n')
        print('{} PLACE YOUR BATTLESHIPS\n'.format(player))
        print('-' * 25, '\n')

    def print_board_heading(self, board):
        """Displays the heading section of the board"""
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

    def print_game_board(self):
        print('-' * 25, '\n', 'Shots at Enemy\n', '-' * 25, '\n')
        print(self.print_board(self.players[0]['moves']))
        print('=' * 25)
        print(self.print_board(self.players[0]['board']))
        print('-' * 25, '\nShots at You\n', '-' * 25)

    def initialize_players(self):
        players = []
        for i in range(Game.MAX_PLAYERS):
            name = Player(self.get_player_name(i + 1))
            players.append({
                'player': name,
                'board': Board(),
                'moves': Board(),
                'fleet': self.build_new_fleet()
            })
        return players

    def build_new_fleet(self):
        """Return a list of Battleships from FLEET"""
        return [Ship(ship[0], ship[1]) for ship in Game.FLEET]
