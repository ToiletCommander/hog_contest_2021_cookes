@echo off
echo "Training"

SET numEpoch=%1
for /l %%x in (1, 1, %numEpoch%) do (
   echo Training %%x out of %numEpoch%
   python generateHitRate.py
)

echo Finished Training
pause