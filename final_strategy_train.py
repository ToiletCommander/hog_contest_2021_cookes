"""
    This file contains your final_strategy that will be submitted to the contest.
    It will only be run on your local machine, so you can import whatever you want!
    Remember to supply a unique PLAYER_NAME or your submission will not succeed.
"""
import gamecalc
import dice as diceLib
from baseline_strategy import baseline_strategy, random_strategy
import time
import pickle
from os import path
import submissions

DEBUG_ON = True
EXCESS_DEBUG = False
TRAIN_STRATEGY_NAME = submissions.STRATEGY_NAME
PLAYER_NAME = submissions.SUBMIT_NAME

MATCH_LAST_EXTRA = False
MATCH_CURRENT_TURN_NUM = 0
MATCH_OVERALL_TURN_NUM = 0

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
                if(key != 1):
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

def predictScoreIncreasePossibilities(num_rolls, opponent_score, diceSide = 6):
    if(num_rolls == 0):
        return {gamecalc.piggy_points(opponent_score):1.0}

    possibilitySig = (num_rolls,diceSide)
    if possibilitySig in predictScoreIncreasePossibilities.possibilities:
        return predictScoreIncreasePossibilities.possibilities[possibilitySig]
    
    diceResults = getDiceResults(num_rolls,diceSide)
    newDictionary = {}
    totalNum = diceResults[0]
    for cKey, cValue in diceResults[1].items():
        newDictionary[cKey] = cValue / totalNum
    return newDictionary

predictScoreIncreasePossibilities.possibilities = {}



def getWinningChance(currentPlayerLastTimeExtra, numToRoll, selfScore, opponentScore, targetScore, overallTurnNum = 0, currentLevel = 0, USE_HIT = False):
    def getWinningChanceForSpecificScoreIncrease(nScore, oTNum, cpLastTimeExtra):
        if(nScore >= targetScore):
            return 1.0

        moreBoar = gamecalc.more_boar(nScore,opponentScore)
        timeTrot = gamecalc.time_trot(oTNum,numToRoll,cpLastTimeExtra)
        moreTurn = (moreBoar or timeTrot)

        biggestChance = 0.0
        biggestChanceThrow = 0

        numChance = 10
        chance = 0
        
        if moreTurn:
            for i in range(0,numChance+1):
                currentChance = getWinningChance(True,i,nScore,opponentScore,targetScore,oTNum+1,currentLevel+1,False)
                if(currentChance > biggestChance):
                    biggestChance = currentChance
                    biggestChanceThrow = i
            chance = biggestChance
        else:
            for i in range(0,numChance+1):
                currentChance = getWinningChance(False,i,opponentScore,nScore,targetScore,oTNum+1,currentLevel+1,False)
                if(currentChance > biggestChance):
                    biggestChance = currentChance
                    biggestChanceThrow = i
            biggestChance = 1.0 - biggestChance
        return biggestChance

    def winningChanceForDicePossibility(oTNum, cpLastTimeExtra):
        diceSideNum = 6 if not(cpLastTimeExtra) else 8
        
        scoreIncreasePossibilities = predictScoreIncreasePossibilities(numToRoll,opponentScore,diceSideNum)
        
        chanceSum = 0
        for cScoreIncrease, cPossibility in scoreIncreasePossibilities.items():
            newScore = selfScore + cScoreIncrease
            specificWinningChance = getWinningChanceForSpecificScoreIncrease(newScore,oTNum,cpLastTimeExtra)
            chanceSum += cPossibility * specificWinningChance
        return max(min(chanceSum,1.0),0.0)
    
    returnVal = 0

    saveKey = (USE_HIT,numToRoll,selfScore,opponentScore,targetScore,overallTurnNum % 8)
    if not(USE_HIT):
        thisTimeItCanTrot = gamecalc.time_trot(overallTurnNum,numToRoll,currentPlayerLastTimeExtra)
        
        saveKey = (USE_HIT,thisTimeItCanTrot,numToRoll,selfScore,opponentScore,targetScore)
        
        if saveKey in getWinningChance.result_dict.keys():
            returnVal = getWinningChance.result_dict[saveKey]
            if DEBUG_ON and EXCESS_DEBUG:
                print('wc(',selfScore,opponentScore,numToRoll,') = ',returnVal)
            return returnVal
        
        returnVal = winningChanceForDicePossibility(overallTurnNum, currentPlayerLastTimeExtra)
        
    else:
        saveKey = (USE_HIT,numToRoll,selfScore,opponentScore,targetScore)
        if saveKey in getWinningChance.hit_result_dict.keys():
            returnVal = getWinningChance.hit_result_dict[saveKey]
            if DEBUG_ON and EXCESS_DEBUG:
                print('wc_hit(',selfScore,opponentScore,numToRoll,') = ',returnVal)
            return returnVal
        
        hitKey = (selfScore,opponentScore)
        possibilityDict = getWinningChance.turn_hit_dict[hitKey] if hitKey in getWinningChance.turn_hit_dict.keys() else {(0,0):1,-1:1}
        total = possibilityDict[-1]
        returnVal = 0
        for cKey, cVal in possibilityDict.items():
            if cKey == -1:
                continue
            currentIsTurnAtLeast1 = cKey[0]
            currentOverallTurnNum = cKey[1]
            currentTurnOccurence = cVal / total
            returnVal += currentTurnOccurence * winningChanceForDicePossibility(currentOverallTurnNum,currentIsTurnAtLeast1)
        returnVal = min(1.0,max(returnVal,0.0))
    
    if DEBUG_ON and not(USE_HIT) and EXCESS_DEBUG:
        print('wc(',selfScore,opponentScore,numToRoll,') = ',returnVal)
    elif DEBUG_ON and USE_HIT and EXCESS_DEBUG:
        print('wc_hit(',selfScore,opponentScore,numToRoll,') = ',returnVal)
    if not(USE_HIT) and not(saveKey in getWinningChance.result_dict.keys()):
        getWinningChance.result_dict[saveKey] = returnVal
    elif USE_HIT and not(saveKey in getWinningChance.hit_result_dict.keys()):
        getWinningChance.hit_result_dict[saveKey] = returnVal
    return returnVal

