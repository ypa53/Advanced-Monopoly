from monopoly_game import Monopoly_Game
from gui import GUI


def main():
    game = Monopoly_Game()
    game_gui = GUI(game)

    game_gui.main_menu()
    pass


if __name__ == "__main__":
    main()
