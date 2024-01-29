import csv
import random
import os


class CardValues:
    folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def get_chance_card(card_index):
        with open(CardValues.folder_path + r'/data/ChanceCards.csv') as f:
            chance = csv.reader(f)
            for row in chance:
                if (str(card_index) == row[0]):
                    return [row[1], row[2], CardValues.folder_path + r'/img/chance/' + row[3]]

    def get_community_chest_card(card_index):
        with open(CardValues.folder_path + r'/data/CommunityChestCards.csv') as f:
            communityChest = csv.reader(f)
            for row in communityChest:
                if (str(card_index) == row[0]):
                    return [row[1], row[2], CardValues.folder_path + r'/img/chest/' + row[3]]


class Tile:
    def __init__(self, name, position, tile_type, rect):
        self.name = name
        self.position = position
        self.type = tile_type
        self.rect = rect

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position

    def get_type(self):
        return self.type

    def operation(self, player):  # may need to pass in player
        pass


class Corner(Tile):
    def __init__(self, name, position, tile_type, rect):
        super().__init__(name, position, tile_type, rect)

        self.at_start = False
        self.at_jail = False
        self.at_parking = False
        self.at_go_to_jail = False

    def operation(self, player):
        self.at_start = False
        self.at_jail = False
        self.at_parking = False
        self.at_go_to_jail = False

        if player.position == 0:
            self.at_start = True
        elif player.position == 10:
            self.at_jail = True
        elif player.position == 20:
            self.at_parking = True
        elif player.position == 30:
            self.at_go_to_jail = True

        return 0


class Property(Tile):
    def __init__(self, name, position, tile_type, price, image_name, rect):
        super().__init__(name, position, tile_type, rect)
        self.price = price
        self.mortgage_price = self.price / 2
        self.owner = None
        self.num = 0
        self.set_owned = False
        self.image_name = image_name

    def operation(self, player):
        pass

    def set_owner(self, owner):
        if (owner.get_balance() < self.price):
            return -1
        if (self.owner != None):
            self.change_set_rent(self.owner, -1)
        self.owner = owner
        sameSet = self.change_set_rent(owner, 1)
        if (sameSet == None):
            self.num = 1
        else:
            self.num = sameSet
        return 0

    def change_set_rent(self, owner, inc):
        sameSet = None
        for property in owner.get_properties():
            if (property.name != self.name and property.type == self.type):
                if (self.type == "Street"):
                    if (self.colour == property.colour):
                        sameSet = property
                        property.num += inc
                        property.set_rent()
                    else:
                        continue
                property.num += inc
                property.set_rent()
                sameSet = property.num
        return sameSet

    def get_owner(self):
        return self.owner

    def is_owned(self):
        return self.owner != None

    def remove_owner(self):
        self.owner = None

    def get_price(self):
        return self.price

    def get_image_name(self):
        return self.image_name


class Street(Property):
    def __init__(self, name, position, tile_type, colour, price, rent, rent_build_1, rent_build_2, rent_build_3,
                 rent_build_4, rent_build_5, build_price, set_num, image_name, rect):
        super().__init__(name, position, tile_type, price, image_name, rect)

        self.rent = [rent, rent_build_1, rent_build_2, rent_build_3, rent_build_4, rent_build_5]
        self.build_price = build_price
        self.colour = colour
        self.set_num = set_num
        self.houses = 0

    class StreetMemento:
        def __init__(self, owner_id, num, position, set_num, houses, set_owned):
            self.type = "Street"
            self.owner_id = owner_id
            self.num = num
            self.set_num = set_num
            self.houses = houses
            self.set_owned = set_owned
            self.position = position

    def save_tile(self):
        if self.owner is None:
            player_id = -1
        else:
            player_id = self.owner.player_id

        return self.StreetMemento(owner_id=player_id, num=self.num, position=self.position, set_num=self.set_num,
                                  houses=self.houses, set_owned=self.set_owned)

    def load_tile(self, street_memento, owner):
        self.owner = owner
        self.num = street_memento.num
        self.set_num = street_memento.set_num
        self.houses = street_memento.houses
        self.set_owned = street_memento.set_owned

    def operation(self, player):
        if (self.owner == None):
            if (player.get_balance() < self.get_price()):  # can't buy property
                return -1  # can't buy property
            self.set_owner(player)
            player.set_balance(player.get_balance() - self.get_price())
            return 0  # bought property
        elif (self.owner == player):
            print("already owned by player")
            return 1  # already owned by player
        else:
            # pay rent
            player.set_balance(player.get_balance() - self.get_rent())
            player.set_asset(player.get_asset() - self.get_rent())
            self.owner.set_balance(self.owner.get_balance() + self.get_rent())
            self.owner.set_asset(self.owner.get_asset() + self.get_rent())
            return 2  # paid rent

    def set_rent(self):
        pass

    def get_rent(self):
        if (self.houses == 0):
            return 2 * self.rent[0] if self.set_owned else self.rent[0]
        return self.rent[self.houses]

    def get_houses(self):
        return self.houses


