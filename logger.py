import copy
import chopsticksGame
import players

class GamestateNode(): #extends Gamestate but also stores children, possible moves, moves tried
  id_counter = 0
  node_list = []

  def __init__(self, gamestate):
    # self.gamestate = chopsticksGame.Gamestate.deepcopy(parent_gamestate) #copies all those instances from parent instance. Deep copy is so that e.g. Player objects are static wrt time
    self.gamestate = gamestate
    active_player = self.gamestate.players[self.gamestate.active_player_index]
    self.children = []

    #initialize move list
    self.all_moves = active_player.list_all_moves(self.gamestate)
    # self.moves_tried = [] #this one might be unnecessary
    self.move_log = [] #will hold move/destination pairs for all moves taken
    self.moves_remaining = self.all_moves
    # self.initialize_move_list()

    self.id = GamestateNode.id_counter
    GamestateNode.id_counter += 1

    GamestateNode.node_list.append(self)

  def __repr__(self):
    return "GamestateNode {}".format(self.id)

    # for move in active_player.list_all_moves(self.gamestate):
    #   print(move)

  @classmethod
  def id_to_node(cls, id):
    for node in cls.node_list:
      if node.id == id:
        return node
    raise ValueError("Invalid node id")
    return False

  @classmethod
  def pop_last_node(cls, id_to_pop): #doesn't actually delete it, just allows its id to be reused. the id input is for verification
    if id_to_pop == cls.id_counter - 1:
      cls.id_counter -= 1

      cls.node_list.pop().id = -1 #both removes the node from the list and sets its id to -1
    else:
      raise ValueError("Tried to pop a node that is not at the end")

  @classmethod
  def sufficiently_deep_copy(cls, parent_node): #basically a shallow copy EXCEPT the gamestate is a deep copy. Children are copied shallowly (cause otherwise computation time increases exponentially ._. whoops). Moves technically don't need to be copied, but they're in there bc that's part of the shallow copy
  #used to make children basically
    child_node = copy.copy(parent_node)
    child_node.children = [] #whooops, forgot about this too
    child_node.move_log = []
    child_node.gamestate = copy.deepcopy(parent_node.gamestate)

    return child_node


  @classmethod
  def make_child(cls, parent_node, move): #given a parent node and a move, returns a new "child" node created from the parent and the move
    # child_node = copy.deepcopy(parent_node) #copy.deepcopy or cls.deepcopy()?
    child_node = cls.sufficiently_deep_copy(parent_node)

    #update id of the node
    child_node.id = cls.id_counter
    cls.id_counter = cls.id_counter + 1

    #update the id of the gamestate CONTAINED INSIDE the node
    child_node.gamestate.id = chopsticksGame.Gamestate.id_counter
    chopsticksGame.Gamestate.id_counter = chopsticksGame.Gamestate.id_counter + 1

    GamestateNode.node_list.append(child_node) ########RETURN HERE AND COMMENT IT OUT
    move.transplant(parent_node.gamestate, child_node.gamestate) #creates a new Move object
    
    active_player = move.attack_hand.owner
    if move.type == "split":
        active_player.split() 
        print("Did it split right?")
    elif move.type == "attack":
      target_player = move.target_player
      target_hand = move.target_hand
      sticks = move.attack_hand.fingers
      target_player.get_hit(sticks, target_hand)
    else:
      raise ValueError("Invalid command given by player {}".format(active_player))

    child_node.gamestate.next_player()
    child_node.initialize_move_list() #recalculate the possible moves for the child
    return child_node

  # @classmethod
  # def deepcopy(cls, parent_node):
  #   child_node = copy.deepcopy(parent_node) #copy.deepcopy or cls.deepcopy()?
  #   child_node.id = cls.id_counter
  #   cls.id_counter = cls.id_counter + 1
  #   cls.

  def initialize_move_list(self):
    active_player = self.gamestate.players[self.gamestate.active_player_index]
    self.all_moves = active_player.list_all_moves(self.gamestate)
    self.moves_remaining = self.all_moves

  def log_move(self, move, child): #updates the lists of moves for this node, and also adds child to the node's children list
    # self.moves_tried.append(move)
    self.moves_remaining.remove(move)
    if child not in self.children:
      self.children.append(child) #the if statement is because it's possible for two different moves to output the same gamestate, e.g. player 0 in (1,1),(0, 1) has two ways to attack to return (1,1),(0,2)
    self.move_log.append({"move":move, "child":child})


