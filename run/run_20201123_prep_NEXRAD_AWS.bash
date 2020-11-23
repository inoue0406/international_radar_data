#!/bin/bash
python ../src/NEXRAD/prep_NEXRAD_AWS_PyART.py train 0 2015-01-01 >& log00 &
python ../src/NEXRAD/prep_NEXRAD_AWS_PyART.py train 1 2015-01-01 >& log01 &
python ../src/NEXRAD/prep_NEXRAD_AWS_PyART.py train 2 2015-01-01 >& log02 &
python ../src/NEXRAD/prep_NEXRAD_AWS_PyART.py train 3 2015-01-01 >& log03 &
#python ../src/prep_NEXRAD_AWS_PyART.py train 0 2015-01-01 >& log04 &




