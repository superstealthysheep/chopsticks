#A library used to analyze and display the graphs created by logger.py

import logger
import chopsticksGame
import players
import presets
import copy
from pyvis.network import Network
import networkx as nx

class Displayer: #a new object that holds most of the info found by the logger, but throws out some of the stuff we no longer use. this is just for nicer modularity/compartmentalizatoin
  def __init__(self, logger_source):
    self.node_list = logger_source.node_list
    self.starting_node = logger_source.starting_node
    self.win_dict = self.find_win_nodes()
    self.strong_node_dict = self.find_strong_win_ancestors()
    self.weak_node_dict = self.find_weak_win_ancestors()
    self.color_dict = {"default":"#9e9e9e", "start":"#00ff00", 
      "wins":["#1653b5",  "#b51633", "#ff8833", "#c929e6"], 
      "weaks":["#82b2ff", "#ff7d95", "#ffb37d", "#f09eff"],
      "strongs":["#4080e6", "#de4964", "#f0a169", "#da65f0"]}
      # "weaks":["#000000","#000000","#000000","#000000"]}

    self.color_nodes()

  def color_nodes(self, nodes_to_color=None): #pass in a list of nodes to color and it'll set their colors
    #hacky "paragraph" but I'm in a rush:
    strong_nodes = []
    weak_nodes = []
    for player in self.node_list[0].gamestate.players:
      strong_nodes.extend(self.strong_node_dict[player.id])
      weak_nodes.extend(self.weak_node_dict[player.id])

    if not nodes_to_color:
      nodes_to_color = self.node_list
    for node in nodes_to_color:
      node.color = self.color_dict["default"] #default--a light gray
      if node == self.starting_node:
        node.color = self.color_dict["start"]
      elif node.gamestate.done():
        winner_id = node.gamestate.players[node.gamestate.active_player_index].id
        node.color = self.color_dict["wins"][winner_id]
      elif node in strong_nodes:
        for winner_id, node_list in self.strong_node_dict.items():
          if node in node_list:
            node.color = self.color_dict["strongs"][winner_id]
            break
      elif node in weak_nodes:
        for winner_id, node_list in self.weak_node_dict.items():
          if node in node_list:
            node.color = self.color_dict["weaks"][winner_id]
            break

  #########
  #Parent-finding functions
  #########
  def find_weak_parents(self, target_nodes): #returns a list including the target nodes and all nodes that have a target node as a child
    output_list = copy.copy(target_nodes)
    for parent_candidate in self.node_list:
      if parent_candidate in output_list:
        continue #skip adding this candidate since they're already there
      for child_candidate in target_nodes:
        if child_candidate in parent_candidate.children:
          output_list.append(parent_candidate)
          break
    return output_list

  def find_strong_parents(self, target_nodes): #returns a list including the target nodes and all nodes that inevitably lead returns a list including the target_nodes and all "strong" parents whose children are either target_nodes or fellow strong parents
    output_list = copy.copy(target_nodes)

    #the way this works is taking the list of all the parents of target_nodes, then culling out any parents that have children not in strong_parent_list. This occurs recursively until the length of strong_parent_list stabilizes.

    num_found = 0
    old_num_found = -1
    while (num_found > old_num_found):
      for candidate in self.find_weak_parents(target_nodes):
        if candidate in output_list:
          continue
        elif set(candidate.children).issubset(set(output_list)):
          output_list.append(candidate)
      
      old_num_found = num_found
      num_found = len(output_list)

    return output_list

  def find_win_nodes(self): #returns a dict where the keys are the winner's player id and the values are lists of nodes where they won
    win_dict = {} #this is a dict because we can't necessarily trust the player ids to be conseutive integers starting at 0
    for node in self.node_list:
      if node.gamestate.done():
        winner_id = node.gamestate.active_player_index
        if winner_id not in win_dict:
          win_dict[winner_id] = []
        win_dict[winner_id].append(node)

    return win_dict

  def find_strong_win_ancestors(self): #finds all strong ancestors of win conditions for each player, ie.e all nodes where a win is now guaranteed for one player
    # node_pool = copy.copy(self.node_list)
    strong_dict = copy.copy(self.win_dict)
    for player_id in self.win_dict:
      last_size = 0
      strong_ancestor_list = strong_dict[player_id] #this is an alias for legibility
      while last_size < len(strong_ancestor_list):
        last_size = len(strong_ancestor_list)
        strong_ancestor_list = self.find_strong_parents(strong_ancestor_list)

      strong_dict[player_id] = strong_ancestor_list #oh wait, the reference is broken in find_strong_parents, so we need to do this

    return strong_dict

  def find_weak_win_ancestors(self): #again, algo might be suboptimal but it gets the job done, i guess? I couldn't immediately think of a more clever bulletproof way to do this 
    weak_dict = copy.copy(self.strong_node_dict) #this might not need to be a copy if that's how python scope works

    for winner_id, weak_list in weak_dict.items():
      layer_n = copy.copy(weak_list)
      layer_n_plus_one = []
      old_weak_list_length = 0
      # weak_list.clear() #this is nicer than weak_list = [] because weak_dict is updated to match this, instead of creating a new reference called weak_list

      while len(weak_list) > old_weak_list_length:
        
        #step 1: identify the PRIVILEGED children
        privileged_children_list = [] #the *priveleged* children where their parents had other options, but chose THEM! the other children were chosen only because they were the only choice remaining) I swear I'm not going insane
        for node in layer_n:
          if find_previous_active_player(node.gamestate).id == winner_id: #if the previous move was made by the winner, add all the weak parents of the node to our list
            privileged_children_list.append(node)

        #step 2: add the (all the weak) parents of the PRIVELEGED children to the newcomer list
        layer_n_plus_one.extend(self.find_weak_parents(privileged_children_list)) 
        #but in all seriousness, the reason why we can do this is if, e.g. we're rooting for player 0 to win right now, and in all of node's parents player 0 is the active player, we don't need for those parents to be strong parents of node. All that matters is that they are parents of some kind, and then player 0 can just choose to make the correct move.

        #step 3: add the (only the strong) parents of all the children
        layer_n_plus_one.extend(self.find_strong_parents(layer_n))
        #Meanwhile, if we're rooting for player 0 to win, but *player 1* was the active player in all of node's parents, we need a guarantee that player 1 will make that move that we need, and we can only guarantee that for *strong* parents of node. for the weak parents, player 1 could well make a different choice that we don't like :( thank you for listening to my ted talk

        #step 4: no more duplicates!
        layer_n_plus_one = list(set(layer_n_plus_one))
        old_weak_list_length = len(weak_list)
        weak_list.extend(layer_n_plus_one)
        weak_list = list(set(weak_list))
        layer_n = layer_n_plus_one

      weak_dict[winner_id] = weak_list

    print(weak_dict)
    return weak_dict #ughhh duplicates
  
def find_previous_active_player(gamestate): #returns last living player before the active_player. works by looping through player list backwards, starting from player before active player. This function probably doesn't belong here, but again, I'm too tired to give a ..darn. Maybe I'll fix it later ;)
  # print("bonk!")
  for index in range(gamestate.active_player_index - 1, gamestate.active_player_index - len(gamestate.players) - 1, -1):
    player = gamestate.players[index]
    # print("player: {}".format(player))
    if player.check_alive():
      return player #note: this COULD be the active player iff they're the last player standing

  

    
        



      

    
    