getWinningChance.result_dict = {}
getWinningChance.hit_result_dict = {}
getWinningChance.turn_hit_dict = {}

def isHitKey(selfScore, opponentScore):
    hitKey = (selfScore, opponentScore)
    return hitKey in getWinningChance.turn_hit_dict.keys()

def feedHitData(cache, turnNum, overallTurnNum, selfScore, opponentScore, occurencePossibility = 1.0):
    hitKey = (selfScore, opponentScore)
    saveKey = (turnNum >= 1, overallTurnNum % 8)

    if not(cache):
        if not(hitKey in getWinningChance.turn_hit_dict.keys()):
            getWinningChance.turn_hit_dict[hitKey] = {-1:0.0} #-1 means total
        if not(saveKey in getWinningChance.turn_hit_dict[hitKey].keys()):
            getWinningChance.turn_hit_dict[hitKey][saveKey] = occurencePossibility
            getWinningChance.turn_hit_dict[hitKey][-1] += occurencePossibility
        else:
            getWinningChance.turn_hit_dict[hitKey][saveKey] += occurencePossibility
            getWinningChance.turn_hit_dict[hitKey][-1] += occurencePossibility
    else:
        cacheValue = (hitKey, saveKey)

        if len(feedHitData.cacheList) > 0:
            if cacheValue in feedHitData.cacheList[-1].keys():
                feedHitData.cacheList[-1][cacheValue] += occurencePossibility
            else:
                feedHitData.cacheList[-1][cacheValue] = occurencePossibility

feedHitData.cacheList = []

def applyHitCacheData(cacheDataList):
    #resultPair = (winRate,chance,hitDataCache,callNumber,invokeNumber)
    #hitDataCache = {(hitKey, saveKey):possibility}
    def invokeCaches(cacheData,cInvokeNum):
        for cCacheValue, cPossibility in cacheData.items():
            if cCacheValue == 'invoke':
                continue
            hitKey = cCacheValue[0]
            saveKey = cCacheValue[1]
            occurencePossibility = cPossibility * cInvokeNum
            if DEBUG_ON:
                print(occurencePossibility)
            if not(hitKey in getWinningChance.turn_hit_dict.keys()):
                getWinningChance.turn_hit_dict[hitKey] = {-1:0.0} #-1 means total
            if not(saveKey in getWinningChance.turn_hit_dict[hitKey].keys()):
                getWinningChance.turn_hit_dict[hitKey][saveKey] = occurencePossibility
                getWinningChance.turn_hit_dict[hitKey][-1] += occurencePossibility
            else:
                getWinningChance.turn_hit_dict[hitKey][saveKey] += occurencePossibility
                getWinningChance.turn_hit_dict[hitKey][-1] += occurencePossibility
   
    def resolveInvokes(chanceCacheData,cInvokeNum = 1):
        cacheData = chanceCacheData[2]
        currentCalledTime = chanceCacheData[3]

        invokeInCacheData = 'invoke' in cacheData.keys() and currentCalledTime > 0

        if invokeInCacheData:
            invokeList = cacheData['invoke']
            for resultKey, invokeNum in invokeList.items():
                numToAdd = invokeNum*currentCalledTime
                cacheDataList[resultKey][3] += numToAdd
                cacheDataList[resultKey][4] += numToAdd
        chanceCacheData[3] = 0

        return invokeInCacheData
        
    
    cacheDataLength = len(cacheDataList)
    totalResolveNumber = 0
    
    while True:
        resolveRemainingNumber = 0

        for saveKey, chanceCacheData in cacheDataList.items():
            if len(chanceCacheData) > 1:
                resolveRemainingNumber += 1 if resolveInvokes(chanceCacheData,1) else 0
        if resolveRemainingNumber == 0:
            break
        elif totalResolveNumber == 0:
            totalResolveNumber = resolveRemainingNumber
        
        if DEBUG_ON:
            print("resolving, remaning", resolveRemainingNumber, '/', totalResolveNumber)
    
    if DEBUG_ON:
        print("resolved!")
    
    counter = 1
    for saveKey, chanceCacheData in cacheDataList.items():
        print('invoking', counter, '/', cacheDataLength)
        if len(chanceCacheData) > 1:
            assert(chanceCacheData[3] == 0)
            invokeCaches(chanceCacheData[2],chanceCacheData[4])
        counter+=1
        
