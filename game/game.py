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
        self.game_over = False

    def play(self):
        while True:
            print('Game Running')
            break
        print('Game Over')

    def get_player_name(self, num):
        """Prompts player for name, returns the name.

        Keyword arguments:
        num -- Number placeholder for a user
        """
        return input('Player {} enter your name: '.format(num))

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
