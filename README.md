# hog_contest
 UC Berkeley Spring 2021 Hog Contest Participant Team: `CookEs` Source Code

## Design Concept
Since @ToiletCommander studied `XSTAT 2` during his freshman Fall19 FPF Semester, he considered using a probability model to estimate the win rate for rolling `n` dices at a given point to compete in the HOG contest.   

This program computes the win rate of throwing n dices when scores are (x, y), assuming that the opponent will always choose the numRoll with the biggest winning chance using dynamic programming.   

This turns out initially to not work well because final_strategy was designed to work based on the history of the game. Then we would use randomly generated matchups to generate hit rate data and use those hit data to estimate the history of the game on the actual runs.   

## Iteration of strategies

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
- Ranked ?
- Win Rate(Against More_Boar): 0.642815624095647
- Win Rate(Against More_Boar, Sample of 2500): 0.8228
- Win Rate(Against Optimal, Sample of 5000): 0.467
- Win Rate(Against Tennis Bot, Ranked #2): Not Submitted

1 Epoch(of 10,000 games against optimal)
- Ranked 1
- Win Rate(Against More_Boar): 0.6439756737689091
- Win Rate(Against More_Boar, Sample of 2500): 0.7876
- Win Rate(Against Optimal, Sample of 5000): 0.477
- Win Rate(Against Tennis Bot, Ranked #2): 0.509287074898

10 Epoch(of 10,000 games against optimal) 2021-2-12 11:50 PM Chinese Standard Time
- Ranked 1
- Win Rate(Against More_Boar): 0.64514360905949
- Win Rate(Against More_Boar, Sample of 2500): 0.7856
- Win Rate(Against Optimal, Sample of 5000): 0.4616
- Win Rate(Against Tennis Bot, Ranked #2): 0.509687099966 => 0.515778508680(Tennis Bot changed its code)

30 Epoch(of 10,000 games against optimal) 2021-2-13 9:00 AM Chinese Standard Time
- Ranked 1
- Win Rate(Against More_Boar): 0.6449884708451865
- Win Rate(Against More_Boar, Sample of 2500): 0.792
- Win Rate(Against Optimal, Sample of 5000): 0.481
- Win Rate(Against Tennis Bot, Ranked #2): 0.515966269520

50 Epoch(of 10,000 games against optimal) 2021-2-13 11:00 AM Chinese Standard Time
- Ranked 1
- Win Rate(Against More_Boar): 0.6450820140965935
- Win Rate(Against More_Boar, Sample of 2500): 0.7792
- Win Rate(Against Optimal, Sample of 5000): 0.471
- Win Rate(Against Tennis Bot, Ranked #2): Not submitted
- Win Rate(Against 30 Epoch): 0.49936865260350893
- Win Rate(Against 10 Epoch): 0.5006358086087815

1 Epoch(of 10,000 games against optimal, with fair start) 2021-2-13 11:20 AM CN Time
- Ranked 1
- Win Rate(Against More_Boar): 0.6445944815554959
- Win Rate(Against More_Boar, calculated locally): 0.7887243139046971
- Win Rate(Against Optimal, calculated locally): 0.47040312907454074
- Win Rate(Against Tennis Bot, Ranked #2): 0.516818765350
- Win Rate(Against 30 Epoch not fair): 0.5009886615042825
- Win Rate(Against 30 Epoch not fair, calculated locally): 0.5012659637901775
- Win Rate(Against 10 Epoch not fair): 0.5023755757836526
- Win Rate(Against Master Hog, Ranked #3): 0.499276426183

10 Epoch(of 10,000 games against optimal, with fair start) 2021-2-13 23:00 PM CN Time
- Ranked 1
- Win Rate(Against More_Boar): 0.6432668941111305
- Win Rate(Against More_Boar, calculated locally): 0.7892700496386653
- Win Rate(Against Optimal, calculated locally): 0.47084969932901544
- Win Rate(Against Tennis Bot, Ranked #2): Not Submitted
- Win Rate(Against 1 Epoch Fair): 0.497628323383721
- Win Rate(Against 1 Epoch Fair, calculated locally): 0.49862808048268126

2021-2-23 12:06 PM CN Time
- Seems like I understand one game rule wrong lol
- Retraining..

1 Epoch (of 20,000 games against optimal, with fair start) 2021-2-13 14:00 CN Time
- Win Rate(Against More_Boar): 0.6738015531783106
- Win Rate(Against More_Boar, calculated locally): 0.7013523354848239
- Win Rate(Against Optimal, calculated locally): 0.40433238585636067
- Win Rate(Against Penguins, Ranked #1): 0.475869216119
- Win Rate(Against 1 Epoch Fair): 0.5012480448243526
- Win Rate(Against 1 Epoch Fair, calculated locally): 0.5007240227951439

10 Epoch (of 20,000 games against optimal, with fair start) 2021-2-13 16:00 CN Time
- Win Rate(Against Penguins, Ranked #2): 0.479203114552
- Win Rate(Against okonoko, Ranked #1): 0.442300378058

1 Epoch Ultimate (of win rate prediction) 2021-2-13 20:10 CN Time
- Win Rate(Against More_Boar): 0.6738015531783106
- Win Rate(Against More_Boar, calculated locally): 0.7138769932697604
- Win Rate(Against Optimal, calculated locally): 0.40346881968464243
- Win Rate(Against 10 Epoch Fair): 0.47357561852699
- Win Rate(Against 10 Epoch Fair, calculated locally): 0.5009814053601395

1 Epoch Ultimate1 (of win rate prediction) 2021-2-13 20:10 CN Time
- Win Rate(Against More_Boar, calculated locally): 0.7159359601282804
- Win Rate(Against Optimal, calculated locally): 0.39259596294984705
- Win Rate(Against 1 Epoch Ultimate): 0.5031092665708581
- Win Rate(Against 1 Epoch Ultimate, calculated locally): 0.5071407243129562

1 Epoch Ultimate2 (of win rate prediction) 2021-2-13 20:10 CN Time
- Win Rate(Against More_Boar, calculated locally): 0.7159359601282804
- Win Rate(Against Optimal, calculated locally): 0.39259596294984705
- Win Rate(Against 1 Epoch Ultimate1): 0.5031092665708581
- Win Rate(Against 1 Epoch Ultimate1, calculated locally): 0.5071407243129562

