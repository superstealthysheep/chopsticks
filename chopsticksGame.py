class Hand:
  def __init__(self, owner, size=5, fingers=0):
    self.fingers = fingers;
    self.size = size;
    self.owner = owner

  def __str__(self):
    return str(self.fingers)

  # def __add__(self, other):


class Player:
  id_counter = 0
  player_list = []

  def __init__(self, hand_count=2, hand_size=5):
    self.alive = True
    self.hand_count = hand_count
    self.hands = []
    self.id = Player.id_counter
    Player.player_list.append(self)
    Player.id_counter += 1

    for i in range(self.hand_count):
      self.hands.append(Hand(self, hand_size))

  def __str__(self):
    pretty_hand_list = []
    for hand in self.hands:
      pretty_hand_list.append(hand.fingers)
        
    return "Player {}: {}".format(self.id, pretty_hand_list)

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
    if hand in self.hands:
      hand.fingers += sticks
      hand.fingers = hand.fingers % hand.size
      self.check_alive()
    else:
      raise ValueError("target hand does not belong to target owner")

  def can_split(self): #returns if you can split
    live_hands = 0
    finger_total = 0
    for hand in self.hands:
      if hand.fingers:
        live_hands += 1
        finger_total += hand.fingers

    return (live_hands == 1) and (finger_total % len(self.hands) == 0) #a lonely hand that can be evenly divided
    
    
  
  def split(self):
    tot = 0
    for hand in self.hands:
      tot += hand.fingers
    avg = int(tot / len(self.hands)) #the avg will be a whole number if self.check_split() was confirmed in advance
    
    for hand in self.hands:
      hand.fingers = avg

    print("SPLIT!!!")
    
  def equals(self, player):
    return self.hands[0] == player.hands[0] and self.hands[1] == player.hands[1]

  def print(self):
    print(self.id)

  def check_alive(self):
    self.alive = False
    for hand in self.hands:
      if hand.fingers:
        self.alive = True
    return self.alive
    
  
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
  
  def done(self): #returns True after only one (or fewer) people are left standing 
    alive_counter = 0
    for player in self.players: #running this loop every single turn might not be the most computationally efficient...
      if player.alive:
        alive_counter += 1
    
    if alive_counter <= 1:
      return True
    else:
      return False

  def first_blood(self): #returns True as soon as first person dies
    for player in self.players:
      if not player.alive:
        return True 
      else:
        return False

  def print(self):
    print("Gamestate:")
    for i in range(len(self.players)):
      if i == self.active_player_index:
        print("{}  *active player".format(self.players[i])) #asterisk indicates active player
      else:
        print(self.players[i])

  def next_player(self): #switches next living player to be the active one
    live_player_found = False
    while not live_player_found:
      self.active_player_index = (self.active_player_index + 1) % len(self.players)
      live_player_found = self.players[self.active_player_index].alive
  
  def run_game(self):
    self.print()
    while not self.done():
      active_player = self.players[self.active_player_index]

      active_player.strategize(self)
      target_player = active_player.target_player
      target_hand = active_player.target_hand
      attack_hand = active_player.attack_hand
      sticks = attack_hand.fingers

      target_player.get_hit(sticks, target_hand)

      self.next_player()
      self.print()
