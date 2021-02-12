import final_strategy_train
import submissions
import time

PLAYER_NAME = submissions.SUBMIT_NAME
TRAIN_STRATEGY_NAME = submissions.STRATEGY_NAME
DEBUG_ON = False

final_strategy = final_strategy_train.final_strategy


startTime = time.time()

withHistWinningChanceFileName = TRAIN_STRATEGY_NAME + "_historyChance.pkl"
hitRateFileName = TRAIN_STRATEGY_NAME + "_hitRate.pkl"

final_strategy_train.readWinningChanceWithHistoryResults(withHistWinningChanceFileName)
final_strategy_train.readWinnningHitResults(hitRateFileName)

readFinishTime = time.time()

if DEBUG_ON:
    print("it took",(readFinishTime - startTime),"to read from pre-trained data")

