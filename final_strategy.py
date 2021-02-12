"""
    This file contains your final_strategy that will be submitted to the contest.
    It will only be run on your local machine, so you can import whatever you want!
    Remember to supply a unique PLAYER_NAME or your submission will not succeed.
"""
import gamecalc
import dice as diceLib
import test
from baseline_strategy import baseline_strategy, random_strategy
import time
import pickle
from os import path
import submissions

DEBUG_ON = False
EXCESS_DEBUG = False
SUBMIT = submissions.IS_SUBMIT
TRAIN_STRATEGY_NAME = submissions.STRATEGY_NAME
PLAYER_NAME = 'CookEs'  # Change this line!

def getDiceResults(numRoll, diceSide, previousSum = 0, isOne = False):
    sumItems = 0
    saveKey = (numRoll, diceSide)
    appendResults = {}

    if not(isOne) and saveKey in getDiceResults.dice_results.keys():
        
        if DEBUG_ON and EXCESS_DEBUG:
            print("fetching saved results where numRoll =", numRoll, 'and diceSide =', diceSide, 'and previousSum =', previousSum)
        savedResults = getDiceResults.dice_results[saveKey]
        
        savedTotalItem = savedResults[0]
        deltaPreviousSum = previousSum
        
        dataSize = savedTotalItem

        savedItems = savedResults[1].items()

        if deltaPreviousSum != 0:
            for (key, value) in savedItems:
                if key == 1:
                    appendResults[key] = value
                else:
                    appendResults[key+deltaPreviousSum] = value
            return (savedResults[0],appendResults)
        else:
            return savedResults

    if isOne:
        numToAdd = 0
        if numRoll == 0:
            numToAdd = 1
        else:
            numToAdd = diceSide ** numRoll
        appendResults[1] = numToAdd
        return (numToAdd,appendResults)

    if DEBUG_ON and EXCESS_DEBUG:
        print("calculating results where numRoll =", numRoll, 'and diceSide =', diceSide, 'and previousSum =', previousSum)

    if numRoll >= 1:
        for i in range(1,diceSide+1):
            if DEBUG_ON and EXCESS_DEBUG:
                print("iterating " + str(i) + "/" + str(diceSide))
            previousSum += i
            newResultsToAdd = {}
            if i == 1:
                newResultsToAdd = getDiceResults(numRoll-1,diceSide,previousSum,True)
            else:
                newResultsToAdd = getDiceResults(numRoll-1,diceSide,previousSum,isOne)
            
            newItems = newResultsToAdd[1].items()
            
            for (key,currentValue) in newItems:
                if key in appendResults.keys():
                    appendResults[key] = appendResults[key] + currentValue
                else:
                    appendResults[key] = currentValue
            sumItems += newResultsToAdd[0]
            previousSum -= i
        
    else: #!isOne and numRoll == 0
        appendResults[previousSum] = 1
        sumItems = 1
    
    if not(saveKey in getDiceResults.dice_results.keys()) and numRoll >= 1:
        saveResults = {}
        if previousSum != 0:
            for (key, currentElement) in appendResults.items():
                currentElement = appendResults[key]
                if(currentElement != 1):
                    saveResults[key-previousSum] = currentElement
                else:
                    saveResults[1] = currentElement
        else:
            saveResults = appendResults
        getDiceResults.dice_results[saveKey] = (sumItems, saveResults)
    
    return (sumItems,appendResults)

getDiceResults.dice_results = {}

def calculateDicePossibility(numRoll,diceSide,targetNum):
    possibilitySig = (numRoll, diceSide, targetNum)

    if possibilitySig in calculateDicePossibility.possibilities:
        return calculateDicePossibility.possibilities[possibilitySig]

    calculatedResults = getDiceResults(numRoll,diceSide)
    returnVal = 0
    if(targetNum in calculatedResults[1]):
        returnVal = calculatedResults[1][targetNum] / calculatedResults[0]
    else:
        returnVal = 0
    
    calculateDicePossibility.possibilities[possibilitySig] = returnVal
    return returnVal

calculateDicePossibility.possibilities = {}

