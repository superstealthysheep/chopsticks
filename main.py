import chopsticksGame
import players
import presets
import logger
from pyvis.network import Network

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
starting_gamestate = logger.DepthFirstGame(2,2,5)
lg = logger.Logger(starting_gamestate) 
lg.run_game()

print("$$$$$$$$$$")

for node in lg.node_list:
  node.gamestate.print()

print(len(lg.node_list))

##################
#  PYVIS TIME
def better_add_node(net, node):
  color = "#a7c0f7" #default--a light blue
  if node.id == 0:
    color = "#00ff00"
  elif node.gamestate.done():
    color_array = ["#1653b5", "#b51633", "#ff8833", "#ff8833"]
    # color = "#000000"
    active_player = node.gamestate.players[node.gamestate.active_player_index]
    color = color_array[active_player.id]

  net.add_node(node.id, node.id, color=color, title=newlines_to_brs(str(node.gamestate)))

def newlines_to_brs(input):
  split_input = input.split("\n")
  output = "<br>".join(split_input)
  return output

edge_counter = 0

net = Network(height='750px', width="50%")
for node in lg.node_list:
  # net.add_node(node.id, node.id, color="#00ff00")
  better_add_node(net, node)
  for move_child_pair in node.move_log:
    # net.add_node(child.id, child.id, color="#000000")
    child = move_child_pair["child"]
    move = move_child_pair["move"]
    print("Node {}: {}".format(node.id, move_child_pair))
    better_add_node(net, child)
    net.add_edge(node.id, child.id, arrows="to", label=str(move))
    edge_counter = edge_counter + 1

  # if node.gamestate.done():
  #   net.add_node(node.id, color="#000000")

  # net.add_node(0, color="#ff0000")
  # net.barnes_hut(overlap=1)
    
net.show_buttons(filter_=["physics"])
net.show("output.html")
print("{} edges".format(edge_counter))