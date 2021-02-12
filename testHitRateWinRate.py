import final_strategy_train
import baseline_strategy
import test
import time
import submissions

TRAIN_START_NAME = submissions.STRATEGY_NAME

def performTest():
    test.tests(baseline_strategy.baseline_strategy,final_strategy_train.final_strategy,1500,False,True)
    test.tests(final_strategy_train.more_boar_strategy,final_strategy_train.final_strategy,1500,False,True)
    test.tests(final_strategy_train.final_strategy_hist,final_strategy_train.final_strategy,5000,False,True)


print("Feeding Test Results to form hit data")

startTime = time.time()

withHistWinningChanceFileName = TRAIN_START_NAME + "_historyChance.pkl"
hitRateFileName = TRAIN_START_NAME + "_hitRate.pkl"

final_strategy_train.readWinningChanceWithHistoryResults(withHistWinningChanceFileName)
final_strategy_train.readWinnningHitResults(hitRateFileName)
readFinishTime = time.time()
print("it took",(readFinishTime - startTime),"to read from pre-trained data")


final_strategy_train.final_strategy.producing_actual_result = True


print("Feeding Test Result to test hit data")

performTest()

endTime = time.time()
timeDiff = endTime - startTime

print("Generate Finished in",timeDiff,"seconds")