import final_strategy_train
import baseline_strategy
import test
import time
import submissions

TRAIN_START_NAME = submissions.STRATEGY_NAME
TRAIN_EPOCH_NUM = submissions.EPOCH_NUM

FILENAME = 'savedStrats/' + TRAIN_START_NAME + "_" + str(TRAIN_EPOCH_NUM) + ".pkl"


print("Feeding Test Results to form hit data")

startTime = time.time()

withHistWinningChanceFileName = TRAIN_START_NAME + "_historyChance.pkl"
hitRateFileName = TRAIN_START_NAME + "_hitRate.pkl"

final_strategy_train.readWinningChanceWithHistoryResults(withHistWinningChanceFileName)
final_strategy_train.readWinnningHitResults(hitRateFileName)
readFinishTime = time.time()
print("it took",(readFinishTime - startTime),"to read from pre-trained data")


final_strategy_train.final_strategy.producing_actual_result = True

final_strategy_train.saveStrategy(FILENAME,final_strategy_train.final_strategy)


endTime = time.time()
timeDiff = endTime - startTime

print("Generation Finished in",timeDiff,"seconds")