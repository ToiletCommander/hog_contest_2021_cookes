import dice as diceLib
import gamecalc
import baseline_strategy
import time
import final_strategy_train
import random
import math

VIEW_STEP_BY_STEP = False

def test(strategy0, strategy1, score0 = 0, score1 = 0, goal = 100, startWho = 0, canPrint = True):
    who = startWho #math.floor(random.random() * 2.0)  # Who is about to take a turn, 0 (first) or 1 (second)
    eight_sided_dice = diceLib.make_fair_dice(8)
    six_sided = diceLib.make_fair_dice(6)
    dice = six_sided

    overallTurnNum = 0

    # BEGIN PROBLEM 5
    while score0 < goal and score1 < goal:
        if who == 0:
            isPlayerPlaying = True
            turnNum = 0
            
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
                
                if strategy0 == final_strategy_train.final_strategy and not(final_strategy_train.final_strategy.producing_actual_result):
                        final_strategy_train.feedHitData(turnNum,overallTurnNum,score0,score1,1.0)

                final_strategy_train.MATCH_CURRENT_TURN_NUM = turnNum
                final_strategy_train.MATCH_LAST_EXTRA = turnNum>=1
                final_strategy_train.MATCH_OVERALL_TURN_NUM = overallTurnNum
                
                strategyThisRound = strategy0(score0,score1)
                scoreAdditionThisRound = gamecalc.take_turn(strategyThisRound,score1,dice,goal)
                score0 += scoreAdditionThisRound
                isMoreBoar = gamecalc.more_boar(score0,score1)
                isTimeTrot = gamecalc.time_trot(overallTurnNum,strategyThisRound,turnNum>=1)
                isPlayerPlaying = isMoreBoar or isTimeTrot

                if canPrint:
                    print("rolling", strategyThisRound, 'with a score increase of',scoreAdditionThisRound)
                    if(isMoreBoar):
                        print("MoreBoar!")
                    elif(isTimeTrot):
                        print("TimeTrot!")
                turnNum += 1
                overallTurnNum += 1
                
            who = 1
        else: #if who == 1
            isPlayerPlaying = True
            turnNum = 0

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

                if strategy1 == final_strategy_train.final_strategy and not(final_strategy_train.final_strategy.producing_actual_result):
                        final_strategy_train.feedHitData(turnNum,overallTurnNum,score1,score0,1.0)

                final_strategy_train.MATCH_CURRENT_TURN_NUM = turnNum
                final_strategy_train.MATCH_LAST_EXTRA = turnNum >= 1
                final_strategy_train.MATCH_OVERALL_TURN_NUM = overallTurnNum

                strategyThisRound = strategy1(score1,score0)
                scoreAdditionThisRound = gamecalc.take_turn(strategyThisRound,score0,dice,goal)
                score1 += scoreAdditionThisRound
                isMoreBoar =  gamecalc.more_boar(score1,score0)
                isTimeTrot = gamecalc.time_trot(overallTurnNum,strategyThisRound,turnNum >= 1)
                isPlayerPlaying = isMoreBoar or isTimeTrot

                if canPrint:
                    print("rolling", strategyThisRound, 'with a score increase of',scoreAdditionThisRound)
                    if(isMoreBoar):
                        print("MoreBoar!")
                    elif(isTimeTrot):
                        print("TimeTrot!")
                turnNum += 1
                overallTurnNum += 1
            who = 0
    
    # END PROBLEM 5
    # (note that the indentation for the problem 6 prompt (***YOUR CODE HERE***) might be misleading)
    # BEGIN PROBLEM 6
    "Finished in PROBLEM 5 parts"
    # END PROBLEM 6
    return score0, score1

