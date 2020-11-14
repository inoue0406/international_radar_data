#!/bin/bash
python ../src/download_aws_nexrad_lv2.py train 0 2015-01-01 >& log00 &
python ../src/download_aws_nexrad_lv2.py train 1 2015-01-01 >& log01 &
python ../src/download_aws_nexrad_lv2.py train 2 2015-01-01 >& log02 &
python ../src/download_aws_nexrad_lv2.py train 3 2015-01-01 >& log03 &
python ../src/download_aws_nexrad_lv2.py train 4 2015-01-01 >& log04 &




