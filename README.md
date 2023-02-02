# COSC241
Course partner: Maxine Dobbs (mdobbs25@amherst.edu). Instructor: Professor Scott Alfeld.


This is the COSC241 - Artificial Intelligence repo. Below is a list of files I wrote and modified, using the UC Berkeley Pacman framework. I am also using this readme file to share with you what I learned in each project, what went right and wrong (mostly wrong), and potentially more.


Project 0:

- Files I edited: addition.py, buyLotsOfFruit.py, shop.py, shopSmart.py

- Project description: Just a mini-Python tutorial since students are assumed to have no prior experience in Python programming. This is also the only project that didn't go wrong.

- What I learned: I was re-familiarized with Python


Project 1: Search algorithms - Updating code

- Files I edited: search.py, searchAgents.py

- Project description: The project tackles some of the most common search algorithms (Depth First Search, Breadth First Search, Uniform Cost Search, A*)

- What I learned: All the said search algorithms, how to argue for heuristic admissibility and consistency, how to design/come up with a good heuristic.

- What went wrong: When I calculated the heuristic in Q7 using the closest food dot, the code didn't execute as expected. As it turned out, after eating the closest food dot, the distance to closest food dot increases, therefore increasing the heuristic, making it inconsistent. A workaround is to calculate heuristics using the furthest food dot.

- What could have been better: I wish we didn't have to hardcode cases that much.

Project 2: Game playing - Adversarial search

- Files I edited: multiAgents.py

- Project description: The project tackles search algorithms that are used when there are adversaries (ghosts in this case). The ones we studied were Reflex, Minimax, Minimax with Alpha-Beta pruning, Expectimax.

- What I learned: Recursion for Minimax-related algorithms, how to design a good evaluation function

- What went wrong: I was very weak in recursion, so Minimax, especially with Alpha-Beta pruning, gave me a really hard time. I couldn't understand what was going on, and even when I had a vague idea of the concept, I didn't know how to implement the algorithm. I ended up asking for input from another peer, which was not allowed per the course policy. Fortunately, Prof. Alfeld was generous enough to give me a chance to show him that I understood the material. As a consequence, I created a PowerPoint explaining how Minimax works, using the game Civilization VI as an example, along with the pseudocode for the algorithm.
