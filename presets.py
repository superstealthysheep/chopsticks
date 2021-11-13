import chopsticksGame
import players

class RandomGame(chopsticksGame.Gamestate):
  def __init__(self, size, hand_count=2, hand_size=5):
    super().__init__()

    for i in range(0, size):
      self.add(players.RandomPlayer(hand_count, hand_size))

    for player in self.players:
      for hand in player.hands:
        player.get_hit(1, hand)
      
class HumanGame(chopsticksGame.Gamestate):
  def __init__(self, size, hand_count=2, hand_size=5):
    super().__init__()

    for i in range(0, size):
      self.add(players.HumanPlayer(hand_count, hand_size))

    for player in self.players:
      for hand in player.hands:
        player.get_hit(1, hand)
