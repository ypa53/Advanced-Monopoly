from tile import *
import json
import pygame


class Board:
    def __init__(self, json_file_path):
        self.spaces = []
        self.property_groups = [(1, 3), (6, 8, 9), (11, 13, 14), (16, 18, 19), (21, 23, 24), (26, 27, 29), (31, 32, 34),
                                (37, 39), (5, 15, 25, 35), (12, 28)]
        self.create_board(json_file_path)

    def create_board(self, json_file_path):
        with open(json_file_path) as json_file:
            data = json.load(json_file)
            for tile in data:
                self.spaces.append(TileFactory.create_tile(tile))

    def save_board(self):
        tile_mementos = []
        for tile in self.spaces:
            if tile.type == "Street" or tile.type == "Railroad" or tile.type == "Utility":
                tile_mementos.append(tile.save_tile())
        return tile_mementos

    def load_board(self, tile_mementos):
        for tile_memento in tile_mementos:
            tile = self.spaces[tile_memento.position]
            tile.load_tile(tile_memento)
    def can_sell(self, tile_index):
        property_group = self.return_property_group(tile_index)
        property = self.spaces[tile_index]

        max_houses = 0
        for tile in property_group:
            if tile.houses > max_houses:
                max_houses = tile.houses

        return property.houses == max_houses

    def can_build(self, tile_index, player):
        property_group = self.return_property_group(tile_index)
        property = self.spaces[tile_index]

        # #check if property is a street
        if property.type != "Street":
            return False

        #check if already has 5 houses
        if property.houses == 5:
            return False

        #check if the player owns all the properties in the group
        for tile in property_group:
            if tile.owner != player:
                return False

        #next check if the player has enough money
        if player.balance < property.build_price:
            return False

        #next check if selected_tile is the tile with the least houses
        min_houses = 5
        for tile in property_group:
            if tile.houses < min_houses:
                min_houses = tile.houses

        return property.houses == min_houses

    def return_property_group(self, tile_index):
        #returns the property group of the tile
        for group in self.property_groups:
            if tile_index in group:
                #create a list of the tiles in the group
                tiles = []
                for tile_index in group:
                    tiles.append(self.spaces[tile_index])
                return tiles

    def update_sets(self, tile_index):
        #if all properties in the group are owned by the same player, update the set_owned
        property_group = self.return_property_group(tile_index)
        property = self.spaces[tile_index]
        owner = property.owner

        #Railroads are a special case
        if property.type == "Railroad":
            count = 0
            for tile in property_group:
                if tile.owner == owner:
                    count += 1

            #for all railroads owned by player, set the num
            for tile in property_group:
                if tile.owner == owner:
                    tile.num = count
                    tile.set_rent()

            return



        all_owned = True
        if owner != None:
            for tile in property_group:
                if tile.owner != owner:
                    all_owned = False
                    break

        if all_owned:
            #set the set_owned flag to true for all tiles in the group
            for tile in property_group:
                tile.set_owned = True

        return all_owned

    def set_sets_to_false(self, tile_index):
        #sets the set_owned flag to false for all tiles in the group
        property_group = self.return_property_group(tile_index)
        for tile in property_group:
            tile.set_owned = False

    def update_Railroad_num(self, tile_index): #called only when selling a railroad
        property_group = self.return_property_group(tile_index)
        owner = self.spaces[tile_index].owner

        #for all railroads owned by player, decrement the num
        for tile in property_group:
            if tile.owner == owner:
                tile.num -= 1
                tile.set_rent()




class TileFactory:

    @staticmethod
    def create_tile(tile_data):
        tile_type = tile_data["Type"]
        tile_rect = TileFactory.create_rect(tile_data["Position"], tile_data["X"], tile_data["Y"])
        if tile_type == "Corner":
            return Corner(tile_data["Name"], tile_data["Position"], tile_data["Type"], tile_rect)
        elif tile_type == "Street":
            return Street(name=tile_data["Name"], position=tile_data["Position"], tile_type=tile_data["Type"],colour=tile_data["Colour"], price=tile_data["Price"],
                          rent=tile_data["Rent"], rent_build_1=tile_data["RentBuild1"], rent_build_2=tile_data["RentBuild2"], rent_build_3=tile_data["RentBuild3"],
                          rent_build_4=tile_data["RentBuild4"], rent_build_5=tile_data["RentBuild5"], build_price=tile_data["PriceBuild"], set_num=tile_data["SetNum"], image_name=tile_data["ImageName"],
                          rect=tile_rect)
        elif tile_type == "Railroad":
            return Railroad(tile_data["Name"], tile_data["Position"], tile_data["Type"], tile_data["Price"], tile_data["Rent"], tile_data["ImageName"], tile_rect)
        elif tile_type == "Utility":
            return Utility(tile_data["Name"], tile_data["Position"], tile_data["Type"], tile_data["Price"], tile_data["Rent"], tile_data["ImageName"], tile_rect)
        elif tile_type == "Tax":
            return Tax(tile_data["Name"], tile_data["Position"], tile_data["Type"], tile_data["Price"], tile_rect)
        elif tile_type == "Chance":
            return Chance(tile_data["Name"], tile_data["Position"], tile_data["Type"], tile_rect)
        elif tile_type == "Community Chest":
            return CommunityChest(tile_data["Name"], tile_data["Position"], tile_data["Type"], tile_rect)
        else:
            return None

    @staticmethod
    def create_rect(tile_position, top_left_x=0, top_left_y=0):
        #we know position, so we can tell orientation/size
        #top left x and y are the top left of the tile
        #positions 1 to 9 are on the bottom row and are vertical ie height = 105, width = 65
        #positions 11 to 19 are on the left side and are horizontal ie height = 65, width = 105
        #positions 21 to 29 are on the top row and are vertical ie height = 105, width = 65
        #positions 31 to 39 are on the right side and are horizontal ie height = 65, width = 105
        #positions 0, 10, 20, 30 are the corners and are 105 x 105
        #tile_position is the position of the tile on the board

        if tile_position == 0 or tile_position == 10 or tile_position == 20 or tile_position == 30:
            return pygame.Rect(top_left_x, top_left_y, 105, 105)

        elif tile_position >= 1 and tile_position <= 9 or tile_position >= 21 and tile_position <= 29:
            return pygame.Rect(top_left_x, top_left_y, 65, 105)

        elif tile_position >= 11 and tile_position <= 19 or tile_position >= 31 and tile_position <= 39:
            return pygame.Rect(top_left_x, top_left_y, 105, 65)
        else:
            return None