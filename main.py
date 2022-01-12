import chopsticksGame
import players
import presets
import logger
import displayer
from pyvis.network import Network
import networkx as nx

# def main():
  # rg = logger.DepthFirstGame(2, 2, 5) #a game with 2 players, each with 3 hands with 10 fingers
  # l = logger.Logger(rg)
  
  # l.run_game()
  # # for g in l.gamestate_list:
  # #   g.print()
  # # for mv in l.history:
  # #   print(mv)

  # # g_node = logger.GamestateNode(rg)
  # # print(g_node.gamestate.active_player_index)

  # # rg = presets.RandomGame(2)
  # # print(rg.players[rg.active_player_index].list_all_moves(rg))

# # main()
# rg = logger.DepthFirstGame(2, 2, 3) #a game with 2 players, each with 3 hands with 10 fingers
# l = logger.Logger(rg)

# l.run_game()
starting_gamestate = logger.DepthFirstGame(3,2,2)
lg = logger.Logger(starting_gamestate) 
lg.run_game()
disp = lg.make_displayer()

print("$$$$$$$$$$")

# for node in lg.node_list:
#   node.gamestate.print()

print(len(disp.node_list))



##################
#  PYVIS TIME
def better_add_node(net, logger_node):
  # if logger_node.id not in disp.weak_node_dict[0]:
  #   return None

  net.add_node(logger_node.id, logger_node.id, color=logger_node.color, title=newlines_to_brs(str(logger_node.gamestate)), shape="circle")


def fix_node_height(node, y):
  node["y"] = y
  node["fixed"] = {"x":False, "y":True} #HEYYY THIS WORKS
  # node["physics"] = False

def newlines_to_brs(input):
  split_input = input.split("\n")
  output = "<br>".join(split_input)
  return output

edge_counter = 0
vertical_spacing = 200 #used to separate nodes by generation/depth

net = Network(height='100%', width="100%")
for logger_node in disp.node_list:
  # net.add_node(node.id, node.id, color="#00ff00")
  better_add_node(net, logger_node)
  node = net.get_node(logger_node.id)
  # fix_node_height(node, vertical_spacing * logger_node.depth)


  for move_child_pair in logger_node.move_log:
    # net.add_node(child.id, child.id, color="#000000")
    child = move_child_pair["child"]
    move = move_child_pair["move"]
    # print("Node {}: {}".format(logger_node.id, move_child_pair))
    # better_add_node(net, logger_node) #parent
    better_add_node(net, child)
    net.add_edge(logger_node.id, child.id, arrows="to", title=str(move), label=str(move), color={"inherit":"to"})
    edge_counter = edge_counter + 1


# net.barnes_hut(gravity=-80000, central_gravity=0.3, spring_length=250, spring_strength=0.001, damping=0.09, overlap=0)
# net.enable_physics(False)  
net.hrepulsion(node_distance=500, central_gravity=0.0, spring_length=100, spring_strength=0.01,
damping=0.09)  
# net.show_buttons(filter_=["physics", "edges", "nodes"])
# net.show_buttons(filter_=["physics"])


# for node in net.get_nodes():
#   if 


net.show("output.html")
print("{} edges".format(edge_counter))

print(disp.win_dict)
print(disp.weak_node_dict)
print(disp.strong_node_dict)