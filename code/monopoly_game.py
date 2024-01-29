from player import *
from achievements import Achievements
from board import Board
import os


class Monopoly_Game:
    def __init__(self):
        self.players = []
        self.board = None
        self.achievements = None
        self.chance_cards = []
        self.community_chest_cards = []
        self.dice = []
        self.current_player = None
        self.current_player_index = 0
        self.rounds_played = 0
        folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.add_board(Board(folder_path + r"/data/tile_init.json"))
        self.add_chance_cards([])
        self.add_community_chest_cards([])
        self.load_achievements(folder_path)

    class GameMemento:
        def __init__(self, current_player_index, rounds_played):
            self.current_player_index = current_player_index
            self.rounds_played = rounds_played

    def save_game(self):
        return self.GameMemento(self.current_player_index, self.rounds_played)

    def load_game(self, game_memento, current_player, players, board):
        self.players = players
        self.board = board
        self.current_player = current_player
        self.current_player_index = game_memento.current_player_index
        self.rounds_played = game_memento.rounds_played

    def add_player(self, player_name, image_name, is_human):
        player_id = len(self.players)
        if is_human:
            self.players.append(HumanPlayer(player_id, player_name, image_name))
        else:
            self.players.append(AIPlayer(player_id, player_name, image_name))

        if self.current_player is None:
            self.current_player = self.players[0]
            self.current_player_index = 0

    def load_achievements(self, folder_path):
        self.achievements = Achievements(folder_path)

    def reset_game(self):
        # remove all the players
        self.remove_all_players()
        self.current_player = None
        self.current_player_index = 0
        self.rounds_played = 0

        # reset the board
        folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.add_board(Board(folder_path + r"/data/tile_init.json"))

    def remove_all_players(self):
        self.players = []
        self.current_player = None

    def add_board(self, board):
        self.board = board

    def add_chance_cards(self, chance_cards):
        self.chance_cards = chance_cards

    def add_community_chest_cards(self, community_chest_cards):
        self.community_chest_cards = community_chest_cards

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.current_player = self.players[self.current_player_index]
