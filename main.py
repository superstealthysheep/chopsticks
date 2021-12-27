import chopsticksGame
import players
import presets
import logger

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