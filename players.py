import chopsticksGame
import random

class RandomPlayer(chopsticksGame.Player):
  def __init__(self, hand_count=2, hand_size=5):
    super().__init__(hand_count, hand_size)
    self.target_player = 0
    self.target_hand = 0
    self.attack_hand = 0
    self.split_probability = 0.5

  def strategize(self, gamestate):
    #check if splitting is possible
    if self.can_split():
      if random.random() < self.split_probability:
        self.split()
        return "split" # to break out of this function

    #assemble list of potential targets
    targets = []
    for player in gamestate.players:
      if player != self and player.alive:
        targets.append(player)
    #pick a target
    self.target_player = random.choice(targets)
      
    #lists that target's non-empty hands
    target_hands = []
    for hand in self.target_player.hands:
      if hand.fingers:
        target_hands.append(hand)
    #pick target hand
    self.target_hand = random.choice(target_hands)

    attack_hands = []
    for hand in self.hands:
      if hand.fingers:
        attack_hands.append(hand)   
    self.attack_hand = random.choice(attack_hands)

class HumanPlayer(chopsticksGame.Player):
  def __init__(self, hand_count=2, hand_size=5):
    super().__init__(hand_count, hand_size)
    self.human = True
    self.target_player = 0
    self.target_hand = 0
    self.attack_hand = 0

  def strategize(self, gamestate):
    #assemble list of potential targets
    self.targets = []
    for player in gamestate.players:
      if player != self:
        self.targets.append(player)

    if self.can_split():
      if (self.prompt_for_split()):
        self.split()
        return "split" # to break out of this function

    self.prompt_for_attack_hand()

    if len(self.targets) <= 1: #might get rid of this "if"
      self.target_player = self.targets[0]
    else:  
      self.prompt_for_target_player()

    self.prompt_for_target_hand()

    #eventually have this function return the last move made for logging/graphing puposes

  def prompt_for_split(self):
    split_response = input("Split hand? (y/N)")
    return split_response.upper() == "Y"

  def prompt_for_attack_hand(self):
    satisfied = False
    while not satisfied:
        try:
          attack_hand_index = int(input("Which hand to use? "))
          self.attack_hand = self.hands[attack_hand_index]
        except IndexError:
          print("You don't have that hand.")
        except ValueError:
          print("Please input a valid index") 
        else:
          if self.attack_hand.fingers == 0:
            print("That hand is dead")
          else:
            satisfied = True

  def prompt_for_target_player(self):
    satisfied = False
    while not satisfied:
      try:
        target_id = int(input("Which player to attack? ")) #COME BACK to fix potential ERROR
        self.target_player = self.id_to_player(target_id)
      except IndexError:
        print("That player doesn't exist")
      except ValueError:
        print("Please input a valid index") 
      else:
        if self.target_player == self:
          print("Can't attack self") 
          #in the future, maybe ^ these checks ^ should go in the game loop, so people can submit their own code and not worry about breaking the game
        elif self.target_player not in self.targets:
          print("That player is not in the game")
        elif self.target_player.alive == False:
          print("That player is dead")
        else:
          satisfied = True
      
      

  def prompt_for_target_hand(self):
    satisfied = False
    while not satisfied:
      try:
        target_hand_index = int(input("Which hand to attack? "))
        self.target_hand = self.target_player.hands[target_hand_index]
      except IndexError:
        print("The target doesn't have that hand.")
      except ValueError:
        print("Please input a valid index") 
      else:
        if self.target_hand.fingers == 0:
          print("That hand is dead")
        else:
          satisfied = True
  

  
