import copy

class Hand:
  id_counter = 0;
  def __init__(self, owner, size=5, fingers=0):
    self.fingers = fingers
    self.size = size;
    self.owner = owner
    self.id = len(owner.hands) #this id is owner-specific only (different owners each have their own hand number 0)

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

  def __repr__(self): 
    return str(self) #for debug purposes

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

    lonely_hand = live_hands == 1
    has_partners = len(self.hands) > 1
    evenly_divisible = (finger_total % len(self.hands) == 0)

    return lonely_hand and has_partners and evenly_divisible #a lonely hand (with dead partners) that can be evenly divided
  
  def split(self):
    tot = 0
    for hand in self.hands:
      tot += hand.fingers
    avg = int(tot / len(self.hands)) #the avg will be a whole number if self.check_split() was confirmed in advance
    
    for hand in self.hands:
      hand.fingers = avg

    print("SPLIT!!!")
    
  def equals(self, other):
    if len(self.hands) != len(other.hands):
      return False
    else:
      for i in range(len(self.hands)):
        if self.hands[i].fingers != other.hands[i].fingers:
          return False
      else:
        return True

  def print(self):
    print(self.id)

  def check_alive(self):
    self.alive = False
    for hand in self.hands:
      if hand.fingers:
        self.alive = True
    return self.alive

  def id_to_hand(self, hand_id):
    for hand in self.hands:
      if hand.id == hand_id:
        return hand
    else:
      raise ValueError("id_to_hand was passed an invalid id")

  def list_targets(self, gamestate): #assemble list of potential targets
    targets = []
    for player in gamestate.players:
      if player != self and player.alive:
        targets.append(player)
      
    return targets

  def list_target_hands(self, target_player):
    target_hands = []
    for hand in target_player.hands:
      if hand.fingers:
        target_hands.append(hand)
    
    return target_hands

  def list_attack_hands(self):
    attack_hands = []
    for hand in self.hands:
      if hand.fingers:
        attack_hands.append(hand)

    return attack_hands

  def list_all_moves(self, gamestate): #could be buggy if self not in gamestate.players
    all_moves = []
    if self.can_split():
      all_moves.append(Move("split", self.hands[0])) #this self.hands[0] thing is just my lazy, janky way to let Move know what player is doing the splitting
    else:
      for attack_hand in self.list_attack_hands():
        for target_player in self.list_targets(gamestate):
          for target_hand in self.list_target_hands(target_player):
            all_moves.append(Move("attack", attack_hand, target_player, target_hand))
    return all_moves
    
  
class Gamestate:
  id_counter = 0

  def __init__(self):
    self.players = []
    self.active_player_index = 0
    # self.active_player = None
    self.parents = []
    self.children = []
    self.id = Gamestate.id_counter #will deepcopy not increment the ID?
    Gamestate.id_counter += 1

  # def __repr__(self):
  #   return "Gamestate {}".format(self.id)

  def __str__(self):
    output = "Gamestate {}:\n".format(self.id)
    for i in range(len(self.players)):
      if i == self.active_player_index:
        output = output + "{}  *active player\n".format(self.players[i]) #asterisk indicates active player
      else:
        output = output + str(self.players[i]) + "\n"

    return output

  # @classmethod
  # def construct_from_data(cls, data):
  #   new_instance = cls()
  #   new_instance.players = data[0]
  #   new_instance.active_player_index = data[1]
  #   new_instance.parents = data[2]
  #   new_instance.children = data[3] #this seems messy/wrong
  #   return new_instance

  # @classmethod
  # def deep_copy(cls, original):
  #   data = copy.deepcopy(original._data())
  #   return cls.construct_from_data(data)

  @classmethod
  def deepcopy(cls, original): #deep copy except for the id
    new_instance = copy.deepcopy(original)
    new_instance.id = cls.id_counter
    cls.id_counter += 1
    return new_instance

  # def _data(self):
  #   data = [self.players, self.active_player_index, self.parents, self.children]
  #   return data


  def add(self, player):
    self.players.append(player)

  def equals(self, state):
    for player in self.players:
      if len(self.players) != len(state.players):
        return False
      else:
        for i in range(len(self.players)):
          if not self.players[i].equals(state.players[i]):
            return False
      if(self.active_player_index != state.active_player_index):
        return False
      else:
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

  def print(self): #should eventually do this through a __str__(), I think
    # print("Gamestate:")
    print("Gamestate {}:".format(self.id))
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

      move = active_player.strategize(self)
      if move.type == "split":
        active_player.split()
      elif move.type == "attack":
        target_player = move.target_player
        target_hand = move.target_hand
        sticks = move.attack_hand.fingers

        target_player.get_hit(sticks, target_hand)
      else:
        raise ValueError("Invalid command given by player {}".format(active_player))

      self.next_player()
      self.print()

class Move():
  def __init__(self, type, attack_hand=0, target_player=0, target_hand=0):
    self.type = type
    self.attack_hand = attack_hand
    self.target_player = target_player
    self.target_hand = target_hand

  def __str__(self):
    if self.type == "attack":
      return "{},{} attacks {},{}".format(self.attack_hand.owner.id, self.attack_hand.id, self.target_player.id, self.target_hand.id, self.target_hand.id)
    elif self.type == "split":
      return "player {} splits".format(self.attack_hand.owner.id)
    elif self.type == "exhausted":
      return "move: \"exhausted\""
    else:
      raise ValueError("Move constructed with invalid type {}".format(self.type))

  def transplant(self, donor, recipient): #takes a move from some donor gamestate, then converts it to the same move (meaning which hands are hitting which hands) for the recipient gamestate
    if not donor.equals(recipient): 
      raise ValueError("Attempted to transplant move between non-identical gamestates")

    #0. Check if it's a split (special case)
    if self.type == "split":
      #1. gather
      donor_attack_hand = self.attack_hand
      #2. convert
      attack_player_index = donor.players.index(donor_attack_hand.owner)
      #3. repackage
      attack_player = recipient.players[attack_player_index]
      self.attack_hand = attack_player.hands[0]
      return    

    #if it's not a split
    #1. gather up the info from donor
    donor_attack_hand = self.attack_hand
    donor_target_player = self.target_player
    donor_target_hand = self.target_hand

    #2. convert it for reconstruction
    attack_player_index = donor.players.index(donor_attack_hand.owner)
    attack_hand_id = donor_attack_hand.id
    target_player_index = donor.players.index(donor_target_player)
    target_hand_id = donor_target_hand.id

    #3. package it back up in recipient
    attack_player = recipient.players[attack_player_index]
    self.attack_hand = attack_player.id_to_hand(attack_hand_id)
    self.target_player = recipient.players[target_player_index]
    self.target_hand = self.target_player.id_to_hand(target_hand_id)






  
  def __repr__(self): #like this for debug reasons
    return self.type