import chopsticksGame
import random

class RandomPlayer(chopsticksGame.Player):
  def __init__(self):
    super().__init__()
    self.target_player = 0
    self.target_hand = 0
    self.attack_hand = 0

  def strategize(self, gamestate):
    #assemble list of potential targets
    targets = []
    for player in gamestate.players:
      if player != self:
        targets.append(player)

    #active player picks a random hand and a random target, does the HITTING
    self.target_player = random.choice(targets)
    self.target_hand = random.choice(range(len(self.target_player.hands)))
    self.attack_hand = random.choice(self.hands)

class HumanPlayer(chopsticksGame.Player):
  def __init__(self):
    super().__init__()
    self.human = True
    self.target_player = 0
    self.target_hand = 0
    self.attack_hand = 0

  def strategize(self, gamestate):
    #assemble list of potential targets
    targets = []
    for player in gamestate.players:
      if player != self:
        targets.append(player)

    print("Which hand to use?")
    self.attack_hand = int(input())

    if len(targets) <= 1: #might get rid of this "if"
      self.target_player = targets[0]
    else:  
      print("Which player to attack?")
      target_id = int(input()) #COME BACK to fix potential ERROR
      self.target_player = self.id_to_player(target_id)
      if self.target_player == self:
        raise ValueError("Can't attack self") 
        #in the future, maybe ^ this check ^ should go in the game loop, so people can submit their own code and not worry about breaking the game

    print("Which hand to attack?")
    self.target_hand = int(input())
  

  