"""
    This file contains your final_strategy that will be submitted to the contest.
    It will only be run on your local machine, so you can import whatever you want!
    Remember to supply a unique PLAYER_NAME or your submission will not succeed.
"""
import gamecalc
import dice as diceLib

DEBUG_ON = False
EXCESS_DEBUG = False
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
        appendReadKeys = appendResults.keys()
        appendKeys = []
        for i in appendReadKeys:
            appendKeys.append(i)
        
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
                if key in appendKeys:
                    appendResults[key] += currentValue
                    appendKeys.append(key)
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

def getWinningChance(currentPlayerLastTimeTrot, opponentLastTimeTrot, numToRoll, selfScore, opponentScore, targetScore, turnNum = 0, currentPlayer = 0, currentLevel = 0):
    def getWinningChanceForSpecificScoreIncrease(lastTimeTrot,newScore):
        if(newScore >= targetScore):
            return 1.0

        moreBoar = gamecalc.more_boar(newScore,opponentScore)
        timeTrot = gamecalc.time_trot(turnNum,numToRoll,lastTimeTrot)
        moreTurn = moreBoar or timeTrot

        biggestChance = 0.0
        biggestChanceThrow = 0

        numChance = 10
        chance = 0
        
        if moreTurn:
            biggestChance = 0
            for i in range(0,numChance+1):
                currentChance = getWinningChance(timeTrot,opponentLastTimeTrot,i,newScore,opponentScore,targetScore,turnNum+1,0,currentLevel+1)
                if(currentChance > biggestChance):
                    biggestChance = currentChance
                    biggestChanceThrow = i
            chance = biggestChance
        else:
            biggestChance = 1.0
            for i in range(0,numChance+1):
                currentChance = 1.0 - getWinningChance(opponentLastTimeTrot,timeTrot,i,opponentScore,newScore,targetScore,0,0,currentLevel+1)
                if(currentChance < biggestChance):
                    biggestChance = currentChance
                    biggestChanceThrow = i
        return biggestChance

    def winningChanceForDicePossibility():
        diceSideNum = 6 if turnNum == 0 else 8
        
        scoreIncrease = 0

        if numToRoll == 0:
            scoreIncrease = gamecalc.piggy_points(opponentScore)
            newScore = selfScore+scoreIncrease
            specificWinningChance = getWinningChanceForSpecificScoreIncrease(currentPlayerLastTimeTrot,newScore)
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
                specificWinningChance = getWinningChanceForSpecificScoreIncrease(currentPlayerLastTimeTrot,newScore)
                chanceSum += calculateDicePossibility(numToRoll,diceSideNum,scoreIncrease) * specificWinningChance
            return chanceSum

    if not(currentPlayer == 0):
        returnVal = 1.0 - getWinningChance(opponentLastTimeTrot,currentPlayerLastTimeTrot,numToRoll,opponentScore,selfScore,targetScore,turnNum,0,currentLevel)
        if DEBUG_ON:
            print('wc(',selfScore,opponentScore,numToRoll,') = ',returnVal)
        return returnVal

    if DEBUG_ON and (currentLevel == 0 or EXCESS_DEBUG):
        print("calculating winning chance for " + str(numToRoll) + " rolls when score is (" + str(selfScore) + "," + str(opponentScore) + "), and turn=" + str(turnNum))
    

    saveKey = (currentPlayerLastTimeTrot,numToRoll,selfScore,opponentScore,targetScore,turnNum)
    if saveKey in getWinningChance.result_dict.keys():
        returnVal = getWinningChance.result_dict[saveKey]
        if DEBUG_ON and (currentLevel == 0 or EXCESS_DEBUG):
            print('wc(',selfScore,opponentScore,numToRoll,') = ',returnVal)
        return returnVal
    
    returnVal = winningChanceForDicePossibility()
    if DEBUG_ON and (currentLevel == 0 or EXCESS_DEBUG):
        print('wc(',selfScore,opponentScore,numToRoll,') = ',returnVal)
        print('cached',len(getWinningChance.result_dict))
    if not(saveKey in getWinningChance.result_dict.keys()):
        getWinningChance.result_dict[saveKey] = returnVal
    return returnVal

getWinningChance.result_dict = {}

def strategy_to_play(turnNum, dice_side_num, selfScore, opponentScore, canTimeTrot):
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
        currentWinningRate = getWinningChance(not(canTimeTrot),False,i,selfScore,opponentScore,targetScore,turnNum,0)
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
        #we should see whether last time really used the "time trot strategy because it might have triggered a more boar"
        if gamecalc.more_boar(score,opponent_score):
            canTrot = True
        diceSideNum = 8

    #determine strategy to play
    strategyReturn = strategy_to_play(turnNumber,diceSideNum,score,opponent_score,canTrot)
    
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