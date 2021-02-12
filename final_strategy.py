import final_strategy_train
import submissions
import time
from os import path

PLAYER_NAME = submissions.SUBMIT_NAME
TRAIN_STRATEGY_NAME = submissions.STRATEGY_NAME
TRAIN_EPOCH_NUM = submissions.EPOCH_NUM

FILENAME = 'savedStrats/' + TRAIN_STRATEGY_NAME + "_" + str(TRAIN_EPOCH_NUM) + ".pkl"
DEBUG_ON = False

final_strategy = final_strategy_train.loadStrategy(FILENAME) if path.exists(FILENAME) else final_strategy_train.final_strategy

startTime = time.time()

withHistWinningChanceFileName = TRAIN_STRATEGY_NAME + "_historyChance.pkl"
hitRateFileName = TRAIN_STRATEGY_NAME + "_hitRate.pkl"

final_strategy_train.readWinningChanceWithHistoryResults(withHistWinningChanceFileName)
final_strategy_train.readWinnningHitResults(hitRateFileName)

final_strategy_train.final_strategy.producing_actual_result = True

readFinishTime = time.time()

if DEBUG_ON:
    print("it took",(readFinishTime - startTime),"to read from pre-trained data")

