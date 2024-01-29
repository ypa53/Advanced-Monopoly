import json
from player import *

class SaveLoad:

    def __init__(self):
        self.file_path = None

    @staticmethod
    def save_file(file_path, GUI, game, board, players):
        GUIMemento = GUI.save_gui()
        gameMemento = game.save_game()
        boardMemento = board.save_board()
        playerMementos = []
        for player in players:
            playerMementos.append(player.save_player())

        # Create dictionaries to store the memento data
        gui_data = {
            "human_rolled": GUIMemento.human_rolled,
            "rolled_double": GUIMemento.rolled_double,
            "AI_rolled_double": GUIMemento.AI_rolled_double,
            "action_button_flag": GUIMemento.action_button_flag,
            "drew_card": GUIMemento.drew_card,
            "made_decision": GUIMemento.made_decision,
            "dice1": GUIMemento.dice1,
            "dice2": GUIMemento.dice2
        }

        game_data = {
            "current_player_index": gameMemento.current_player_index,
            "rounds_played": gameMemento.rounds_played
        }

        board_data = [{"type": tile.type,
                        "owner_id": tile.owner_id,
                        "num": tile.num,
                        "set_num": tile.set_num,
                        "houses": tile.houses,
                        "set_owned": tile.set_owned,
                        "position": tile.position
                       } for tile in boardMemento]

        player_data = []
        for player in playerMementos:
            player_data.append({
                "player_id": player.player_id,
                "name": player.name,
                "balance": player.balance,
                "asset": player.asset,
                "rounds_in_jail": player.rounds_in_jail,
                "position": player.position,
                "out_of_jail_cards": player.out_of_jail_cards,
                "is_bankrupt": player.is_bankrupt,
                "properties": player.properties,
                "image_name": player.image_name
            })

        # Combine all data into a single dictionary
        data = {
            "gui_data": gui_data,
            "game_data": game_data,
            "board_data": board_data,
            "player_data": player_data
        }

        # Convert the dictionary to JSON format
        json_data = json.dumps(data, indent=4)

        # Write the JSON data to the file
        with open(file_path, "w") as file:
            file.write(json_data)

    @staticmethod
    def load_file(file_path, GUI, game, board, players):
        with open(file_path, "r") as file:
            json_data = json.load(file)

        gui_data = json_data["gui_data"]
        game_data = json_data["game_data"]
        board_data = json_data["board_data"]
        player_data = json_data["player_data"]
        player_classes = [HumanPlayer, AIPlayer]

        for i, player_info in enumerate(player_data):
            player_class = player_classes[i]
            player = player_class(player_info["player_id"], player_info["name"], player_info["image_name"])
            player_memento = player.save_player()

            for key in player_info:
                setattr(player_memento, key, player_info[key])

            player.load_player(player_memento)
            players.append(player)  # These are added to the actual game list of players

        # Load the board
        for datum in board_data:
            tile = board.spaces[datum["position"]]
            tile_memento = tile.save_tile()

            for key in datum:
                setattr(tile_memento, key, datum[key])

            if tile_memento.owner_id == -1:
                owner = None
            else:
                owner = players[tile_memento.owner_id]

            tile.load_tile(tile_memento, owner)

        # Load the game
        game_memento = game.save_game()
        for key in game_data:
            setattr(game_memento, key, game_data[key])

        game.load_game(game_memento, players[game_memento.current_player_index], players, board)

        # Load the GUI
        gui_memento = GUI.save_gui()
        for key in gui_data:
            setattr(gui_memento, key, gui_data[key])

        GUI.load_gui(gui_memento, game)


