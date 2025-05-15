class Game:
    def __init__(self, title):
        if not isinstance(title, str):
            raise Exception("Title must be a string")
        if len(title) == 0:
            raise Exception("Title must be longer than 0 characters")
        self._title = title

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if hasattr(self, '_title'):
            raise Exception("Cannot change game title")
        if not isinstance(value, str):
            raise Exception("Title must be a string")
        if len(value) == 0:
            raise Exception("Title must be longer than 0 characters")
        self._title = value

    def results(self):
        return [result for result in Result.all if result.game == self]

    def players(self):
        return list(set(result.player for result in self.results()))

    def average_score(self, player):
        if not isinstance(player, Player):
            raise Exception("Must be a Player instance")
        results = [result for result in self.results() if result.player == player]
        return sum(result.score for result in results) / len(results) if results else 0


class Player:
    _all = []

    def __init__(self, username):
        if not isinstance(username, str):
            raise Exception("Username must be a string")
        if not 2 <= len(username) <= 16:
            raise Exception("Username must be between 2 and 16 characters")
        self._username = username
        Player._all.append(self)

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not isinstance(value, str):
            raise Exception("Username must be a string")
        if not 2 <= len(value) <= 16:
            raise Exception("Username must be between 2 and 16 characters")
        self._username = value

    def results(self):
        return [result for result in Result.all if result.player == self]

    def games_played(self):
        return list(set(result.game for result in self.results()))

    def played_game(self, game):
        if not isinstance(game, Game):
            raise Exception("Must be a Game instance")
        return game in self.games_played()

    def num_times_played(self, game):
        if not isinstance(game, Game):
            raise Exception("Must be a Game instance")
        return len([result for result in self.results() if result.game == game])

    @classmethod
    def highest_scored(cls, game):
        if not isinstance(game, Game):
            raise Exception("Must be a Game instance")
        if not game.results():
            return None
        player_averages = {}
        for player in cls._all:
            avg_score = game.average_score(player)
            if avg_score > 0:
                player_averages[player] = avg_score
        return max(player_averages.items(), key=lambda x: x[1])[0] if player_averages else None


class Result:
    all = []

    def __init__(self, player, game, score):
        if not isinstance(player, Player):
            raise Exception("Player must be a Player instance")
        if not isinstance(game, Game):
            raise Exception("Game must be a Game instance")
        if not isinstance(score, int):
            raise Exception("Score must be an integer")
        if not 1 <= score <= 5000:
            raise Exception("Score must be between 1 and 5000")
        self._player = player
        self._game = game
        self._score = score
        Result.all.append(self)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        raise Exception("Cannot change score")

    @property
    def player(self):
        return self._player

    @property
    def game(self):
        return self._game