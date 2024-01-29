from time import sleep
import pygame as pg
import os
from os import environ
from monopoly_game import Monopoly_Game

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # Hide pygame support prompt
from button import *
from dice import *
from saves import SaveLoad

class GUI:
    def __init__(self, game):
        self.game = game
        self.screen = None
        self.folder_path = None
        self.folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.board_game = pg.image.load(self.folder_path + r"/img/board_game.jpg")
        self.board_menu = pg.image.load(self.folder_path + r"/img/board_menu.jpg")
        self.running = True
        self.clock = pg.time.Clock()
        self.human_rolled = False
        self.rolled_double = 0
        self.AI_rolled_double = 0
        self.action_button_flag = 0
        self.drew_card = 0
        self.made_decision = False

        self.dice1 = 0
        self.dice2 = 0

        pg.init()
        self.screen = pg.display.set_mode((1200, 800))
        pg.display.set_caption("Monopoly")
    class GUIMemento:
        def __init__(self, human_rolled, rolled_double, AI_rolled_double, action_button_flag, drew_card, made_decision, dice1, dice2):
            self.human_rolled = human_rolled
            self.rolled_double = rolled_double
            self.AI_rolled_double = AI_rolled_double
            self.action_button_flag = action_button_flag
            self.drew_card = drew_card
            self.made_decision = made_decision
            self.dice1 = dice1
            self.dice2 = dice2
    def save_gui(self):
        return self.GUIMemento(self.human_rolled, self.rolled_double,
                               self.AI_rolled_double, self.action_button_flag, self.drew_card, self.made_decision, self.dice1, self.dice2)

    def load_gui(self, guiMemento, game):
        self.game = game
        self.human_rolled = guiMemento.human_rolled
        self.rolled_double = guiMemento.rolled_double
        self.AI_rolled_double = guiMemento.AI_rolled_double
        self.action_button_flag = guiMemento.action_button_flag
        self.drew_card = guiMemento.drew_card
        self.made_decision = guiMemento.made_decision
        self.dice1 = guiMemento.dice1
        self.dice2 = guiMemento.dice2

    def save_gamefile(self):
        file_path = self.folder_path + "/data/save_states/save_state.json"
        SaveLoad.save_file(file_path=file_path, GUI=self, game=self.game, board=self.game.board, players=self.game.players)
        print("Game saved!")

    def load_game(self, file="data/save_states/save_state.json"):
        file_path = self.folder_path + "/" + file
        SaveLoad.load_file(file_path=file_path, GUI=self, game=self.game, board=self.game.board, players=self.game.players)
        self.new_game()

    def main_menu(self):
        new_game_button = Button(525, 280, 150, 50, "New Game")
        load_game_button = Button(525, 340, 150, 50, "Load Game")
        help_button = Button(525, 400, 150, 50, "Help")
        demo_button = Button(525, 460, 150, 50, "Demos")
        achievements_button = Button(525, 520, 150, 50, "Achievements")
        quit_button = Button(525, 580, 150, 50, "Quit")

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEMOTION:
                    if new_game_button.handle_event(event):
                        self.initialize_game()
                    if load_game_button.handle_event(event):
                        self.load_game()
                    if quit_button.handle_event(event):
                        self.running = False
                    if demo_button.handle_event(event):
                        self.demo_page()
                    if achievements_button.handle_event(event):
                        self.achievements()
                    if help_button.handle_event(event):
                        self.show_rules()

            # draw menu background image
            self.screen.blit(self.board_menu, (0, 0))

            new_game_button.draw(self.screen)
            load_game_button.draw(self.screen)
            quit_button.draw(self.screen)
            demo_button.draw(self.screen)
            achievements_button.draw(self.screen)
            help_button.draw(self.screen)
            pg.display.update()

    def demo_page(self):
        #display 3 buttons with descriptions under them

        #button 1
        endgame_button = Button(325, 280, 150, 50, "End Game")
        endgame_text = "Its a close game, can you get the win?"
        #button 2
        build_haven_button = Button(325, 380, 150, 50, "Build Haven")
        build_haven_text = "$10,000. All Streets owned. Build away!"

        #button 3
        AI_panic_button = Button(325, 480, 150, 50, "AI Panic")
        AI_panic_text = "The AI is in debt. Watch it panic sell!"

        #back button
        back_button = Button(525, 580, 150, 50, "Back")

        #put the text to the right of the buttons
        font1 = pg.font.SysFont('Comic Sans MS', 21)
        endgame_text = font1.render(endgame_text, False, (0, 0, 0))
        build_haven_text = font1.render(build_haven_text, False, (0, 0, 0))
        AI_panic_text = font1.render(AI_panic_text, False, (0, 0, 0))

        #draw the menu
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEMOTION:
                    if endgame_button.handle_event(event):
                        self.load_game(file="data/save_states/end_game.json")
                    if build_haven_button.handle_event(event):
                        self.load_game(file="data/save_states/build_haven.json")
                    if AI_panic_button.handle_event(event):
                        self.load_game(file="data/save_states/ai_panic.json")
                    if back_button.handle_event(event):
                        return

            # draw menu background image
            self.screen.blit(self.board_menu, (0, 0))

            endgame_button.draw(self.screen)
            build_haven_button.draw(self.screen)
            AI_panic_button.draw(self.screen)
            back_button.draw(self.screen)

            #draw the text
            self.screen.blit(endgame_text, (480, 285))
            self.screen.blit(build_haven_text, (480, 385))
            self.screen.blit(AI_panic_text, (480, 485))

            pg.display.update()


        pass

    def achievements(self):
        achievement_page = (pg.image.load(self.folder_path + r"/img/achievement/blank_menu.png"))
        back_button = Button(900, 720, 200, 50, "Back")

        self.game.load_achievements(self.folder_path)

        achievement_data = self.game.achievements.get_achievement_data()

        # draw trophies and text onto achievement page
        achievement_spacing = 120  # Vertical spacing between achievements
        achievement_margin = 500  # Horizontal margin between columns

        for i in range(len(achievement_data)):
            row = i // 2  # Determine the row (0, 1, 2, ...) for the achievement
            column = i % 2  # Determine the column (0 or 1) for the achievement

            if achievement_data[i]["Completed"]:
                trophy = pg.image.load(self.folder_path + r"/img/achievement/trophy.png")
            else:
                trophy = pg.image.load(self.folder_path + r"/img/achievement/trophy_grey.png")

            x_offset = 150 + column * achievement_margin  # X-coordinate for trophy and text
            y_offset = 150 + row * achievement_spacing  # Y-coordinate for trophy and text

            achievement_page.blit(trophy, (x_offset, y_offset))

            font1 = pg.font.SysFont('Comic Sans MS', 22)
            font2 = pg.font.SysFont('Comic Sans MS', 28)
            description = font1.render(achievement_data[i]["Description"], False, (0, 0, 0))
            name = font2.render(achievement_data[i]["Name"], False, (0, 0, 0))

            text_x_offset = x_offset + 100  # X-coordinate for text
            text_y_offset = y_offset + 25  # Y-coordinate for text

            achievement_page.blit(description, (text_x_offset, text_y_offset + 15))
            achievement_page.blit(name, (text_x_offset, text_y_offset - 15))

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEMOTION:
                    if back_button.handle_event(event):
                        return

            self.screen.blit(achievement_page, (0, 0))
            back_button.draw(self.screen)
            pg.display.update()

    def initialize_game(self):

        # reset the GUI flags
        self.human_rolled = False
        self.rolled_double = 0
        self.AI_rolled_double = 0
        self.action_button_flag = 0
        self.drew_card = 0
        self.made_decision = False
        self.dice1 = 0
        self.dice2 = 0

        player_name = ""
        player_piece = ""

        self.screen.blit(self.board_menu, (0, 0))

        font1 = pg.font.SysFont('Comic Sans MS', 30)

        name_text = font1.render('Please enter your name: ', False, (0, 0, 0))
        piece_text = font1.render('You choose: ', False, (0, 0, 0))
        piece_text2 = font1.render('Please select your piece:', False, (0, 0, 0))

        self.screen.blit(name_text, (420, 260))
        self.screen.blit(piece_text, (480, 540))
        self.screen.blit(piece_text2, (420, 420))

        input_rect = pg.Rect(440, 320, 300, 60)
        color = pg.Color((255, 255, 255))

        piece_button1 = img_Button(400, 480, 60, 60, pg.image.load(self.folder_path + r"/img/pieces/Cat.png"))
        piece_button2 = img_Button(480, 480, 60, 60, pg.image.load(self.folder_path + r"/img/pieces/ScottieDog.png"))
        piece_button3 = img_Button(560, 480, 60, 60, pg.image.load(self.folder_path + r"/img/pieces/TopHat.png"))
        piece_button4 = img_Button(640, 480, 60, 60, pg.image.load(self.folder_path + r"/img/pieces/Battleship.png"))
        piece_button5 = img_Button(720, 480, 60, 60, pg.image.load(self.folder_path + r"/img/pieces/RubberDucky.png"))
        new_game_button = Button(500, 600, 200, 60, "Let's get started!")

        pg.display.update()

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEMOTION:
                    if piece_button1.handle_event(event):
                        player_piece = "Cat"
                        piece_text = font1.render('You choose: Cat               ', False, (0, 0, 0), (205, 230, 208))
                        self.screen.blit(piece_text, (440, 540))
                        pg.display.flip()
                    if piece_button2.handle_event(event):
                        player_piece = "ScottieDog"
                        piece_text = font1.render('You choose: Scottia Dog  ', False, (0, 0, 0), (205, 230, 208))
                        self.screen.blit(piece_text, (440, 540))
                        pg.display.flip()
                    if piece_button3.handle_event(event):
                        player_piece = "TopHat"
                        piece_text = font1.render('You choose: Top Hat          ', False, (0, 0, 0), (205, 230, 208))
                        self.screen.blit(piece_text, (440, 540))
                        pg.display.flip()
                    if piece_button4.handle_event(event):
                        player_piece = "Battleship"
                        piece_text = font1.render('You choose: Battleship        ', False, (0, 0, 0), (205, 230, 208))
                        self.screen.blit(piece_text, (440, 540))
                        pg.display.flip()
                    if piece_button5.handle_event(event):
                        player_piece = "RubberDucky"
                        piece_text = font1.render('You choose: Rubber Duck', False, (0, 0, 0), (205, 230, 208))
                        self.screen.blit(piece_text, (440, 540))
                        pg.display.flip()
                    if new_game_button.handle_event(event):
                        if player_name == "":
                            piece_text = font1.render("Please enter a name!         ", False, (0, 0, 0),
                                                      (205, 230, 208))
                            self.screen.blit(piece_text, (440, 540))
                            pg.display.flip()
                        elif player_piece == "":
                            piece_text = font1.render("Please select a piece!          ", False, (0, 0, 0),
                                                      (205, 230, 208))
                            self.screen.blit(piece_text, (440, 540))
                            pg.display.flip()
                        else:
                            # add the human player to the game
                            #player_image = pg.image.load(self.folder_path + r"/img/pieces/" + player_piece + ".png")
                            image_name = player_piece + ".png"
                            self.game.add_player(player_name, image_name, True)

                            # add one AI player to the game
                            AI_piece = "ScottieDog" if player_piece == "Cat" else "Cat"
                            AI_image_name = AI_piece + ".png"
                            self.game.add_player("AI", AI_image_name, False)
                            self.new_game()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        player_name = player_name[0:-1]
                    else:
                        player_name += event.unicode
                if len(player_name) >= 10:
                    player_name = player_name[0:14]
                pg.draw.rect(self.screen, color, input_rect)
                text_surface = font1.render(player_name, True, (0, 0, 0))
                self.screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
                input_rect.w = max(100, text_surface.get_width() + 10)
                pg.display.flip()

            piece_button1.draw(self.screen)
            piece_button2.draw(self.screen)
            piece_button3.draw(self.screen)
            piece_button4.draw(self.screen)
            piece_button5.draw(self.screen)
            new_game_button.draw(self.screen)

    def new_game(self):
        font2 = pg.font.SysFont('Comic Sans MS', 20)

        roll_dice_button = Button(810, 430, 150, 35, "Roll Dice")
        end_turn_button = Button(810, 490, 150, 35, "End Turn")
        sell_button = Button(810, 540, 150, 35, "Sell")
        build_button = Button(810, 590, 150, 35, "Build")

        sell_button.change(unavail)
        build_button.change(unavail)

        save_game_button = Button(810, 640, 150, 35, "Save Game")

        achievements_button = Button(810, 690, 150, 35, "Achievements")
        rule_button = Button(940, 740, 120, 35, "Rules")
        main_menu_button = Button(810, 740, 120, 35, "Main Menu")
        exit_game_button = Button(1070, 740, 120, 35, "Exit Game")

        yes_button = Button(810, 300, 150, 35, "Yes")
        no_button = Button(810, 350, 150, 35, "No")
        jail_pay_button = Button(970, 300, 150, 35, "Pay $50")
        jail_roll_dice_button = Button(970, 350, 150, 35, "Roll Dice")

        property = img(450, 300, 175, 257, pg.image.load(self.folder_path + r"/img/title deed/B.jpg"))
        propertyOwner=font2.render(str(""), False, (0, 0, 0))
        chest_button = img_Button(160, 300, 220, 150, pg.image.load(self.folder_path + r"/img/chest/chest.jpg"))
        chest_button.change(unavail)
        chance_button = img_Button(160, 500, 220, 150, pg.image.load(self.folder_path + r"/img/chance/chance.jpg"))
        chance_button.change(unavail)
        dice1_img = img(460, 590, 60, 60, pg.image.load(self.folder_path + r"/img/dice/1.png"))
        dice2_img = img(560, 590, 60, 60, pg.image.load(self.folder_path + r"/img/dice/1.png"))

        if self.human_rolled == True:
            roll_dice_button.change(unavail)
        else:
            end_turn_button.change(unavail)

        def draw_board():
            # draw menu background image
            self.screen.blit(self.board_game, (0, 0))
            # draw the board
            roll_dice_button.draw(self.screen)
            end_turn_button.draw(self.screen)
            sell_button.draw(self.screen)
            build_button.draw(self.screen)
            exit_game_button.draw(self.screen)
            save_game_button.draw(self.screen)
            achievements_button.draw(self.screen)
            rule_button.draw(self.screen)
            main_menu_button.draw(self.screen)
            property.draw(self.screen)
            chest_button.draw(self.screen)
            chance_button.draw(self.screen)
            dice1_img.draw(self.screen)
            dice2_img.draw(self.screen)
            self.screen.blit(propertyOwner, (450, 270))
            self.draw_properties()
            player_image = pg.image.load(self.folder_path + r"/img/pieces/" + self.game.players[0].image_name)
            AI_image = pg.image.load(self.folder_path + r"/img/pieces/" + self.game.players[1].image_name)

            player_icon = img(990, 430, 60, 60, player_image)
            AI_icon = img(990, 590, 60, 60, AI_image)
            player_icon.draw(self.screen)
            AI_icon.draw(self.screen)
            player_text = font2.render("Cash: $" + str(self.game.players[0].balance), False, (0, 0, 0))
            AI_text = font2.render("Cash: $" + str(self.game.players[1].balance), False, (0, 0, 0))
            player_text2 = font2.render(self.game.players[0].name, False, (0,0,0))
            AI_text2 = font2.render("AI", False, (0,0,0))
            player_text3 = font2.render("Asset: $" + str(self.game.players[0].asset), False, (0, 0, 0))
            AI_text3 = font2.render("Asset: $" + str(self.game.players[1].asset), False, (0, 0, 0))
            self.screen.blit(player_text, (990, 490))
            self.screen.blit(AI_text, (990, 650))
            self.screen.blit(player_text2, (1050,430))
            self.screen.blit(AI_text2, (1050,590))
            self.screen.blit(player_text3, (990, 510))
            self.screen.blit(AI_text3, (990, 670))
            player_out_jail_card = img(1120, 490, 60, 40, pg.image.load(self.folder_path + r"/img/GetOutJailFree.jpg"))
            AI_out_jail_card = img(1120, 650, 60, 40, pg.image.load(self.folder_path + r"/img/GetOutJailFree.jpg"))
            if self.game.players[0].out_of_jail_cards > 0:
                player_out_jail_card.draw(self.screen)
            if self.game.players[1].out_of_jail_cards > 0:
                AI_out_jail_card.draw(self.screen)

            rounds_played = font2.render(str("Round " + str(self.game.rounds_played) + "/30"), False, (0, 0, 0))
            self.screen.blit(rounds_played, (820, 400))

        def draw_opponent(current_player_id):
            player = self.game.players[(current_player_id + 1) % 2]
            position = player.position
            tile = self.game.board.spaces[position]
            tile_center = tile.rect.center
            player_image = pg.image.load(self.folder_path + r"/img/pieces/" + player.image_name)
            self.screen.blit(player_image, (
                tile_center[0] - player_image.get_width() / 2, tile_center[1] - player_image.get_height() / 2))
        def draw_players():
            for player in self.game.players:
                position = player.position
                tile = self.game.board.spaces[position]
                tile_center = tile.rect.center
                player_image = pg.image.load(self.folder_path + r"/img/pieces/" + player.image_name)
                self.screen.blit(player_image, (
                    tile_center[0] - player_image.get_width() / 2, tile_center[1] - player_image.get_height() / 2))

        font2 = pg.font.SysFont('Comic Sans MS', 20)
        selected_tile = None
        while self.running:
            draw_board()

            if selected_tile != None:
                pg.draw.rect(self.screen, (255, 0, 0), selected_tile.rect, 3)
                if (selected_tile.owner == self.game.players[0]) and self.game.current_player == self.game.players[0]:
                    sell_button.change(avail)
                    if self.game.board.can_build(selected_tile.position, self.game.current_player):
                        build_button.change(avail)
                    else:
                        build_button.change(unavail)
                else:
                    sell_button.change(unavail)
                    build_button.change(unavail)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEMOTION:
                    for tile in self.game.board.spaces:
                        if tile.rect.collidepoint(event.pos):
                            # check if tile is street, railroad, or utility
                            if tile.type == "Street" or tile.type == "Railroad" or tile.type == "Utility":
                                #check if clicked on
                                if event.type == pg.MOUSEBUTTONDOWN:
                                    if selected_tile == tile:
                                        selected_tile = None
                                    else:
                                        selected_tile = tile

                                #show title owner
                                if(tile.owner!=None):
                                    owner=tile.owner.name
                                    propertyOwner = font2.render(str("Owner: "+owner), False, (0, 0, 0))
                                    
                                else:
                                    propertyOwner=font2.render(str(""), False, (0, 0, 0))
                                
                                #show title deed
                                property= img(450, 300, 175, 257, pg.image.load(self.folder_path + r"/img/title deed/" + tile.image_name))

                    if roll_dice_button.handle_event(event):
                        self.dice1 = Dice.roll_dice()
                        self.dice2 = Dice.roll_dice()
                        dice1_img.image = pg.image.load(self.folder_path + r"/img/dice/" + str(self.dice1) + ".png")
                        dice2_img.image = pg.image.load(self.folder_path + r"/img/dice/" + str(self.dice2) + ".png")
                        chance_button.image = pg.image.load(self.folder_path + r"/img/chance/chance.jpg")
                        chest_button.image = pg.image.load(self.folder_path + r"/img/chest/chest.jpg")

                        draw_opponent(self.game.current_player.player_id)
                        dice1_img.draw(self.screen)
                        dice2_img.draw(self.screen)
                        background = self.screen.copy() # final GUI image, without current player
                        draw_players()
                        self.simulate_dice_roll(self.dice1, self.dice2)   #draw dice roll

                        # move the player
                        current_player = self.game.current_player
                        self.draw_player_movement(current_player, background, self.dice1 + self.dice2)

                        tile = self.game.board.spaces[current_player.position]
                        if tile.type == "Street" or tile.type == "Railroad" or tile.type == "Utility":
                            if tile.owner != None and tile.owner != current_player:
                                status = tile.operation(current_player)
                                self.handle_operation_status(status, current_player)

                        self.action_button_flag = 1
                        self.drew_card = 0
                        self.made_decision = False
                        yes_button.change(avail)
                        no_button.change(avail)

                        if self.dice1 == self.dice2 and self.rolled_double < 2:
                            self.rolled_double += 1
                            end_turn_button.change(unavail)
                        elif self.dice1 == self.dice2 and self.rolled_double == 2:
                            current_player.go_to_jail()
                            self.rolled_double = 0
                            roll_dice_button.change(unavail)
                            end_turn_button.change(avail)
                            self.human_rolled = True
                        else:
                            roll_dice_button.change(unavail)
                            end_turn_button.change(avail)
                            self.human_rolled = True
                            self.rolled_double = 0

                    elif end_turn_button.handle_event(event):  # TODO: fix needing to press end turn when ai rolls double
                        self.end_turn()
                        ai_turn = True
                        while ai_turn:
                            # print(self.game.current_player.name)
                            chance_button.change(unavail)
                            chest_button.change(unavail)
                            self.action_button_flag = 0
                            chance_button.image = pg.image.load(self.folder_path + r"/img/chance/chance.jpg")
                            chest_button.image = pg.image.load(self.folder_path + r"/img/chest/chest.jpg")
                            sleep(0.5)
                            draw_board()
                            self.dice1 = Dice.roll_dice()
                            self.dice2 = Dice.roll_dice()
                            dice1_img.image = pg.image.load(self.folder_path + r"/img/dice/" + str(self.dice1) + ".png")
                            dice2_img.image = pg.image.load(self.folder_path + r"/img/dice/" + str(self.dice2) + ".png")
                            draw_opponent(self.game.current_player.player_id)
                            dice1_img.draw(self.screen)
                            dice2_img.draw(self.screen)
                            background = self.screen.copy()  # final, sans current player
                            draw_players()  # final
                            self.simulate_dice_roll(self.dice1, self.dice2)

                            # move the player
                            current_player = self.game.current_player
                            self.draw_player_movement(current_player, background, self.dice1 + self.dice2)

                            tile = self.game.board.spaces[current_player.position]
                            if (tile.type == "Chance"):
                                temp = self.game.board.spaces[current_player.position].operation(current_player,self.game.players,self.game.board.spaces)
                                chance_button.image = pg.image.load(temp)
                                chance_button.change(unavail)
                            elif (tile.type == "Community Chest"):
                                temp = self.game.board.spaces[current_player.position].operation(current_player,self.game.players,self.game.board.spaces)
                                chest_button.image = pg.image.load(temp)
                                chest_button.change(unavail)
                            else:
                                if (self.game.players[1].balance > 600):
                                    status = self.game.board.spaces[current_player.position].operation(current_player)
                                    self.handle_operation_status(status, current_player)

                            self.AI_try_build()
                            if self.AI_try_sell() == -1:
                                #AI bankrupt
                                self.end_game()
                                return

                            if self.dice1 == self.dice2 and self.AI_rolled_double < 2:
                                self.AI_rolled_double += 1
                            elif self.dice1 == self.dice2 and self.AI_rolled_double == 2:
                                current_player.go_to_jail()
                                self.AI_rolled_double = 0
                                roll_dice_button.change(avail)
                                end_turn_button.change(unavail)
                                self.human_rolled = False
                                self.end_turn()
                                ai_turn = False
                            else:
                                roll_dice_button.change(avail)
                                end_turn_button.change(unavail)
                                self.human_rolled = False
                                self.AI_rolled_double = 0
                                self.end_turn()
                                ai_turn = False



                    elif chest_button.handle_event(event):

                        current_player = self.game.current_player
                        tile = self.game.board.spaces[current_player.position]
                        temp=tile.operation(current_player,self.game.players,self.game.board.spaces)
                        chest_button.image = pg.image.load(temp)
                        chest_button.change(unavail)
                        self.drew_card = 1
                        if (self.dice1 != self.dice2):
                            end_turn_button.change(avail)
                        else:
                            roll_dice_button.change(avail)

                    elif chance_button.handle_event(event):

                        current_player = self.game.current_player
                        tile = self.game.board.spaces[current_player.position]
                        temp=tile.operation(current_player,self.game.players,self.game.board.spaces)
                        chance_button.image = pg.image.load(temp)
                        chance_button.change(unavail)
                        self.drew_card = 2
                        if (self.dice1 != self.dice2):
                            end_turn_button.change(avail)
                        else:
                            roll_dice_button.change(avail)

                    elif sell_button.handle_event(event):
                        self.sell(selected_tile)
                    elif build_button.handle_event(event):
                        self.build(selected_tile)
                    elif save_game_button.handle_event(event):
                        self.save_gamefile()
                    elif achievements_button.handle_event(event):
                        self.calculate_assets(self.game.players[0])
                        self.calculate_assets(self.game.players[1])
                        self.achievements()
                    elif rule_button.handle_event(event):
                        self.show_rules()
                    elif main_menu_button.handle_event(event):
                        self.game.reset_game()
                        self.reset_gui()
                        self.main_menu()
                    elif exit_game_button.handle_event(event):
                        self.running = False
                    elif yes_button.handle_event(event):
                        current_player = self.game.current_player
                        status = self.game.board.spaces[current_player.position].operation(current_player)
                        self.handle_operation_status(status, current_player)
                        yes_button.change(unavail)
                        no_button.change(unavail)
                        self.made_decision = True
                        if (self.human_rolled == True):
                            end_turn_button.change(avail)
                        else:
                            roll_dice_button.change(avail)

                    elif no_button.handle_event(event):
                        yes_button.change(unavail)
                        no_button.change(unavail)
                        self.made_decision = True
                        if (self.human_rolled == True):
                            end_turn_button.change(avail)
                        else:
                            roll_dice_button.change(avail)

                    elif jail_pay_button.handle_event(event):
                        self.made_decision = True
                        self.game.players[0].set_balance(self.game.players[0].get_balance()-50)
                        self.game.players[0].set_asset(self.game.players[0].get_asset()-50)
                        self.game.players[0].round_in_jail = 0
                        jail_pay_button.change(unavail)
                        jail_roll_dice_button.change(unavail)
                        roll_dice_button.change(avail)

                    elif jail_roll_dice_button.handle_event(event):
                        self.made_decision = True
                        jail_pay_button.change(unavail)
                        jail_roll_dice_button.change(unavail)
                        if self.game.players[0].rounds_in_jail > 0:
                            self.dice1 = Dice.roll_dice()
                            self.dice2 = Dice.roll_dice()
                            dice1_img.image = pg.image.load(self.folder_path + r"/img/dice/" + str(self.dice1) + ".png")
                            dice2_img.image = pg.image.load(self.folder_path + r"/img/dice/" + str(self.dice2) + ".png")
                            if self.dice1 == self.dice2:
                                self.game.players[0].rounds_in_jail = 0
                                roll_dice_button.change(avail)
                            self.game.players[0].rounds_in_jail -= 1
                            end_turn_button.change(avail)
                        else:
                            self.game.players[0].set_balance(self.game.players[0].get_balance()-50)
                            self.game.players[0].set_asset(self.game.players[0].get_asset()-50)
                            self.game.players[0].round_in_jail = 0
                            roll_dice_button.change(avail)

            # draw the player pieces
            for player in self.game.players:
                # get the player tile position
                position = player.position
                # get the tile in that position
                tile = self.game.board.spaces[position]
                # draw the player piece in the centre of the tile rect
                tile_center = tile.rect.center
                player_image = pg.image.load(self.folder_path + r"/img/pieces/" + player.image_name)
                self.screen.blit(player_image, (tile_center[0] - player_image.get_width() / 2, tile_center[1] - player_image.get_height() / 2))
                if player.player_id == 0:
                    player_location = font2.render(str("You are at: " + tile.name + "              "), False, (0, 0, 0), (205, 230, 208))
                    self.screen.blit(player_location, (820, 10))
                    if tile.type == "Street" or tile.type == "Railroad" or tile.type == "Utility":
                        if tile.owner == None:  # TODO: use operation() function to check if tile is owned
                            info = font2.render(str("Do you want to buy:"), False, (0, 0, 0), (205, 230, 208))
                            info2 = font2.render(str(tile.name + "              "), False, (0, 0, 0), (205, 230, 208))
                            if (self.made_decision == False):
                                end_turn_button.change(unavail)
                                roll_dice_button.change(unavail)
                            if (self.action_button_flag == 1):
                                yes_button.draw(self.screen)
                                no_button.draw(self.screen)
                            self.screen.blit(info, (820, 80))
                            self.screen.blit(info2, (820, 110))
                        elif tile.owner == self.game.players[1]:
                            info = font2.render(str("Sorry, please pay rent.     ") , False, (0, 0, 0), (205, 230, 208))
                            self.screen.blit(info, (820, 80))
                        else:
                            info = font2.render(str("Enjoy a break at your property!   ") , False, (0, 0, 0), (205, 230, 208))
                            self.screen.blit(info, (820, 80))
                    elif tile.type == "Chance":
                        if (self.drew_card != 2):
                            info = font2.render(str("Please draw a Chance card."), False, (0, 0, 0), (205, 230, 208))
                            self.screen.blit(info, (820, 80))
                            chance_button.change(avail)
                            end_turn_button.change(unavail)
                            roll_dice_button.change(unavail)
                    elif tile.type == "Community Chest":
                        if (self.drew_card != 1):
                            info = font2.render(str("Please draw a Chest card."), False, (0, 0, 0), (205, 230, 208))
                            self.screen.blit(info, (820, 80))
                            chest_button.change(avail)
                            end_turn_button.change(unavail)
                            roll_dice_button.change(unavail)
                    elif tile.type == "Tax":
                        info = font2.render(str("Please pay the tax."), False, (0, 0, 0), (205, 230, 208))
                        self.screen.blit(info, (820, 80))
                        if (self.made_decision == False):
                            end_turn_button.change(unavail)
                            roll_dice_button.change(unavail)
                        if (self.action_button_flag == 1):
                            yes_button.draw(self.screen)
                    else:
                        tile.operation(player)
                        if tile.at_start == True:
                            info = font2.render(str("Let's start!"), False, (0, 0, 0), (205, 230, 208))
                            self.screen.blit(info, (820, 80))
                        elif tile.at_parking == True:
                            info = font2.render(str("Free parking!"), False, (0, 0, 0), (205, 230, 208))
                            self.screen.blit(info, (820, 80))
                        elif tile.at_jail == True and player.check_in_jail() == False:
                            info = font2.render(str("Relax! You are not in jail."), False, (0, 0, 0), (205, 230, 208))
                            self.screen.blit(info, (820, 80))
                        elif tile.at_jail == True and player.check_in_jail() == True:
                            self.game.achievements.complete_achievement("jailBird")
                            if (player.out_of_jail_cards) > 0:
                                player.use_jail_card()
                            else:
                                info = font2.render(str("You are in jail."), False, (0, 0, 0), (205, 230, 208))
                                self.screen.blit(info, (820, 80))
                                if (self.made_decision == False):
                                    jail_pay_button.change(avail)
                                    jail_roll_dice_button.change(avail)
                                    end_turn_button.change(unavail)
                                    roll_dice_button.change(unavail)
                                if (player.check_in_jail() == True):
                                    jail_pay_button.draw(self.screen)
                                    jail_roll_dice_button.draw(self.screen)
                        elif tile.at_go_to_jail == True:
                            info = font2.render(str("Sorry. Go to jail!   "), False, (0, 0, 0), (205, 230, 208))
                            self.screen.blit(info, (820, 80))
                            player.go_to_jail()


                if player.player_id == 1:
                    player_location = font2.render(str("AI is at: " + tile.name + "              "), False, (0, 0, 0), (205, 230, 208))
                    self.screen.blit(player_location, (820, 40))
                    if player.position == 30:
                        player.go_to_jail()
                    if player.check_in_jail() == True:
                        if (player.out_of_jail_cards) > 0:
                            player.use_jail_card()
                        else:
                            player.set_balance(player.get_balance()-50)
                            player.set_asset(player.get_asset()-50)
                            player.rounds_in_jail = 0

            # update the screen
            pg.display.update()
            self.clock.tick(30)
    def reset_gui(self):
        self.human_rolled = False
        self.rolled_double = 0
        self.AI_rolled_double = 0
        self.action_button_flag = 0
        self.drew_card = 0
        self.made_decision = False
        self.dice1 = 0
        self.dice2 = 0

    def draw_properties(self):
        x_offsets = [18, 83, 18, 2]  # positions + offsets for drawing houses/hotels
        y_offsets = [2, 18, 83, 18]
        i = -1
        for position, tile in enumerate(self.game.board.spaces):
            if not (position % 10) and position != 40:
                i += 1

            if tile.type == "Street":
                # want to draw house and hotel images onto the tile rect
                # get the number of houses and hotels on the tile
                num_of_properties = tile.houses
                building_image = pg.image.load(self.folder_path + r"/img/building/building" + str(num_of_properties) + ".jpg")
                self.screen.blit(building_image, (tile.rect.x + x_offsets[i], tile.rect.y + y_offsets[i]))

    def simulate_dice_roll(self, actual_d1, actual_d2):
        # draw random dice roll onto the screen
        for i in range(5):
            dice1 = Dice.roll_dice()
            dice2 = Dice.roll_dice()
            dice1_img = img(460, 590, 60, 60, pg.image.load(self.folder_path + r"/img/dice/" + str(dice1) + ".png"))
            dice2_img = img(560, 590, 60, 60, pg.image.load(self.folder_path + r"/img/dice/" + str(dice2) + ".png"))
            dice1_img.draw(self.screen)
            dice2_img.draw(self.screen)
            pg.display.update()
            sleep(0.1)

        dice1_img = img(460, 590, 60, 60, pg.image.load(self.folder_path + r"/img/dice/" + str(actual_d1) + ".png"))
        dice2_img = img(560, 590, 60, 60, pg.image.load(self.folder_path + r"/img/dice/" + str(actual_d2) + ".png"))
        dice1_img.draw(self.screen)
        dice2_img.draw(self.screen)

    def draw_player_movement(self, player, background, dice_sum):
        initial_position = player.position
        if (initial_position + dice_sum >= 40):
                player.set_balance(player.get_balance() +200)
                player.set_asset(player.get_asset() +200)
        for i in range(initial_position, initial_position + dice_sum + 1):
            player.move_player_to(i % 40)
            self.screen.blit(background, (0, 0))
            # self.draw_properties()
            for p in self.game.players:
                tile_center = self.game.board.spaces[p.position].rect.center
                player_image = pg.image.load(self.folder_path + r"/img/pieces/" + p.image_name)
                self.screen.blit(player_image, (tile_center[0] - player_image.get_width() / 2, tile_center[1] - player_image.get_height() / 2))
            pg.display.update()
            sleep(0.2)

    def sell(self, selected_tile):

        if selected_tile.type == "Railroad":
            self.game.board.update_Railroad_num(selected_tile.position)

        if selected_tile.type == "Utility" or selected_tile.type == "Railroad":
            self.game.board.set_sets_to_false(selected_tile.position)
            owner = selected_tile.owner
            #owner will get back half of the price
            owner.set_balance(owner.get_balance() + int(selected_tile.price / 2))
            owner.set_asset(owner.get_asset() - int(selected_tile.price / 2)) # because -price + price/2 = -1/2 price
            selected_tile.remove_owner()
            if owner == self.game.players[0]:
                self.game.achievements.complete_achievement("sellProperty")
            return

        if not(self.game.board.can_sell(selected_tile.position)):
            print("Cant sell")
        elif selected_tile.houses:
            selected_tile.houses -= 1
            selected_tile.owner.set_balance(selected_tile.owner.get_balance() + int(selected_tile.build_price / 2))
            selected_tile.owner.set_asset(selected_tile.owner.get_asset() - int(selected_tile.build_price / 2))
        else:
            self.game.board.set_sets_to_false(selected_tile.position)
            owner = selected_tile.owner
            # owner will get back half of the price
            owner.set_balance(owner.get_balance() + int(selected_tile.price / 2))
            owner.set_asset(owner.get_asset() - int(selected_tile.price / 2))
            selected_tile.remove_owner()
            if owner == self.game.players[0]:
                self.game.achievements.complete_achievement("sellProperty")

    def build(self, selected_tile):
        # build one house on the selected tile
        if selected_tile.owner == self.game.players[0]:
            self.game.achievements.complete_achievement("buildHouse")
        selected_tile.houses += 1
        selected_tile.owner.set_balance(selected_tile.owner.get_balance() - selected_tile.build_price)

    def handle_operation_status(self, status, current_player):
        # if status == 0, property was bought, so update rent
        if status == 0:
            #check if players position is a property
            tile = self.game.board.spaces[current_player.position]
            if tile.type == "Street" or tile.type == "Railroad" or tile.type == "Utility":

                all_owned = self.game.board.update_sets(current_player.position)
                self.game.achievements.complete_achievement("buyProperty")

                #check if all properties in set are owned by same player
                if all_owned:
                    self.game.achievements.complete_achievement("getMonopoly")
            return

        # if status == -1, player doesn't have enough money to buy property
        if status == -1:
            print("Not enough money")

        # if status == -2, player doesn't have enough money to pay rent
        if status == -2:
            print("Not enough money for rent")
            self.try_sell()

    def try_sell(self):
        #while player is in debt, let them sell things
        print("Please sell some property to continue")

    def AI_try_build(self):
        # AI will try to build on all properties it owns while it has enough money (>1000)

        can_build = True
        while self.game.current_player.get_balance() > 1000 and can_build:
            can_build = False
            for tile in self.game.board.spaces:
                if tile.type == "Street" or tile.type == "Railroad" or tile.type == "Utility":
                    if tile.owner == self.game.current_player:
                        if self.game.board.can_build(tile.position, self.game.current_player):

                            #check if AI will have >1000 after building
                            if self.game.current_player.get_balance() - tile.build_price > 1000:
                                can_build = True
                                self.build(tile)
                                self.draw_properties()
                                pg.display.update()
                                sleep(0.5)

    def AI_try_sell(self):
        # AI will try to sell things when it is in debt
        if self.game.current_player.get_balance() >= 0:
            return

        def AI_sold_enough():
            #check if AI has enough money to pay off debt
            return self.game.current_player.get_balance() > 200


        AI_owned_properties = []
        for tile in self.game.board.spaces:
            if tile.type == "Street" or tile.type == "Railroad" or tile.type == "Utility":
                if tile.owner == self.game.current_player:
                    AI_owned_properties.append(tile)


        #else, try to sell properties that are not in a set
        for tile in AI_owned_properties.copy():
            if tile.set_owned == False:
                print("AI sold " + tile.name)
                self.sell(tile)
                AI_owned_properties.remove(tile)
                self.draw_properties()
                pg.display.update()
                sleep(0.2)
                if AI_sold_enough():
                    print("AI sold enough")
                    return 0

        #else, try to sell houses
        can_sell_house = True
        while can_sell_house:
            can_sell_house = False
            for tile in AI_owned_properties.copy():
                if tile.houses:
                    can_sell_house = True
                    if self.game.board.can_sell(tile.position):
                        print("AI sold a house on " + tile.name)
                        self.sell(tile)
                        self.draw_properties()
                        pg.display.update()
                        sleep(0.2)
                        if AI_sold_enough():
                            print("AI sold enough")
                            return 0

        AI_owned_properties.reverse()

        #else, try to sell properties that are in a set
        for tile in AI_owned_properties.copy():
            print("AI sold " + tile.name)
            self.sell(tile)
            AI_owned_properties.remove(tile)
            self.draw_properties()
            pg.display.update()
            sleep(0.2)
            if AI_sold_enough():
                print("AI sold enough")
                return 0

        #if we get here, the AI has no more properties to sell
        if self.game.current_player.get_balance() < 0:
            print("AI is bankrupt")
            return -1

    def calculate_assets(self, player):
        assets = player.get_balance()
        for tile in self.game.board.spaces:
            if tile.type == "Street" or tile.type == "Railroad" or tile.type == "Utility":
                if tile.owner == player:
                    assets += tile.price
                    if tile.type == "Street":
                        assets += tile.houses * tile.build_price
        print("Player " + str(player.player_id) + " has " + str(assets) + " assets")


    def show_rules(self):
        self.help_page = (pg.image.load(self.folder_path + r"/img/help/1.jpg"))
        page_num = 1

        previous_button = Button(350, 620, 50, 50, "<--")
        next_button = Button(800, 620, 50, 50, "-->")
        back_button = Button(500, 620, 200, 50, "Back")

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEMOTION:
                    if back_button.handle_event(event):
                        return
                    if previous_button.handle_event(event):
                        next_button.change(avail)
                        if page_num != 1:
                            page_num -= 1
                            self.help_page = (pg.image.load(self.folder_path + r"/img/help/" + str(page_num) + ".jpg"))
                        else:
                            previous_button.change(unavail)
                    if next_button.handle_event(event):
                        previous_button.change(avail)
                        if page_num != 9:
                            page_num += 1
                            self.help_page = (pg.image.load(self.folder_path + r"/img/help/" + str(page_num) + ".jpg"))
                        else:
                            next_button.change(unavail)

            self.screen.blit(self.help_page, (0, 0))
            previous_button.draw(self.screen)
            next_button.draw(self.screen)
            back_button.draw(self.screen)
            pg.display.update()

    def end_turn(self):
        self.game.next_player()

        #if next player is human, increment rounds played
        if self.game.current_player.player_id == 0:
            self.game.achievements.complete_achievement("finishRound")
            self.game.rounds_played += 1
            if self.game.rounds_played == 30:
                #end the game
                self.end_game()

    def end_game(self):

        #determine who has the most assets
        self.game.achievements.complete_achievement("finishGame")
        winner = self.game.players[0]
        for player in self.game.players:
            if player.get_asset() > winner.get_asset():
                winner = player

        #display win or lose screen
        screen = img(0, 60, 1, 1, pg.image.load(self.folder_path + r"/img/win.png"))
        if winner.player_id == 1:
            screen = img(0, 90, 1, 1, pg.image.load(self.folder_path + r"/img/lose.png"))
            self.game.achievements.complete_achievement("loseGame")
        else:
            self.game.achievements.complete_achievement("winGame")


        #draw black background
        self.screen.fill((0, 0, 0))

        #main menu and exit buttons
        main_menu_button = Button(500, 500, 200, 50, "Main Menu")
        exit_game_button = Button(500, 560, 200, 50, "Exit Game")


        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEMOTION:
                    if main_menu_button.handle_event(event):
                        self.game.reset_game()
                        self.reset_gui()
                        self.screen.fill((0, 0, 0))
                        pg.display.update()
                        self.main_menu()
                    if exit_game_button.handle_event(event):
                        self.running = False

            screen.draw(self.screen)
            main_menu_button.draw(self.screen)
            exit_game_button.draw(self.screen)
            pg.display.update()
            self.clock.tick(30)
