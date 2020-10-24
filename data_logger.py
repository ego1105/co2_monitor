#!/usr/bin/python3
# -*- coding:utf-8 -*-

from time import sleep
import csv
import os.path
from datetime import datetime

# import sensors
import Adafruit_DHT
import mh_z19

# data file name
file_name = 'data_log.csv'

# sensor settings
dht_sensor = Adafruit_DHT.DHT22
dht_pin = 4

try:
    #if the file does not already exist, create a new file with headers
    if not os.path.isfile(file_name):
        csv_headers = ['Datetime', 'Temp/°C', 'Feucht/%', 'CO2/ppm']
        with open(file_name, 'w') as new_data_file:
            datawriter = csv.writer(new_data_file)
            datawriter.writerow(csv_headers)

    # datetime
    now = datetime.now()       
            
    # sensor humidity and temp
    humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)

    # sensor CO2    
    mh_z19_data = mh_z19.read_all(serial_console_untouched=True)
    co2 = mh_z19_data["co2"]

    # comine data in list
    new_log = []
    new_log.append(now)
    new_log.append( "%0.1f" % temperature )
    new_log.append( "%0.1f" % humidity)        
    new_log.append( "%0.0f" % co2)        
    
    #write results to log
    with open(file_name, 'a') as data_log:
        logwriter = csv.writer(data_log)
        logwriter.writerow(new_log)
        data_log.flush()

except IOError as e:
    print(e)
    
except KeyboardInterrupt:    
    print("ctrl + c:")    
    exit()