class Railroad(Property):
    def __init__(self, name, position, tile_type, price, rent, image_name, rect):
        super().__init__(name, position, tile_type, price, image_name, rect)
        self.rent = rent  # save

    class RailroadMemento:
        def __init__(self, owner_id, num, position):
            self.type = "Railroad"
            self.owner_id = owner_id
            self.num = num
            self.position = position
            self.set_num = -1
            self.houses = -1
            self.hotels = -1
            self.set_owned = -1

    def save_tile(self):
        if self.owner is None:
            player_id = -1
        else:
            player_id = self.owner.player_id
        return self.RailroadMemento(owner_id=player_id, num=self.num, position=self.position)

    def load_tile(self, railroad_memento, owner):
        self.owner = owner
        self.num = railroad_memento.num
        self.set_rent()

    def operation(self, player):
        if (self.owner == None):
            if (player.get_balance() < self.get_price()):  # can't buy property
                return -1
            self.set_owner(player)
            player.set_balance(player.get_balance() - self.get_price())
            return 0
        elif (self.owner == player):
            print("already owned by player")
            return 1
        else:
            # pay rent
            # need to check if player has enough money
            player.set_balance(player.get_balance() - self.get_rent())
            player.set_asset(player.get_asset() - self.get_rent())
            self.owner.set_balance(self.owner.get_balance() + self.get_rent())
            self.owner.set_asset(player.get_asset() + self.get_rent())
            return 2

    def set_rent(self):
        if (self.num == 1):
            self.rent = 25
        elif (self.num == 2):
            self.rent = 50
        elif (self.num == 3):
            self.rent = 100
        elif (self.num == 4):
            self.rent = 200

    def get_rent(self):
        return self.rent


class Utility(Property):
    def __init__(self, name, position, tile_type, price, rent, image_name, rect):
        super().__init__(name, position, tile_type, price, image_name, rect)
        self.rent = rent

    class UtilityMemento:
        def __init__(self, owner_id, num, position):
            self.type = "Utility"
            self.owner_id = owner_id
            self.num = num
            self.position = position
            self.set_num = -1
            self.houses = -1
            self.hotels = -1
            self.set_owned = -1

    def save_tile(self):
        if self.owner is None:
            player_id = -1
        else:
            player_id = self.owner.player_id
        return self.UtilityMemento(owner_id=player_id, num=self.num, position=self.position)

    def load_tile(self, utility_memento, owner):
        self.owner = owner
        self.num = utility_memento.num
        self.set_rent()

    def operation(self, player):
        if (self.owner == None):
            if (player.get_balance() < self.get_price()):  # can't buy property
                return -1
            self.set_owner(player)
            player.set_balance(player.get_balance() - self.get_price())
            return 0
        elif (self.owner == player):
            print("already owned by player")
            return 1
        else:
            # pay rent
            # need to check if player has enough money
            player.set_balance(player.get_balance() - self.get_rent())
            player.set_asset(player.get_asset() - self.get_rent())
            self.owner.set_balance(self.owner.get_balance() + self.get_rent())
            self.owner.set_asset(player.get_asset() - self.get_rent())
            return 2

    def set_rent(self):
        if (self.num == 1):
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            self.rent = 4 * dice1 * dice2
        elif (self.num == 2):
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            self.rent = 10 * dice1 * dice2

    def get_rent(self):
        if self.set_owned:
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            return 10 * (dice1 + dice2)
        else:
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            return 4 * (dice1 + dice2)


class Tax(Tile):
    def __init__(self, name, position, tile_type, tax_price, rect):
        super().__init__(name, position, tile_type, rect)
        self.tax_price = tax_price

    def operation(self, player):
        player.set_balance(player.get_balance() - self.tax_price)
        player.set_asset(player.get_asset() - self.tax_price)


# There should be a singleton queue of cards for both chance and community chest
# look for a way to implement this pythonically
class Card_Collection:

    def __init__(self, get_type, jail_num):
        self.list = []
        # turns true when card is in either players hand and false otherwise
        self.get_type = get_type
        self.jail_num = jail_num
        self.get_out_of_jail_card = False

    def add_item(self, item):
        if (item == self.jail_num and self.get_out_of_jail_card):
            return
        self.list.append(item)

    def set_jail_card(self, bool):
        self.get_out_of_jail_card = bool

    def pop(self):
        return self.list.pop()

    def create_iterator(self):
        return Card_Iterator(self)


