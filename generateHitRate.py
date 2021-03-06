import final_strategy_train
import baseline_strategy
import test
import time
import submissions

READ_TRAINNED_DATA = True
TRAINING_START_NAME = submissions.STRATEGY_NAME

def train():
    #test.predicts(final_strategy_train.final_strategy_hist,final_strategy_train.final_strategy,True,False,True,True)
    test.predicts(final_strategy_train.loadStrategy('savedStrats/ultimate1_1.pkl'),final_strategy_train.final_strategy,True,False,True,True)
    test.predicts(final_strategy_train.loadStrategy('savedStrats/ultimate_2.pkl'),final_strategy_train.final_strategy,True,True,True,True)
    test.predicts(final_strategy_train.more_boar_strategy,final_strategy_train.final_strategy,True,True,True,True)
    test.predicts(baseline_strategy.baseline_strategy,final_strategy_train.final_strategy,True,True,True,True)


print("Feeding Test Results to form hit data")

startTime = time.time()

withHistWinningChanceFileName = TRAINING_START_NAME + "_historyChance.pkl"
hitRateFileName = TRAINING_START_NAME + "_hitRate.pkl"
final_strategy_train.final_strategy.producing_actual_result = False
if READ_TRAINNED_DATA:
    final_strategy_train.readWinningChanceWithHistoryResults(withHistWinningChanceFileName)
    final_strategy_train.readWinnningHitResults(hitRateFileName)
    readFinishTime = time.time()
    print("it took",(readFinishTime - startTime),"to read from pre-trained data")

train()

final_strategy_train.saveWinningChanceWithHistoryResults(withHistWinningChanceFileName)
final_strategy_train.saveWinningHitResults(hitRateFileName)

endTime = time.time()
timeDiff = endTime - startTime

print("Generate Finished in",timeDiff,"seconds")