import dice as diceLib
import gamecalc
import baseline_strategy
import time
import final_strategy
import random
import math

VIEW_STEP_BY_STEP = False

def test(strategy0, strategy1, score0 = 0, score1 = 0, goal = 100, canPrint = True):
    final_strategy.resetFinalStrat()
    final_strategy.resetFinalStratHis()
    who = math.floor(random.random() * 2.0)  # Who is about to take a turn, 0 (first) or 1 (second)
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
                if canPrint:
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
                isPreviousTimeTrot = isTimeTrot
                if canPrint:
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
                if canPrint:
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
                isPreviousTimeTrot = isTimeTrot
                if canPrint:
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

def tests(baseStrategy, strategy, size, canPrint = True, resultPrint = True):
    if resultPrint:
        print("testing",baseStrategy.__name__,"against",strategy.__name__,"with",size,"iterations of game")

    testResults = []
    for i in range(size):
        if canPrint:
            print("testcase",i+1,'/',size)
        testResults.append(test(baseStrategy,strategy,0,0,100,canPrint))
    countWinNum = 0
    for i in testResults:
        if i[1] >= 100:
            countWinNum+=1
    if resultPrint:
        print("winRate of", strategy.__name__, "winning", baseStrategy.__name__, countWinNum,'/',size)
    return countWinNum / size