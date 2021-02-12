@echo off
echo "Training"

SET numEpoch=10
for /l %%x in (1, 1, %numEpoch%) do (
   echo Training %%x out of %numEpoch%
   python generateHitRate.py
)

echo Finished Training
pause