def getWinningChance(currentPlayerLastTimeTrot, opponentLastTimeTrot, numToRoll, selfScore, opponentScore, targetScore, turnNum = 0, currentPlayer = 0, currentLevel = 0, CALCULATING_HIT = False, USE_HIT = False):
    def getWinningChanceForSpecificScoreIncrease(nScore, tNum, cpLastTimeTrot):
        if(nScore >= targetScore):
            return 1.0

        moreBoar = gamecalc.more_boar(nScore,opponentScore)
        timeTrot = gamecalc.time_trot(tNum,numToRoll,cpLastTimeTrot)
        moreTurn = moreBoar or timeTrot

        biggestChance = 0.0
        biggestChanceThrow = 0

        numChance = 10
        chance = 0
        
        if moreTurn:
            biggestChance = 0
            for i in range(0,numChance+1):
                currentChance = getWinningChance(timeTrot,opponentLastTimeTrot,i,nScore,opponentScore,targetScore,tNum+1,0,currentLevel+1,False,False)
                if(currentChance > biggestChance):
                    biggestChance = currentChance
                    biggestChanceThrow = i
            chance = biggestChance
        else:
            biggestChance = 0
            for i in range(0,numChance+1):
                currentChance = getWinningChance(opponentLastTimeTrot,timeTrot,i,opponentScore,nScore,targetScore,0,0,currentLevel+1,False,False)
                if(currentChance > biggestChance):
                    biggestChance = currentChance
                    biggestChanceThrow = i
            biggestChance = 1.0 - biggestChance
        return biggestChance

    def winningChanceForDicePossibility(tNum, cpLastTimeTrot):
        diceSideNum = 6 if tNum == 0 else 8
        
        scoreIncrease = 0

        if numToRoll == 0:
            scoreIncrease = gamecalc.piggy_points(opponentScore)
            newScore = selfScore+scoreIncrease
            specificWinningChance = getWinningChanceForSpecificScoreIncrease(newScore,tNum,cpLastTimeTrot)
            chance = specificWinningChance
            return chance

        elif numToRoll >= 1:
            diceSmallest = 2
            diceBiggest = diceSideNum

            scoreSmallest = diceSmallest * numToRoll
            scoreBiggest = diceBiggest * numToRoll
            chanceSum = 0.0

            valueToIterate = []
            valueToIterate.append(1)
            for i in range(scoreSmallest,scoreBiggest+1):
                valueToIterate.append(i)
            
            for i in valueToIterate:
                scoreIncrease = i
                newScore = selfScore+scoreIncrease
                specificWinningChance = getWinningChanceForSpecificScoreIncrease(newScore,tNum,cpLastTimeTrot)
                chanceSum += calculateDicePossibility(numToRoll,diceSideNum,scoreIncrease) * specificWinningChance
            return chanceSum

    if not(currentPlayer == 0):
        returnVal = 1.0 - getWinningChance(opponentLastTimeTrot,currentPlayerLastTimeTrot,numToRoll,opponentScore,selfScore,targetScore,turnNum,0,currentLevel)
        if DEBUG_ON:
            print('wc(',selfScore,opponentScore,numToRoll,') = ',returnVal)
        return returnVal

    if DEBUG_ON and (currentLevel == 0 or EXCESS_DEBUG):
        print("calculating winning chance for " + str(numToRoll) + " rolls when score is (" + str(selfScore) + "," + str(opponentScore) + "), and turn=" + str(turnNum))
    
    hitKey = (selfScore, opponentScore)

    if CALCULATING_HIT and not(USE_HIT) and currentLevel == 0:
        trotHitNum = 1 if not(currentPlayerLastTimeTrot) else 0
        if not(hitKey in getWinningChance.turn_hit_dict.keys()):
            getWinningChance.turn_hit_dict[hitKey] = {-1:0} #-1 means total
        if not(turnNum in getWinningChance.turn_hit_dict[hitKey].keys()):
            getWinningChance.turn_hit_dict[hitKey][turnNum] = [1,trotHitNum]
            getWinningChance.turn_hit_dict[hitKey][-1] += 1
        else:
            getWinningChance.turn_hit_dict[hitKey][turnNum][0] += 1
            getWinningChance.turn_hit_dict[hitKey][turnNum][1] += trotHitNum
            getWinningChance.turn_hit_dict[hitKey][-1] += 1
    
    returnVal = 0

    saveKey = (False,numToRoll,selfScore,opponentScore,targetScore,USE_HIT)
    if not(USE_HIT):
        thisTimeItCanTrot = gamecalc.time_trot(turnNum,numToRoll,currentPlayerLastTimeTrot)
        
        saveKey = (thisTimeItCanTrot,numToRoll,selfScore,opponentScore,targetScore)
        
        if saveKey in getWinningChance.result_dict.keys():
            returnVal = getWinningChance.result_dict[saveKey]
            if DEBUG_ON and (currentLevel == 0 or EXCESS_DEBUG):
                print('wc(',selfScore,opponentScore,numToRoll,') = ',returnVal)
            return returnVal
        returnVal = winningChanceForDicePossibility(turnNum,currentPlayerLastTimeTrot)
        
    else:
        saveKey = (numToRoll,selfScore,opponentScore,targetScore)
        if saveKey in getWinningChance.hit_result_dict.keys():
            returnVal = getWinningChance.hit_result_dict[saveKey]
            if DEBUG_ON and (currentLevel == 0 or EXCESS_DEBUG):
                print('wc_hit(',selfScore,opponentScore,numToRoll,') = ',returnVal)
            return returnVal
        hitKey = (selfScore,opponentScore)
        possibilityDict = getWinningChance.turn_hit_dict[hitKey] if hitKey in getWinningChance.turn_hit_dict.keys() else {0:(1,0),-1:1}
        total = possibilityDict[-1]
        for cKey, cVal in possibilityDict.items():
            if cKey == -1:
                continue
            currentTurnNum = cKey
            currentTurnOccurence = cVal[0] / total
            currentCanTrotOccurence = cVal[1] / cVal[0]
            returnVal += currentTurnOccurence * (currentCanTrotOccurence * winningChanceForDicePossibility(currentTurnNum,False) + (1-currentCanTrotOccurence) * winningChanceForDicePossibility(currentTurnNum,True))

    
    if DEBUG_ON and not(USE_HIT) and (currentLevel == 0 or EXCESS_DEBUG):
        print('wc(',selfScore,opponentScore,numToRoll,') = ',returnVal)
    elif DEBUG_ON and USE_HIT and (currentLevel == 0 or EXCESS_DEBUG):
        print('wc_hit(',selfScore,opponentScore,numToRoll,') = ',returnVal)
    if not(USE_HIT) and not(saveKey in getWinningChance.result_dict.keys()):
        getWinningChance.result_dict[saveKey] = returnVal
    elif USE_HIT and not(saveKey in getWinningChance.hit_result_dict.keys()):
        getWinningChance.hit_result_dict[saveKey] = returnVal
    return returnVal

