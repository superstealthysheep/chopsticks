import copy
import chopsticksGame
import players

class GamestateNode(): #extends Gamestate but also stores children, possible moves, moves tried
  def __init__(self, parent_gamestate):
    self.gamestate = copy.deepcopy(parent_gamestate) #copies all those instances from parent instance. Deep copy is so that e.g. Player objects are static wrt time
    active_player = self.gamestate.players[self.gamestate.active_player_index]
    self.children = []
    self.all_moves = active_player.list_all_moves(self.gamestate)
    self.moves_tried = [] #this one might be unnecessary
    self.moves_remaining = self.all_moves

    # for move in active_player.list_all_moves(self.gamestate):
    #   print(move)

  def update_node(self, move, child): #updates the lists of moves for this node, and also adds child to the node's children list
    self.moves_tried.append(move)
    self.moves_remaining.remove(move)
    if child not in self.children:
      self.children.append(child) #the if statement is because it's possible for two different moves to output the same gamestate, e.g. player 0 in (1,1),(0, 1) has two ways to attack to return (1,1),(0,2)

class Logger(): #takes a gamestate as input, not a node
  def __init__(self, starting_gamestate):
    self.node_list = []
    # self.gamestate_list = [] #this is janky to have. it's a list parallel to node_list containing only the gamestates 
    # self.last_viable_node #is the most recently visited node with moves not yet tried
    # self.starting_gamestate = starting_gamestate
    # self.gamestate = self.starting_gamestate
    self.starting_node = self.create_node(starting_gamestate)
    starting_gamestate.node = self.starting_node
    self.node = self.starting_node
    self.node_list.append(self.starting_node)

    self.history = []
  
  def done(self):
    pass

  def create_node(self, gamestate): #creates the new node and sets gamestate.node to [a reference to that node] 
    new_node = GamestateNode(gamestate)
    # new_gamestate = new_node.gamestate
    gamestate.node = new_node ##jankkkkk
    self.node_list.append(new_node)
    # self.gamestate_list.append(gamestate)

    return new_node


  def run_game(self):
    
    self.gamestate_list = []
    while not self.node.gamestate.done():
      

      # if self.node.gamestate not in self.gamestate_list:
      #   node = self.create_node(self.node.gamestate) #create a new node and also add self.gamestate to self.gamestate_list
      # else:
      #   node = self.gamestate.node #the "node =..." 2 lines up could be eliminated if this code were run outside of this else, but I find this more legible

      active_player = self.node.gamestate.players[self.node.gamestate.active_player_index]

      move = active_player.strategize(self.node)
      if move.type == "split":
        active_player.split() #self.gamestate is now the child
      elif move.type == "attack":
        target_player = move.target_player
        target_hand = move.target_hand
        sticks = move.attack_hand.fingers

        print(sticks)
        print(target_hand)
        target_player.get_hit(sticks, target_hand) #self.gamestate is now the child #for some reason this isn't affecting self.gamestate. is this because target_player isn't in self.gamestate? instead it's in self.gamestate.node.gamestate?
        print(move)
      else:
        raise ValueError("Invalid command given by player {}".format(active_player))

      self.node.gamestate.next_player()
      self.node.gamestate.print()

      #logging
      self.history.append(move)
      self.node.update_node(move, self.node.gamestate) #self.gamestate is the child by now

      #creating new node if this gamestate isn't yet represented
      try:
        self.node.gamestate.node
      except AttributeError:
        print("This gamestate doesn't have its node field filled in. Creating new node...")
        self.node = self.create_node(self.node.gamestate)
      
      #refresh gamestate_list
      self.gamestate_list = []
      for node in self.node_list:
        self.gamestate_list.append(node.gamestate)

class DepthFirstPlayer(chopsticksGame.Player): #takes the first move available in the list stored for that gamestate
  def __init__(self, hand_count=2, hand_size=5):
    super().__init__(hand_count, hand_size)

  def strategize(self, node): #would actually be nicer if this took node as an input, but that's not consistent with the other players
    # node = gamestate.node
    possible_moves = node.moves_remaining
    # print(possible_moves)
    return possible_moves[0]
    
class DepthFirstGame(chopsticksGame.Gamestate):
  def __init__(self, size, hand_count=2, hand_size=5):
    super().__init__()

    for i in range(0, size):
      self.add(DepthFirstPlayer(hand_count, hand_size))

    for player in self.players:
      for hand in player.hands:
        player.get_hit(1, hand)



