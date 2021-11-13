class Player:
    def __init__(self):
        self.hands = [0,0]
        self.human = False

    def fingers(self, hand): #returns how many fingers are up on the given hand
        return self.hands[hand]
  
    def hit(self, sticks, hand): #runs when you get hit
        self.hands[hand] = (self.hands[hand] + sticks) % 5

    def can_i_split():
        nonzero_hand_counter = 0;
        for hand in self.hands:
            if self.fio


    def split(self): #only can run if 