class Card_Iterator:
    _instance = None

    def __init__(self, card_collection):
        if (self._instance != None):
            return self._instance
        self.collection = card_collection
        self.cards_left = 16
        self.fill_list()

    def fill_list(self):
        list = []
        for i in range(1, 17):
            list.append(i)
        random.shuffle(list)
        for element in list:
            self.collection.add_item(element)

    def get_next(self):
        card = self.collection.pop()
        jail_num = self.collection.jail_num
        if (card == jail_num):
            self.collection.set_jail_card(True)
        self.cards_left -= 1
        if (self.cards_left == 0):
            self.fill_list()
            self.cards_left = 16
        cardvalue = self.collection.get_type(card)
        return cardvalue

    def has_next(self):
        return True


class Chance(Tile):
    _instance = None

    def __init__(self, name, position, tile_type, rect):
        super().__init__(name, position, tile_type, rect)
        if (Chance._instance != None):
            self.card_iterator = Chance._instance
            return
        self.card_iterator = Card_Collection(CardValues.get_chance_card,
                                             9).create_iterator()  # 9 represents the jail card
        Chance._instance = self.card_iterator

    def operation(self, player, all_players, tiles):
        card = self.card_iterator.get_next()
        if (card[0] == 'move'):
            newPosition = None
            if (card[1] == 'jail'):
                player.go_to_jail()
                return card[2]
            elif (card[1] == 'utility'):
                if (self.position == 22):  # the only way to get to waterworks is on space 22
                    newPosition = 28
                else:
                    newPosition = 12
            elif (card[1] == 'railroad'):
                if (self.position == 7):  # checks which chance spaces a player is on
                    newPosition = 15
                elif (self.position == 22):
                    newPosition = 25
                else:
                    newPosition = 5
            elif (card[1] == '-3'):
                newPosition = player.position - 3
            else:
                newPosition = int(card[1])
            if (newPosition - self.position < 0):  # passed go
                player.set_balance(player.get_balance() + 200)
                player.set_asset(player.get_asset() + 200)
            player.move_player_to(newPosition)
            return card[2]
        elif (card[0] == 'money'):
            if (card[1] == 'house'):
                owed = 0
                for tile in tiles:
                    if (type(tile) == Street):
                        if (tile.owner == player):
                            if (tile.get_houses() < 5):
                                owed += tile.get_houses() * 25
                            else:  # if 5 then hotel
                                owed += 100
                player.set_balance(player.get_balance() - owed)
                player.set_asset(player.get_asset() - owed)
            elif (card[1] == 'players'):
                for eachPlayer in all_players:
                    if (eachPlayer == player):
                        continue
                    eachPlayer.set_balance(player.get_balance() + 50)
                    eachPlayer.set_asset(player.get_asset() + 50)
                    player.set_balance(player.get_balance() - 50)
                    player.set_asset(player.get_asset() - 50)
            else:
                amount = int(card[1])
                player.set_balance(player.get_balance() + amount)
                player.set_asset(player.get_asset() + amount)

        else:
            player.add_jail_card()

        return card[2]


class CommunityChest(Tile):
    _instance = None

    def __init__(self, name, position, tile_type, rect):
        super().__init__(name, position, tile_type, rect)
        if (CommunityChest._instance != None):
            self.card_iterator = CommunityChest._instance
            return
        self.card_iterator = Card_Collection(CardValues.get_community_chest_card,
                                             1).create_iterator()  # 1 represents the jailcard
        CommunityChest._instance = self.card_iterator

    def operation(self, player, all_players, tiles):
        # call card.operation(player)
        card = self.card_iterator.get_next()
        if (card[0] == 'move'):
            newPosition = None
            if (card[1] == 'jail'):
                player.go_to_jail()
                return card[2]
            else:
                newPosition = int(card[1])
            if (newPosition - self.position < 0):  # passed go
                player.set_balance(player.get_balance() + 200)
                player.set_asset(player.get_asset() + 200)
            player.move_player_to(newPosition)

        elif (card[0] == 'money'):
            if (card[1] == 'house'):
                owed = 0
                for tile in tiles:
                    if (type(tile) == Street):
                        if (tile.owner == player):
                            if (tile.get_houses() < 5):
                                owed += tile.get_houses() * 40
                            else:  # if 5 then hotel
                                owed += 115
                player.set_balance(player.get_balance() - owed)
                player.set_asset(player.get_asset() - owed)
            elif (card[1] == 'players'):

                for eachPlayer in all_players:
                    if (eachPlayer == player):
                        continue
                    eachPlayer.set_balance(player.get_balance() - 10)
                    eachPlayer.set_asset(player.get_asset() - 10)
                    player.set_balance(player.get_balance() + 10)
                    player.set_asset(player.get_asset() + 10)

            else:
                amount = int(card[1])
                player.set_balance(player.get_balance() + amount)
                player.set_asset(player.get_asset() + amount)

        else:
            player.add_jail_card()
        return card[2]
