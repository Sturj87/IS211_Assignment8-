import random
import time

class Player():

    def __init__(self, name):
        self._name = name
        self._total_score = 0

    def add_episode_score_to_total_score(self, episode_score):
        self._total_score += episode_score

    def get_total_score(self):
        return self._total_score

    def get_name(self):
        return self._name


class Die():

    def __init__(self):
        super().__init__()

    def roll(self):
        return random.randint(1, 6)


class PlayerFactory():
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)


class HumanPlayer(Player):

    def __init__(self, name):
        super().__init__(name)

    def make_decision(self, episode_score):
        while True:
            decision = input(f"{self._name}, your current score is {self._total_score}. The episode score is {episode_score}. Choose either to roll(r) or to hold(h): ")
            if decision == "r" or decision == "h":
                return decision


class ComputerPlayer(Player):

    def __init__(self, name):
        super().__init__(name)

    def make_decision(self, episode_score):
        if self._total_score + episode_score >= 100 or episode_score >= min(25, 100 - self._total_score):
            return "h"
        else:
            return "r"


class TimedGameProxy():

    def __init__(self, numPlayers, player1_type, player2_type, timed):
        self._die = Die()
        self._players = [PlayerFactory.create_player(player1_type, "Player 1"), PlayerFactory.create_player(player2_type, "Player 2")]
        self._timed = timed
        self._start_time = time.time()
        self._winner = None

    def _play_episode(self, player):
        episode_score = 0
        print(f"Hi {player.get_name()}, it's your turn. Your total score is {player.get_total_score()}.")
        while True:
            print(f"Your current episode score is {episode_score}.")
            decision = player.make_decision(episode_score)
            if decision == "r":
                roll_value = self._die.roll()
                print(f"{roll_value} was rolled")
                if roll_value == 1:
                    return 0
                episode_score += roll_value
                cumulative_score = player.get_total_score() + episode_score
                if cumulative_score >= 100:
                    return cumulative_score

            elif decision == "h":
                player.add_episode_score_to_total_score(episode_score)
                return 0

    def play_game(self):
        player_idx = 0
        print(f"Starting a new game with {len(self._players)} players")
        while not self._winner:
            p = self._players[player_idx]
            value = self._play_episode(p)
            if value >= 100:
                self._winner = p.get_name()

            if self._timed and time.time() - self._start_time > 60:
                print("Time's up!")
                return

            player_idx = (player_idx + 1) % len(self._players)

        print(f"The winner is {self._winner}")

if __name__ == "__main__":
    game = TimedGameProxy(2, "human", "computer", False)
    game.play_game()
