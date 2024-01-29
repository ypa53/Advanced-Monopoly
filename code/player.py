class Player:
    def __init__(self, player_id, name, image_name):
        self.player_id = player_id
        self.name = name
        self.balance = 1500
        self.asset = 1500
        self.rounds_in_jail = 0
        self.position = 0
        self.out_of_jail_cards = 0
        self.is_bankrupt = False
        self.properties = []
        self.image_name = image_name

    class PlayerMemento:
        def __init__(self, player_id, name, balance, asset, rounds_in_jail, position, out_of_jail_cards, is_bankrupt,
                     properties, image_name):
            self.player_id = player_id
            self.name = name
            self.balance = balance
            self.asset = asset
            self.rounds_in_jail = rounds_in_jail
            self.position = position
            self.out_of_jail_cards = out_of_jail_cards
            self.is_bankrupt = is_bankrupt
            self.properties = properties
            self.image_name = image_name

    def save_player(self):
        return self.PlayerMemento(self.player_id, self.name, self.balance, self.asset, self.rounds_in_jail,
                                  self.position,
                                  self.out_of_jail_cards, self.is_bankrupt, self.properties, self.image_name)

    def load_player(self, player_memento):
        self.player_id = player_memento.player_id
        self.name = player_memento.name
        self.balance = player_memento.balance
        self.asset = player_memento.asset
        self.rounds_in_jail = player_memento.rounds_in_jail
        self.position = player_memento.position
        self.out_of_jail_cards = player_memento.out_of_jail_cards
        self.is_bankrupt = player_memento.is_bankrupt
        self.properties = player_memento.properties
        self.image_name = player_memento.image_name

    def make_move(self):
        pass

    def check_bankruptcy(self):
        if self.balance < 0:
            self.is_bankrupt = True

    def get_balance(self):
        return self.balance

    def set_balance(self, balance):
        self.balance = balance

    def get_asset(self):
        return self.asset

    def set_asset(self, asset):
        self.asset = asset

    def go_to_jail(self):
        self.rounds_in_jail = 3
        self.position = 10

    def check_in_jail(self):
        return self.rounds_in_jail > 0

    def use_jail_card(self):
        if self.out_of_jail_cards > 0:
            self.out_of_jail_cards -= 1
            self.rounds_in_jail = 0

    def add_jail_card(self):
        self.out_of_jail_cards += 1

    def move_player_to(self, position):
        self.position = position

    def get_properties(self):
        return self.properties


# extra class for human player
class HumanPlayer(Player):
    def __init__(self, player_id, name, image_name):
        super().__init__(player_id, name, image_name)
        self.is_human = True


# extra class for AI player
class AIPlayer(Player):
    def __init__(self, player_id, name, image_name):
        super().__init__(player_id, name, image_name)
        self.is_human = False
