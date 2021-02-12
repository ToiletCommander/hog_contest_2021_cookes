@echo off

TrainNumEpochs %1
echo Testing...

performTest

echo Submitting

python ok --submit --timeout 0

pause