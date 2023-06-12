========CAPSTONE PROJECT========

1. Nguyen Hai Nam 20205188
2. Phi Viet Hoang 20205153
3. Bui Hoang Ha 20205149
4. Nguyen Tien Duy 20200801

========INFORMATION========
This program is a basic chess game with built-in chess AI.
The main goal of the project is to create a chess AI.
Our AI may not be smart for a pro but surly a real nightmare for beginner.

========ALGORITHMS========
1. We count the relative strength of the pieces on the board with respect to their strength to choose best move.
2. We use Minimax algorithm to create a search tree. The higher the depth is, the more effectively our AI perform.
3. We use Alpha-beta pruning to optimize run time, which leads to higher depth (my laptop can handle the highest DEPTH = 4).
4. We improve the initial evaluation function to make our AI smarter.

========TECHNOLOGIES========

1. Python 3.10
2. Pygame 2.1.2

========INSTRUCTIONS========

* How to run the game? 
(Skip step 1 + 2 if you've already installed python and pygame)

1. Install python at "https://www.python.org/".
2. In Command Prompt enter "pip install pygame" to install pygame library.
3. Run program: in Command Prompt, go to the project folder, enter "py Main.py".
4. Hope you can beat the AI.

* How to play the game?
1. Open file "Main.py", go to line 34 and 35, edit "player1 = True" and "player2 = False" if you want to play as player 1 or "player1 = False" and "player2 = True" if you want an AI take over player 1.
2. Open file "Main.py", go to line 82, edit "findBestMoveAlphaBetaPrunning" (AlphaBeta prunning algorithm) to "findBestMoveGreedy" (Greedy algorithm), "findBestMoveMinMax" (Minimax Algorithm), or "findBestMoveNegaMax" (Negamax Algorithm). 
3. Open file "SmartMove.py", go to line 62, edit "DEPTH = ..." to choose depth.
4. Start game by Terminal: 
- First, enter command "cd <Path to file Main.py>".
- After that, enter command "py Main.py".
5. First click to choose a piece, second click to play a move with that piece.
6. Press "z" to undo a move.
7. Press "r" to reset the game.
8. The game ends whenever a checkmate or a stalemate occur.

!!!ENJOY!!!