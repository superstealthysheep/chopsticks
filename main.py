import chopsticksGame
import players

def main():
  # g = chopsticksGame.Gamestate()
  # p1 = chopsticksGame.Player()
  # p2 = chopsticksGame.Player()
  # g.add(p1)
  # g.add(p2)

  # for player in g.players:
  #   for i in range(len(player.hands)):
  #     player.get_hit(1, i)

  # g.print()
  # print("\n" + "#"*10)
  random_game()
    
# def play_game(): #i'm just having fun now. this is a game between you and a random ai
#   g = chopsticksGame.Gamestate()
#   p1 = chopsticksGame.Player()
#   p2 = chopsticksGame.Player()

def random_game():
  g = chopsticksGame.Gamestate()
  p1 = players.RandomPlayer()
  p2 = players.HumanPlayer()
  #p3 = chopsticksGame.Player()
  g.add(p1)
  g.add(p2)
  #g.add(p3)

  for player in g.players:
    for i in range(len(player.hands)):
      player.get_hit(1, i)

  g.print()

  #random game loop
  while not g.done():
    active_player = g.players[g.active_player_index]

    active_player.strategize(g)
    target_player = active_player.target_player
    target_hand = active_player.target_hand
    attack_hand = active_player.attack_hand
    sticks = active_player.hands[attack_hand]

    target_player.get_hit(sticks, target_hand)

    g.next_player()
    g.print()
    

main()