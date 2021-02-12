# hog_contest
 UC Berkeley Spring 2021 Hog Contest Participant Team: `CookEs` Source Code

## Design Concept
Since @ToiletCommander studied `XSTAT 2` during his freshman Fall19 FPF Semester, he considered using a probability model to estimate the win rate for rolling `n` dices at a given point to compete in the HOG contest.   

This turns out initially to not work well because final_strategy was designed to work based on the history of the game.

60,000 games against roll(6), 20,000 games against more_boar
 - Ranked #2 on the leaderboard
 - Lose Rate(Against Teenis Bot, ranked #1 during submission): 0.514374540901

1 Epochs(of 10,000 games each for more boar and optimal training)
 - Win Rate(Against More_Boar): 0.637709008522221
 - Win Rate(Against Optimal, Sample of 5000): Didn't test
 - Lose Rate(Against Teenis Bot): 0.674265235367 (For some reason, it might be there is an error in cache codes)

2 Epochs(of 10,000 games each)
 - Win Rate(Against More_Boar): OMG Service Unavilable
 - Win Rate(Against More_Boar, Sample of 1500): 0.803
 - Win Rate(Against Optimal, Sample of 5000): 0.462
 - Lose Rate(Against Tennis Bot): Didn't submit

10 Epochs(of 10,000 games each)
 - Ranked #1
 - Win Rate(Against More_Boar): 0.6434462
 - Win Rate(Against More_Boar, Sample of 1500): 0.8146667
 - Win Rate(Against Optimal, Sample of 5000): 0.4678
 - Lose Rate(Against Tennis Bot): 0.499621698987
 - Win Rate(Against Teenis Bot, Ranked #2): 0.500378301013

30 Epochs(of 10,000 games each)
