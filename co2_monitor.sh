#!/bin/bash

# change into directory of co2_monitor
cd /home/pi/devel/co2_monitor

# log sensor data
./data_logger.py > data_logger.log 2>&1

# get last 500 records, keeping the header
head -n 1 data_log.csv > data_log_last_500.csv
tail -n 500 data_log.csv | grep -v Datetime >> data_log_last_500.csv

# evaluate data and create plot
./data_plotter.py > data_plotter.log 2>&1

# switch traffic lights
./ampel.py > ampel.log 2>&1