def addHitCacheData(saveKey,factor):
    if len(feedHitData.cacheList) > 0:
        if not('invoke' in feedHitData.cacheList[-1].keys()):
            feedHitData.cacheList[-1]['invoke'] = {}
        if not(saveKey in feedHitData.cacheList[-1]['invoke'].keys()):
            feedHitData.cacheList[-1]['invoke'][saveKey] = factor
        else:
            feedHitData.cacheList[-1]['invoke'][saveKey] += factor

def startHitDataCache(rLevel):
    feedHitData.cacheList.append({})

def endHitDataCache(saveKey,rLevel):
    data = feedHitData.cacheList.pop(-1)
    if len(feedHitData.cacheList) and len(data) > 0:
        if not('invoke' in feedHitData.cacheList[-1].keys()):
            feedHitData.cacheList[-1]['invoke'] = {}
        if not(saveKey in feedHitData.cacheList[-1]['invoke'].keys()):
            feedHitData.cacheList[-1]['invoke'][saveKey] = 1.0
        else:
            feedHitData.cacheList[-1]['invoke'][saveKey] += 1.0
    return data

def saveDictionary(filename,dictionary):
    file = open(filename,"wb")
    pickle.dump(dictionary,file)
    file.close()

def loadDictionary(filename):
    file = open(filename,"rb")
    temp = pickle.load(file)
    file.close()
    return temp

def saveStrategy(filename,strategyToSave):
    strategyDict = {}
    for i in range(0,100):
        if DEBUG_ON:
            print("saving strategy step",i,'/',99)
        for j in range(0,100):
            key = (i,j)
            strategyDict[key] = strategyToSave(i,j)
    saveDictionary(filename,strategyDict)

def loadStrategy(filename):
    strategyDict = loadDictionary(filename)
    def play(score,opponent_score):
        key = (score,opponent_score)
        if key in strategyDict.keys():
            return strategyDict[key]
        else:
            return 0
    return play

def saveWinningChanceWithHistoryResults(filename):
    saveDictionary("savedData/" + filename,getWinningChance.result_dict)

def readWinningChanceWithHistoryResults(filename):
    if path.exists("savedData/" + filename):
        getWinningChance.result_dict = loadDictionary("savedData/" + filename)

def getListNotHit():
    clist = []
    for i in range(100):
        for j in range(100):
            currentKey = (i,j)
            if not(currentKey in getWinningChance.turn_hit_dict.keys()):
                clist.append(currentKey)
    return clist

def saveWinningHitResults(filename):
    saveDictionary("savedData/" + filename,getWinningChance.turn_hit_dict)

def readWinnningHitResults(filename):
    if path.exists("savedData/" + filename):
        getWinningChance.turn_hit_dict = loadDictionary("savedData/" + filename)
    if DEBUG_ON:
        print('notHitKeys', getListNotHit())

def make_winning_chance(score0,score1):
	def func(numToRoll):
		return getWinningChance(False,False,numToRoll,score0,score1,100,0,0,0)
	return func

def strategy_to_play(turnNum, overallTurnNum, selfScore, opponentScore, lastExtraTurn, USE_HIT):
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
        currentWinningRate = getWinningChance(lastExtraTurn,i,selfScore,opponentScore,targetScore,overallTurnNum,0,USE_HIT)
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
    turnNumber = MATCH_CURRENT_TURN_NUM

    #determine strategy to play
    strategyReturn = strategy_to_play(turnNumber,MATCH_OVERALL_TURN_NUM,score,opponent_score,MATCH_LAST_EXTRA,final_strategy.producing_actual_result)
    
    #decode strategyReturn
    numToRollDice = strategyReturn

    return numToRollDice

final_strategy.producing_actual_result = False

def final_strategy_hist(score, opponent_score):
    turnNumber = MATCH_CURRENT_TURN_NUM

    #determine strategy to play
    strategyReturn = strategy_to_play(turnNumber,MATCH_OVERALL_TURN_NUM,score,opponent_score,MATCH_LAST_EXTRA,False)
    
    #decode strategyReturn
    numToRollDice = strategyReturn
    return numToRollDice