getWinningChance.result_dict = {}
getWinningChance.hit_result_dict = {}
getWinningChance.turn_hit_dict = {}

def saveDictionary(filename,dictionary):
    file = open(filename,"wb")
    pickle.dump(dictionary,file)
    file.close()

def loadDictionary(filename):
    file = open(filename,"rb")
    temp = pickle.load(file)
    file.close()
    return temp

def saveWinningChanceWithHistoryResults(filename):
    saveDictionary("savedData/" + filename,getWinningChance.result_dict)

def readWinningChanceWithHistoryResults(filename):
    if path.exists("savedData/" + filename):
        getWinningChance.result_dict = loadDictionary("savedData/" + filename)

def saveWinningHitResults(filename):
    saveDictionary("savedData/" + filename,getWinningChance.turn_hit_dict)

def readWinnningHitResults(filename):
    if path.exists("savedData/" + filename):
        getWinningChance.turn_hit_dict = loadDictionary("savedData/" + filename)

def make_winning_chance(score0,score1):
	def func(numToRoll):
		return getWinningChance(False,False,numToRoll,score0,score1,100,0,0,0)
	return func

def strategy_to_play(turnNum, dice_side_num, selfScore, opponentScore, canTimeTrot, CALC_HIT, USE_HIT):
    """This is the function to implement final strategy, it gives you all possible informations about the current turn
    turnNum = number of consecutive turn the player is playing, starting from 0
    canTimeTrot = if the player can use the time trot strategy in this turn

    returns numToRoll
    """
    winningChances = []
    biggestWinningRate = 0
    biggestWinningIndex = 0

    targetScore = 100

    """
    while (selfScore > targetScore or opponentScore > targetScore):
        targetScore *= 2
    """

    for i in range(0,11):
        currentWinningRate = getWinningChance(not(canTimeTrot),False,i,selfScore,opponentScore,targetScore,turnNum,0,0,CALC_HIT,USE_HIT)
        winningChances.append(currentWinningRate)
        if(currentWinningRate > biggestWinningRate):
            biggestWinningRate = currentWinningRate
            biggestWinningIndex = i
    return biggestWinningIndex
    