def calculateWinRateOfStrat0(strategy0, strategy1, score0 = 0, score1 = 0, goal = 100, currentWho = 0, canCacheStrat0 = True, canCacheStrat1 = True, currentTurn = 0, overallTurn = 0, rLevel = 0, Flipped = False, chance = 1.0):
    if score1 >= goal:
        return 0.0
    elif score0 >= goal:
        return 1.0
    
    
    if currentWho == 1:
        return 1.0 - calculateWinRateOfStrat0(strategy1, strategy0, score1, score0, goal, 0, canCacheStrat1, canCacheStrat0, currentTurn, overallTurn, rLevel, not(Flipped), chance)
    if rLevel == 0:
        calculateWinRateOfStrat0.result_dict = {}

    saveKey = (Flipped, score0, score1, currentTurn >= 1,overallTurn % 8)
    
    if saveKey in calculateWinRateOfStrat0.result_dict.keys() and canCacheStrat0:
        savedPair = calculateWinRateOfStrat0.result_dict[saveKey]
        if strategy0 == final_strategy_train.final_strategy and not(final_strategy_train.final_strategy.producing_actual_result):
            hitCacheData = savedPair[1]
            final_strategy_train.applyHitCacheData(hitCacheData)
        return savedPair[0]

    diceSide = 6
    
    isMoreBoar = False
    isTimeTrot = False

    if(currentTurn == 0):
        diceSide = 6
    else:
        diceSide = 8
    

    if strategy0 == final_strategy_train.final_strategy and not(final_strategy_train.final_strategy.producing_actual_result) and canCacheStrat0:
        final_strategy_train.startHitDataCache()
        final_strategy_train.feedHitData(currentTurn,overallTurn,score0,score1,chance)
        

    final_strategy_train.MATCH_CURRENT_TURN_NUM = currentTurn
    final_strategy_train.MATCH_LAST_EXTRA = currentTurn >= 1
    final_strategy_train.MATCH_OVERALL_TURN_NUM = overallTurn

    numToRollThisRound = strategy0(score0,score1)

    allPossibleScoreIncreases = final_strategy_train.predictScoreIncreasePossibilities(numToRollThisRound,score1,diceSide)
    totalPossibility = 0.0

    isTimeTrot = gamecalc.time_trot(overallTurn,numToRollThisRound,currentTurn >= 1)
    for cScoreAddition, cPossibility in allPossibleScoreIncreases.items():
        newScore0 = score0 + cScoreAddition
        isMoreBoar = gamecalc.more_boar(newScore0,score1)
        
        currentIterationTotalPossibility = chance * cPossibility

        isPlayerPlaying = isMoreBoar or isTimeTrot
        if isPlayerPlaying:
            totalPossibility += cPossibility * calculateWinRateOfStrat0(strategy0,strategy1,newScore0,score1,goal,0,canCacheStrat0,canCacheStrat1,currentTurn+1,overallTurn+1,rLevel+1,Flipped,currentIterationTotalPossibility)
        else:
            totalPossibility += cPossibility * (1.0 - calculateWinRateOfStrat0(strategy1,strategy0,score1,newScore0,goal,0,canCacheStrat1,canCacheStrat0,0,overallTurn+1,rLevel+1,not(Flipped),currentIterationTotalPossibility))

    totalPossibility = max(min(totalPossibility,1.0),0.0)

    if rLevel != 0: #and not(saveKey in calculateWinRateOfStrat0.result_dict.keys()):
        if (canCacheStrat0):
            resultPair = None
            if strategy0 == final_strategy_train.final_strategy and not(final_strategy_train.final_strategy.producing_actual_result):
                resultPair = (totalPossibility,final_strategy_train.endHitDataCache())
            else:
                resultPair = (totalPossibility,)
            calculateWinRateOfStrat0.result_dict[saveKey] = resultPair

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

def predicts(baseStrategy, strategy, cache = True, resultPrint = True):
    if resultPrint:
        print("predicting win rate of",strategy.__name__,"against",baseStrategy.__name__)

    predictResult0 = calculateWinRateOfStrat0(strategy,baseStrategy,0,0,100,0,cache,cache)
    predictResult1 = calculateWinRateOfStrat0(strategy,baseStrategy,0,0,100,1,cache,cache)
    predictResult = (predictResult0 + predictResult1) / 2.0
    if resultPrint:
        print("winRate of", strategy.__name__, "winning", baseStrategy.__name__, predictResult0, "if",strategy.__name__,"were to play first")
        print("winRate of", strategy.__name__, "winning", baseStrategy.__name__, predictResult1, "if",baseStrategy.__name__,"were to play first")
        print("winRate of", strategy.__name__, "winning", baseStrategy.__name__, predictResult)