import dice as diceLib
import gamecalc
import baseline_strategy
import time
import final_strategy_train
import random
import math

VIEW_STEP_BY_STEP = False

def test(strategy0, strategy1, score0 = 0, score1 = 0, goal = 100, startWho = 0, canPrint = True):
    final_strategy_train.resetFinalStrat()
    final_strategy_train.resetFinalStratHis()
    who = startWho #math.floor(random.random() * 2.0)  # Who is about to take a turn, 0 (first) or 1 (second)
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

def calculateWinRateOfStrat0(strategy0, strategy1, score0 = 0, score1 = 0, goal = 100, currentWho = 0, canCacheStrat0 = True, canCacheStrat1 = True, currentTurn = 0, previousTrot = False, rLevel = 0, Flipped = False):
    if score1 >= goal:
        return 0.0
        final_strategy_train.resetFinalStrat()
        final_strategy_train.resetFinalStratHis()
    elif score0 >= goal:
        return 1.0
        final_strategy_train.resetFinalStrat()
        final_strategy_train.resetFinalStratHis()
    
    if rLevel == 0:
        final_strategy_train.resetFinalStrat()
        final_strategy_train.resetFinalStratHis()
    
    if currentWho == 1:
        return 1.0 - calculateWinRateOfStrat0(strategy1, strategy0, score1, score0, goal, 0, currentTurn, previousTrot, rLevel, not(Flipped))
    if rLevel == 0:
        calculateWinRateOfStrat0.result_dict = {}

    who = currentWho #math.floor(random.random() * 2.0)  # Who is about to take a turn, 0 (first) or 1 (second)
    diceSide = 6

    

    saveKey = (score0,score1,currentTurn,previousTrot)
    if(Flipped):
        saveKey = (score1,score0,currentTurn,previousTrot)
    
    if saveKey in calculateWinRateOfStrat0.result_dict.keys():
        if not(Flipped):
            return calculateWinRateOfStrat0.result_dict[saveKey]
        else:
            return 1.0 - calculateWinRateOfStrat0.result_dict[saveKey]
    

    turnNum = currentTurn
    
    isMoreBoar = False
    isTimeTrot = False

    if(turnNum == 0):
        diceSide = 6
    else:
        diceSide = 8
    
    numToRollThisRound = strategy0(score0,score1)

    allPossibleScoreIncreases = final_strategy_train.predictScoreIncreasePossibilities(numToRollThisRound,score1,diceSide)
    totalPossibility = 0.0

    counter = 1
    totalNumItems = len(allPossibleScoreIncreases)
    for cScoreAddition, cPossibility in allPossibleScoreIncreases.items():
        newScore0 = score0 + cScoreAddition
        isMoreBoar = gamecalc.more_boar(newScore0,score1)
        isTimeTrot = gamecalc.time_trot(turnNum,numToRollThisRound,previousTrot)
        
        isPlayerPlaying = isMoreBoar or isTimeTrot
        if isPlayerPlaying:
            totalPossibility += cPossibility * calculateWinRateOfStrat0(strategy0,strategy1,newScore0,score1,goal,0,turnNum+1,isTimeTrot,rLevel+1,Flipped)
        else:
            totalPossibility += cPossibility * (1.0 - calculateWinRateOfStrat0(strategy1,strategy0,score1,newScore0,goal,0,0,False,rLevel+1,not(Flipped)))
        counter += 1
    assert(totalPossibility < 1.001 and totalPossibility > -0.001)

    totalPossibility = max(min(totalPossibility,1.0),0.0)

    if rLevel != 0: #and not(saveKey in calculateWinRateOfStrat0.result_dict.keys()):
        valToSave = totalPossibility if not(Flipped) else 1.0 - totalPossibility
        if (Flipped and canCacheStrat1) or (not(Flipped) and canCacheStrat0):
            calculateWinRateOfStrat0.result_dict[saveKey] = valToSave

    return totalPossibility

calculateWinRateOfStrat0.result_dict = {}

def tests(baseStrategy, strategy, size, canPrint = True, resultPrint = True):
    if resultPrint:
        print("testing",strategy.__name__,"against",baseStrategy.__name__,"with",size,"iterations of game")

    testResults = []
    for i in range(size):
        if canPrint:
            print("testcase",i+1,'/',size)
        testResults.append(test(baseStrategy,strategy,0,0,100,i%2,canPrint))
    countWinNum = 0
    for i in testResults:
        if i[1] >= 100:
            countWinNum+=1
    if resultPrint:
        print("winRate of", strategy.__name__, "winning", baseStrategy.__name__, countWinNum,'/',size, '=', (countWinNum / size))
    return countWinNum / size

def predicts(baseStrategy, strategy, resultPrint = True):
    if resultPrint:
        print("predicting win rate of",strategy.__name__,"against",baseStrategy.__name__)

    predictResult0 = calculateWinRateOfStrat0(strategy,baseStrategy,0,0,100,0)
    predictResult1 = calculateWinRateOfStrat0(strategy,baseStrategy,0,0,100,1)
    predictResult = (predictResult0 + predictResult1) / 2.0
    if resultPrint:
        print("winRate of", strategy.__name__, "winning", baseStrategy.__name__, predictResult0, "if",strategy.__name__,"were to play first")
        print("winRate of", strategy.__name__, "winning", baseStrategy.__name__, predictResult1, "if",baseStrategy.__name__,"were to play first")
        print("winRate of", strategy.__name__, "winning", baseStrategy.__name__, predictResult)