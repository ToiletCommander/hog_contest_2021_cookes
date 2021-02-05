import dice as diceLib
import final_strategy
import gamecalc
import baseline_strategy
import time

VIEW_STEP_BY_STEP = False

def test(strategy0, strategy1, score0 = 0, score1 = 0, goal = 100):
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    eight_sided_dice = diceLib.make_fair_dice(8)
    six_sided = diceLib.make_fair_dice(6)
    dice = six_sided

    # BEGIN PROBLEM 5
    while score0 < goal and score1 < goal:
        if who == 0:
            isPlayerPlaying = True
            turnNum = 0
            
            isPreviousTimeTrot = False
            isMoreBoar = False
            isTimeTrot = False
            
            while isPlayerPlaying and score0 < goal:
                print("--------------------------")
                print('score',score0,score1)
                print('player',0,'turn',turnNum)
                if VIEW_STEP_BY_STEP:
                    time.sleep(2)
                if(turnNum == 0):
                    dice = six_sided
                else:
                    dice = eight_sided_dice
                
                strategyThisRound = strategy0(score0,score1)
                scoreAdditionThisRound = gamecalc.take_turn(strategyThisRound,score1,dice,goal)
                score0 += scoreAdditionThisRound
                isMoreBoar = gamecalc.more_boar(score0,score1)
                isTimeTrot = gamecalc.time_trot(turnNum,strategyThisRound,isPreviousTimeTrot)
                isPlayerPlaying = isMoreBoar or isTimeTrot
                isPreviousTimeTrot = not(isMoreBoar) and isTimeTrot
                print("rolling", strategyThisRound, 'with a score increase of',scoreAdditionThisRound)
                if(isMoreBoar):
                    print("MoreBoar!")
                elif(isTimeTrot):
                    print("TimeTrot!")
                turnNum += 1
                
            who = 1
        else: #if who == 1
            isPlayerPlaying = True
            turnNum = 0
            
            isPreviousTimeTrot = False
            isMoreBoar = False
            isTimeTrot = False
            
            while isPlayerPlaying and score1 < goal:
                print("--------------------------")
                print('score',score0,score1)
                print('player',1,'turn',turnNum)
                if VIEW_STEP_BY_STEP:
                    time.sleep(2)
                if(turnNum == 0):
                    dice = six_sided
                else:
                    dice = eight_sided_dice
                strategyThisRound = strategy1(score1,score0)
                scoreAdditionThisRound = gamecalc.take_turn(strategyThisRound,score0,dice,goal)
                score1 += scoreAdditionThisRound
                isMoreBoar =  gamecalc.more_boar(score1,score0)
                isTimeTrot = gamecalc.time_trot(turnNum,strategyThisRound,isPreviousTimeTrot)
                isPlayerPlaying = isMoreBoar or isTimeTrot
                isPreviousTimeTrot = not(isMoreBoar) and isTimeTrot
                print("rolling", strategyThisRound, 'with a score increase of',scoreAdditionThisRound)
                if(isMoreBoar):
                    print("MoreBoar!")
                elif(isTimeTrot):
                    print("TimeTrot!")
                turnNum += 1
            who = 0
    
    # END PROBLEM 5
    # (note that the indentation for the problem 6 prompt (***YOUR CODE HERE***) might be misleading)
    # BEGIN PROBLEM 6
    "Finished in PROBLEM 5 parts"
    # END PROBLEM 6
    return score0, score1

testResults = []
numTest = 50
for i in range(numTest):
    print("testcase",i+1,'/',numTest)
    testResults.append(test(baseline_strategy.baseline_strategy,final_strategy.final_strategy,0,0,100))
print("finished")
print(testResults)
countWinNum = 0
for i in testResults:
    if i[1] >= 100:
        countWinNum+=1
print("winRate",countWinNum,'/',numTest)