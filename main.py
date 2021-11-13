import chopsticksGame
import players
import presets

def main():
  rg = presets.RandomGame(2, 3, 10) #a game with 2 players, each with 3 hands with 10 fingers
  rg.run_game()


main()
