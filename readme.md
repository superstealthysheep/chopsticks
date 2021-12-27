# chopsticks
### Goals 
Ultimately, to make a graph of all possible Chopsticks game states. 

Subgoals:

1. ~~Simulate the game Chopsticks~~ (it can even do games with arbitrary player counts, hands per player, and fingers per hand!)
2. ~~Make a program that will try every possible move and make a big tree~~ (could probably be optimized, but it works well enough for now)
3. Visualize the tree with a cool graph
4. ???
5. Profit

### Regional Chopsticks rules
1. You can only split from an even-fingered lonely hand (a hand without a partner)
2. Splits must be neatly in half
3. Splitting counts as a turn

### Project history
In August I started wondering if I could find out an optimal Chopsticks strategy. I started out by making a graph of a bunch of game states. 
It soon became quite tedious, so I decided I'd write a program to do it or something. 
There's an upper bound of (5 fingers)^(4 hands)\*(2 players whose turn it could be) = 1250 gamestates, each with at most two edges to children, so this graph should be quite achievable.

On 11/10/2021 I mentioned it to my compsci TA Henri, and he made us a replit to start working. That weekend, I barely slept and did no homework, but I created a logger! That was broken!!!! Then I was busy until the end of the semester.

On 12/25/2021 I fixed the logger!
