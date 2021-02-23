
GOAL_SCORE = 100
from dice import four_sided,six_sided

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    sum = 0
    sow_sad = False
    for i in range(num_rolls):
        currentRoll = dice()
        if(currentRoll == 1):
            sow_sad = True
        else:
            sum += currentRoll
    returnVal = 1 if sow_sad else sum
    return returnVal
    # END PROBLEM 1


def piggy_points(score):
    """Return the points scored from rolling 0 dice.

    score:  The opponent's current score.
    """
    scoreSq = score ** 2
    smallestDigit = -1
    while scoreSq > 0:
        currentDigit = scoreSq % 10
        scoreSq = scoreSq // 10
        if currentDigit < smallestDigit or smallestDigit == -1:
            smallestDigit = currentDigit
    if smallestDigit == -1:
        smallestDigit = 0
    
    returnVal = smallestDigit + 3
    return returnVal


def take_turn(num_rolls, opponent_score, dice=six_sided, goal=GOAL_SCORE):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 in the case
    of a player using Piggy Points.
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    goal:            The goal score of the game.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < goal, 'The game should be over.'
    # BEGIN PROBLEM 3
    if num_rolls == 0:
        return piggy_points(opponent_score)
    else:
        return roll_dice(num_rolls,dice)
    # END PROBLEM 3

def possibility_of_rolling_one_point(numSide, numDice):
    if numDice < 1:
        return 0
    elif numSide < 1:
        return 0
    return pow(1.0/numSide,numDice)

def avg_score_of_sides_not_one(numSide):
    return(numSide * (numSide+1) / 2.0 - 1.0) / (numSide-1.0)

def avg_score_of_rolling(numSide, numDice):
    possibilityOfGettingOne = possibility_of_rolling_one_point(numSide,numDice)
    return possibilityOfGettingOne * 1 + (1-possibilityOfGettingOne) * (avg_score_of_sides_not_one(numSide))

def calc_turn_avg(num_rolls, opponent_score, sideNum):
    return avg_score_of_rolling(sideNum,num_rolls) if num_rolls >= 1 else piggy_points(opponent_score)

def calc_turn_score(diceOutcomes,opponent_score):
    if(len(diceOutcomes) == 0):
        return piggy_points(opponent_score)
    sumScore = 0
    for i in range(len(diceOutcomes)):
        if diceOutcomes[i] != 1:
            sumScore += diceOutcomes[i]
        else:
            sumScore = 1
            break
    return sumScore


def getDigitsFromRightToLeft(number):
    digits = []
    if(number == 0):
        return [0]
    while number > 0:
        digits.append(number % 10)
        number = number // 10
    return digits

def getDigitsFromLeftToRight(number):
    rToL = getDigitsFromRightToLeft(number)
    rToL.reverse()
    return rToL
    
def getFirstAndSecondDigit(number):
    fDigit, sDigit = 0,0
    while(number >= 100):
        number = number // 10
    sDigit = number % 10
    
    if(number < 10):
        fDigit = 0
    else:
        fDigit = number // 10
    return fDigit, sDigit


def more_boar(player_score, opponent_score):
    """Return whether the player gets an extra turn.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.

    >>> more_boar(21, 43)
    True
    >>> more_boar(22, 43)
    True
    >>> more_boar(43, 21)
    False
    >>> more_boar(12, 12)
    False
    >>> more_boar(7, 8)
    False
    """
    playerfDigit, playersDigit = getFirstAndSecondDigit(player_score)
    opponentfDigit, opponentsDigit = getFirstAndSecondDigit(opponent_score)
    return(playerfDigit < opponentfDigit and playersDigit < opponentsDigit)

def time_trot(turn, numRolls, lastExtra):
    return (turn % 8 == numRolls and not(lastExtra))
