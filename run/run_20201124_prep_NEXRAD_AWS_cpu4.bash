#!/bin/bash

#for i in {0..40} ; do
#for i in {41..80} ; do
#for i in {81..120} ; do
for i in {121..155} ; do
    python ../src/NEXRAD/prep_NEXRAD_AWS_PyART.py train ${i} 2015-01-01 >& log${i}
done    





