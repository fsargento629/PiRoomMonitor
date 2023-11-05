#!/usr/bin/python
# coding=utf-8
 
# Needed modules will be imported
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import datetime
import csv
import os


def Write2CSV(file_name,temp,hum,date):
    row = [date,temp,hum]
    # append data to main csv
    with open(file_name, 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()

    # edit lastValues file
    current_status_filename = '/var/www/html/current_sensor_data.csv'
    if os.path.exists(current_status_filename):
        os.remove(current_status_filename)
        print(current_status_filename +" has been deleted.")
    else:
        print(current_status_filename + " does not exist or could not be found.")
    #write to it now after deleting
    with open(current_status_filename, 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()


csv_name = '/var/www/html/sensor_data.csv'
# Log data every 30 seconds
sleeptime = 30
 
# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHTSensor = Adafruit_DHT.DHT11
 
# The pin which is connected with the sensor will be declared here
GPIO_Pin = 14
 
print('KY-015 sensortest - temperature and humidity')
 
try:
    while(1):
        # Measurement will be started and the result will be written into the variables
        humid, temper = Adafruit_DHT.read_retry(DHTSensor, GPIO_Pin)
 
        print("-----------------------------------------------------------------")
        if humid is not None and temper is not None:
 
            # The result will be shown at the console
            print('temperature = {0:0.1f}C  | rel. humidity = {1:0.1f}%'.format(temper, humid))
            Write2CSV(csv_name,temper,humid,datetime.datetime.now())
         
        # Because of the linux OS, the Raspberry Pi has problems with realtime measurements.
        # It is possible that, because of timing problems, the communication fails.
        # In that case, an error message will be displayed - the result should be shown at the next try.
        else:
            print('Error while reading - please wait for the next try!')
        print("-----------------------------------------------------------------")
        print("")
        time.sleep(sleeptime)
 
# Scavenging work after the end of the program
except KeyboardInterrupt:
    GPIO.cleanup() 
