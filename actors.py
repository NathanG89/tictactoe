class Player(object):
    def __init__(self, id, symbol='-'):
        self.id = id
        self.turn = False
        self.symbol = symbol

    def is_my_turn(self):
        return self.turn

    def toggle_turn(self):
        self.turn = not self.turn


class Game(object):
    """ids represents total number of players, it starts at 0.
    current_turn is used to iterate through all players."""
    ids = 0
    current_turn = 0

    def __init__(self, players=None):
        # create players
        # by default, player 1 goes first
        self.players = players
        if players is None or len(players) <= 1:
            self.players = []
            for i in range(2):
                self.players.append(Player(self.ids))
                self.ids += 1
        self.players[0].toggle_turn()

    def next(self):
        self.next_player_turn()

    def next_player_turn(self):
        self.players[self.current_turn].toggle_turn()
        self.current_turn = (self.current_turn + 1) % len(self.players)
        self.players[self.current_turn].toggle_turn()
        assert self.players[self.current_turn].id == self.current_turn
        assert self.players[self.current_turn].is_my_turn()
