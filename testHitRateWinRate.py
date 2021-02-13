import final_strategy_train
import baseline_strategy
import test
import time
import submissions
from os import path

TRAIN_START_NAME = submissions.STRATEGY_NAME
TRAIN_EPOCH_NUM = submissions.EPOCH_NUM

FILENAME = 'savedStrats/' + TRAIN_START_NAME + "_" + str(TRAIN_EPOCH_NUM) + ".pkl"

finalStrategyToTrain = final_strategy_train.loadStrategy(FILENAME) if path.exists(FILENAME) else final_strategy_train.final_strategy

def performTest():
    test.predicts(final_strategy_train.more_boar_strategy,finalStrategyToTrain,True)
    test.predicts(final_strategy_train.final_strategy_hist,finalStrategyToTrain,True)
    test.predicts(final_strategy_train.loadStrategy("savedStrats/optimal_fairStart_1.pkl"),finalStrategyToTrain,True)


print("Loading Trainned Results to hit data")

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

print("Test Finished in",timeDiff,"seconds")