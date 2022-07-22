msg = """This is the main Python file in my AI Othello Player.
There are three (planned) versions:
\t1) Random moves: The AI will make random moves without considering what effect it may have on its success during the game.
\t2) Minimax: The AI will make moves that are the best possible for itself using the Minimax algorithm.
\t3) Self-play: The AI will develop a strategy based off the games it plays against itself.
These algorithms can be found in respective folders \x1b[1;31m(random, minimax, self-play)\x1b[0m.

Utility files used for determining game state and running a terminal game can be found in \x1b[1;31m(utils)\x1b[0m."""

print(msg)