def piggypoints_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy rolls 0 dice if that gives at least CUTOFF points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    if(gamecalc.piggy_points(opponent_score) >= cutoff):
        return 0
    else:
        return num_rolls

def more_boar_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy rolls 0 dice when it triggers an extra turn. It also
    rolls 0 dice if it gives at least CUTOFF points and does not give an extra turn.
    Otherwise, it rolls NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    if gamecalc.more_boar(score + gamecalc.piggy_points(opponent_score),opponent_score):
        return 0
    else:
        return piggypoints_strategy(score,opponent_score,cutoff,num_rolls)
    # END PROBLEM 11

def final_strategy(score, opponent_score):
    turnNumber = 0
    canTrot = False
    diceSideNum = 6

    #determine if this is the first turn or not
    if(final_strategy.last_opponent_score < opponent_score):
        turnNumber = 0
        diceSideNum = 6
        canTrot = True
    else:
        turnNumber = final_strategy.last_turn_num + 1
        canTrot = not(final_strategy.last_time_trot)
        diceSideNum = 8

    #determine strategy to play
    strategyReturn = strategy_to_play(turnNumber,diceSideNum,score,opponent_score,canTrot,not(final_strategy.producing_actual_result),final_strategy.producing_actual_result)
    
    #decode strategyReturn
    numToRollDice = strategyReturn
    isTimeTrot = gamecalc.time_trot(turnNumber,numToRollDice,not(canTrot))

    #update state variables
    final_strategy.last_opponent_score = opponent_score
    final_strategy.last_turn_num = turnNumber
    final_strategy.last_self_score = score
    final_strategy.last_time_trot = isTimeTrot

    return numToRollDice

#In the global frame we want to initialize 
final_strategy.last_opponent_score = -1
final_strategy.last_turn_num = 0
final_strategy.last_self_score = 0
final_strategy.last_time_trot = False
final_strategy.producing_actual_result = False

def resetFinalStrat():
    final_strategy.last_opponent_score = -1
    final_strategy.last_turn_num = 0
    final_strategy.last_self_score = 0
    final_strategy.last_time_trot = False

def final_strategy_hist(score, opponent_score):
    turnNumber = 0
    canTrot = False
    diceSideNum = 6

    #determine if this is the first turn or not
    if(final_strategy_hist.last_opponent_score < opponent_score):
        turnNumber = 0
        diceSideNum = 6
        canTrot = True
    else:
        turnNumber = final_strategy_hist.last_turn_num + 1
        canTrot = not(final_strategy_hist.last_time_trot)
        diceSideNum = 8

    #determine strategy to play
    strategyReturn = strategy_to_play(turnNumber,diceSideNum,score,opponent_score,canTrot,True,False)
    
    #decode strategyReturn
    numToRollDice = strategyReturn
    isTimeTrot = gamecalc.time_trot(turnNumber,numToRollDice,not(canTrot))

    #update state variables
    final_strategy_hist.last_opponent_score = opponent_score
    final_strategy_hist.last_turn_num = turnNumber
    final_strategy_hist.last_self_score = score
    final_strategy_hist.last_time_trot = isTimeTrot

    return numToRollDice

#In the global frame we want to initialize 
final_strategy_hist.last_opponent_score = -1
final_strategy_hist.last_turn_num = 0
final_strategy_hist.last_self_score = 0
final_strategy_hist.last_time_trot = False

def resetFinalStratHis():
    final_strategy_hist.last_opponent_score = -1
    final_strategy_hist.last_turn_num = 0
    final_strategy_hist.last_self_score = 0
    final_strategy_hist.last_time_trot = False

if SUBMIT:
    startTime = time.time()

    withHistWinningChanceFileName = TRAIN_STRATEGY_NAME + "_historyChance.pkl"
    hitRateFileName = TRAIN_STRATEGY_NAME + "_hitRate.pkl"

    readWinningChanceWithHistoryResults(withHistWinningChanceFileName)
    readWinnningHitResults(hitRateFileName)

    readFinishTime = time.time()

    if DEBUG_ON:
        print("it took",(readFinishTime - startTime),"to read from pre-trained data")
