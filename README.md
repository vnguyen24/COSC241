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

- What could have been better: I wish we didn't have to hardcode that much.


Project 2: Game playing - Adversarial search

- Files I edited: multiAgents.py

- Project description: The project tackles search algorithms that are used when there are adversaries (ghosts in this case). The ones we studied were Reflex, Minimax, Minimax with Alpha-Beta pruning, Expectimax.

- What I learned: Recursion for Minimax-related algorithms, how to design a good evaluation function, the fact that Minimax can be applied on multiple agents, not just agent MIN and agent MAX.

- What went wrong: I was very weak in recursion, so Minimax, especially with Alpha-Beta pruning, gave me a really hard time. I couldn't understand what was going on, and even when I had a vague idea of the concept, I didn't know how to implement the algorithm. I ended up asking for input from another peer, which was not allowed per the course policy. Fortunately, Prof. Alfeld was generous enough to give me a chance to show him that I understood the material. As a consequence, I created a PowerPoint explaining how Minimax works, using the game Civilization VI as an example, along with the pseudocode for the algorithm.

- What could have been better: I wish I was better taught in Intro to CS II.


Project 3: Reinforcement learning

- Files I edited: analysis.py, qlearningAgents.py, valueIterationAgents.py

- Project description: The project challenges us on common reinforcement learning algorithms, such as Value Iteration, Q-Learning (With Epsilon-greedy), approximate Q-Learning.

- What I learned: All the shown algorithms, Q-learning on features and not just states

- What went wrong: Nothing really went wrong for this project. In fact, this is the topic I enjoyed the most in the course!

- What could have been better: I wish I knew what's going on in the background: The code for simulation was given to us, so I'm not sure how everything runs together and adjust the features' values. I also want to learn more about TD Q-learning, especially its runtime and how it is more efficient than other model-based learning algorithms, as I didn't quite understand that part.


Project 4: Reasoning under uncertainty

- Files I edited: busterAgents.py, inference.py

- Project description: This project tackles reasoning under uncertainty algorithms such as Exact Inference, Approximate Inference, Joint Particle Filtering, which allows Pacman to hunt down the ghosts, whose positions are unknown.

- What I learned: All the said algorithms, reasoning under uncertainty with time.

- What went wrong: I was solid in Probability, but in no way great at it. So although implementation wasn't a problem this time, I had a relatively challenging time understanding how an algorithm works in theory. Also, using a given library that I didn't write means spending extra time learning about how to use that library. 

- What could have been better: I didn't completely understand Joint Particle Filtering (though I understood Particle Filtering quite well), so I wish I had the chance to redo this part of the project.


Final Project: Pacman capture the flag (CTF)

- Files I edited: myTeam.py

- Project description: It's a CTF tournament between 8 teams. I believe this is a tradition at the end of every course that uses the UC Berkeley framework. The goal is to eat as many of the opponent food dots as possible, while also defending as many of our own food dots as possible.

- What I learned: How to design an even more complex evaluation function, how to read and comprehend given code efficiently.

- What went wrong: Although using an evaluation function was a good start, we couldn't break through and utilize a more sophisticated algorithm.

- What could have been better: I wish we were able to figure out how to apply Reinforcement Learning to this project


This is my recap for COSC241 - Artificial Intelligence.
