# class Hand:
#   def __init__(self):
#     self.fingers = 0;
  
#   def __str__(self):
#     return self.fingers

#   def __add__(self, other)


class Player:
  id_counter = 0
  player_list = []

  def __init__(self):
    self.hands = [0,0] ##wait, I have a feeling all of the hand counters will be pointing to the SAME array
    self.id = Player.id_counter
    Player.player_list.append(self)
    Player.id_counter += 1

  def __str__(self):

    return "Player {}: {}".format(self.id, self.hands)

  @classmethod
  def id_to_player(cls, id):
    for player in cls.player_list:
      if player.id == id:
        return player
    raise ValueError("Invalid player id")
    return False

  def fingers(self, hand): #returns how many fingers are up on the given hand
  #what even do we need this function for? is it a style thing?
    return self.hands[hand]
  
  def get_hit(self, sticks, hand): #runs when you get hit
    self.hands[hand] += sticks
    self.hands[hand] = self.hands[hand] % 5

  def checkSplit(self): #returns if you can split
    return (self.hands[0] % 2 == 0 and self.hands[1] == 0) or (self.hands[1] % 2 == 0 and self.hands[0] == 0)
  
  def split(self):
    tot = self.hands[0] + self.hands[1]
    avg = tot / 2
    self.hands[0] = avg
    self.hands[1] = avg
    
  def equals(self, player):
    return self.hands[0] == player.hands[0] and self.hands[1] == player.hands[1]

  def print(self):
    print(self.id)
    
  
class Gamestate:
  def __init__(self):
    self.players = []
    self.active_player_index = 0
    self.parents = []
    self.children = []

  def add(self, player):
    self.players.append(player)

  def equals(self, state):
    for player in self.players:
      if self.players.len() != state.players.len():
        return False
      else:
        for i in range(self.players.len()):
          if not self.players[i].equals(state.players[i]):
            return False

        return True #returns True only if all the players are the same
  
  def done(self): #returns True if the game is over, which we're saying is once a single person has been eliminated. I think this is better for simulation purposes (stop the simulation, then refer back to the graph we have for the 2 player game with the corresponding gamestate)
    for player in self.players:
      hand_counter = 0
      for hand in player.hands:
        hand_counter += hand
      
      if hand_counter == 0:
        return True
    
    return False

  def print(self):
    print("Gamestate:")
    for i in range(len(self.players)):
      if i == self.active_player_index:
        print("{}  *active player".format(self.players[i])) #asterisk indicates active player
      else:
        print(self.players[i])

  def next_player(self): #increments the active player counter
    self.active_player_index = (self.active_player_index + 1) % len(self.players)
        