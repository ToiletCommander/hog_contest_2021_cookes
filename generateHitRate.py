import final_strategy
import baseline_strategy
import test
import time
import submissions

READ_TRAINNED_DATA = True
TRAINING_START_NAME = submissions.STRATEGY_NAME

def train():
    test.tests(final_strategy.more_boar_strategy,final_strategy.final_strategy,100000,False,True)
    #test.tests(baseline_strategy,final_strategy,2500,False,not(SUBMIT))
    test.tests(final_strategy.final_strategy_hist,final_strategy.final_strategy,100000,False,True)


print("Feeding Test Results to form hit data")

startTime = time.time()

withHistWinningChanceFileName = TRAINING_START_NAME + "_historyChance.pkl"
hitRateFileName = TRAINING_START_NAME + "_hitRate.pkl"
final_strategy.final_strategy.producing_actual_result = False
if READ_TRAINNED_DATA:

    final_strategy.readWinningChanceWithHistoryResults(withHistWinningChanceFileName)
    final_strategy.readWinnningHitResults(hitRateFileName)
    readFinishTime = time.time()
    print("it took",(readFinishTime - startTime),"to read from pre-trained data")

train()

final_strategy.saveWinningChanceWithHistoryResults(withHistWinningChanceFileName)
final_strategy.saveWinningHitResults(hitRateFileName)

endTime = time.time()
timeDiff = endTime - startTime

print("Generate Finished in",timeDiff,"seconds")