class Logger(): #takes a gamestate as input, not a node
  def __init__(self, starting_gamestate):
    self.node_list = []
    self.unexhausted_nodes = []
    # self.gamestate_list = [] #this is janky to have. it's a list parallel to node_list containing only the gamestates 
    # self.last_viable_node #is the most recently visited node with moves not yet tried
    # self.starting_gamestate = starting_gamestate
    # self.gamestate = self.starting_gamestate
    self.starting_node = self.create_node(starting_gamestate)
    # starting_gamestate.node = self.starting_node
    self.node = self.starting_node
    # self.node_list.append(self.starting_node) #accidentally redundant
    self.move_log = [] #stores dicts of move/destination pairs

    # self.history = []
  
  def done(self):
    pass

  def create_node(self, gamestate): #creates the new node and sets gamestate.node to [a reference to that node] 
    new_node = GamestateNode(gamestate)
    # new_gamestate = new_node.gamestate
    # new_node.gamestate.node = new_node ##jankkkkk #note: gamestate != new_node.gamestate because new_node.gamestate is a deep copy of gamestate, not a reference to it
    # new_node.gamestate.node = new_node
    self.node_list.append(new_node)
    # self.gamestate_list.append(gamestate)

    if len(new_node.moves_remaining) > 0:
      self.unexhausted_nodes.append(new_node)
      print("++++++++++++++++++++++new unexhausted")

    return new_node

  def gamestate_to_node(self, gamestate):
    for node in self.node_list:
      if node.gamestate.equals(gamestate):
        return node
    else:
      return None

  def run_game(self):
    self.node.gamestate.print()
    
    while len(self.unexhausted_nodes) > 0:

      active_player = self.node.gamestate.players[self.node.gamestate.active_player_index]

      print("active player: {}".format(active_player))
      move = active_player.strategize(self.node)

      print("Game loop move: {}".format(move))

      #handling if the node is exhausted
      if move.type == "exhausted":
        self.unexhausted_nodes.pop()
        try:
          next_node = self.unexhausted_nodes[-1] #typo found here?
        except IndexError: #if no unexhausted nodes remain
          print("Out of unexhausted nodes. Breaking..")
          break
        else:
          print("EXHAUSTED. Returning to:")
          next_node.gamestate.print()
          print() #to help my EYES. divides consecutive nodes in the printout

      #if the node isn't exhausted, find its child
      else:
        print() #to help my EYES. divides consecutive nodes in the printout
        parent_node = self.node
        child_node = GamestateNode.make_child(parent_node, move)

        replacement_child = self.gamestate_to_node(child_node.gamestate) #searches in the existing list of gamestates to see if there's a previous one which the child is a duplicate of
        if replacement_child: #and not replacement_child.equals(child_node): #why do we need to check if (replacment node)? isn't it guaranteed to be true if we just created that child node?
          print("!!!!!Repeated gamestate {}! deleting newborn node ({})...".format(replacement_child.gamestate.id, child_node.id))
          GamestateNode.pop_last_node(child_node.id)#deletes the child node
          child_node = replacement_child
        else:
          print("This gamestate {} has not appeared before. Keeping newborn node ({})...".format(child_node.gamestate.id, child_node.id))
          self.node_list.append(child_node)
          self.unexhausted_nodes.append(child_node)
        parent_node.log_move(move, child_node) #wow, the parent will only accept the child after they've proven themself to be of use. heartless... 
        next_node = child_node

      self.node = next_node
      self.node.gamestate.print()
      
    print(self.unexhausted_nodes)

class DepthFirstPlayer(chopsticksGame.Player): #takes the first move available in the list stored for that gamestate
  def __init__(self, hand_count=2, hand_size=5):
    super().__init__(hand_count, hand_size)

  def strategize(self, node): #would actually be nicer if this took node as an input, but that's not consistent with the other players
    # node = gamestate.node
    possible_moves = node.moves_remaining
    # print(possible_moves)
    try:
      return possible_moves[0]
    except IndexError: #if there are no possible moves left, return "exhausted"
      return chopsticksGame.Move("exhausted")
    
class DepthFirstGame(chopsticksGame.Gamestate):
  def __init__(self, size, hand_count=2, hand_size=5):
    super().__init__()

    for i in range(0, size):
      self.add(DepthFirstPlayer(hand_count, hand_size))

    for player in self.players:
      for hand in player.hands:
        player.get_hit(1, hand)

  def __repr__(self):
    return "DepthFirstGame {}".format(self.id)



