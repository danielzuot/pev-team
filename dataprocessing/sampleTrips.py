import csv
import requests
import json
import datetime

dropoff_csv = '../../Taxi/TaxiData_pt1/filtered_taxi_9_12/filtered_dropoffs_9_12.csv'
pickup_csv = '../../Taxi/TaxiData_pt1/filtered_taxi_9_12/filtered_pickups_9_12.csv'
morning_dropoff_csv = '../../Taxi/repData/rep_dropoffs_morning_9_12.csv'
morning_pickup_csv = '../../Taxi/repData/rep_pickups_morning_9_12.csv'
afternoon_dropoff_csv = '../../Taxi/repData/rep_dropoffs_afternoon_9_12.csv'
afternoon_pickup_csv = '../../Taxi/repData/rep_pickups_afternoon_9_12.csv'
evening_dropoff_csv = '../../Taxi/repData/rep_dropoffs_evening_9_12.csv'
evening_pickup_csv = '../../Taxi/repData/rep_pickups_evening_9_12.csv'
driveMode = "driving"
bikeMode = "bicycling"
DTZ_API_KEY = "AIzaSyDLnF0RwcwqWQtnZwyjwe0V0qJjmJmnH1c"
JXM_API_KEY = "AIzaSyAbJsA8HEWB8X50nD_rH_vcwt84D4588Ww"
skip = 100
morningStartHr=6
morningStartMin=0
morningEndHr=12
morningEndMin=0
afternoonStartHr=12
afternoonStartMin=0
afternoonEndHr=18
afternoonEndMin=0
eveningStartHr=18
eveningStartMin=0
eveningEndHr=23
eveningEndMin=59


def convertToDatetime(x):
    xList = x.split()

    dateList = xList[0].split('/')
    month = int(dateList[0])
    day = int(dateList[1])
    year = int(dateList[2])

    timeList = xList[1].split(":")
    hour = int(timeList[0])
    minute = int(timeList[1])
    AMPM = xList[2]
    if AMPM=='PM' and hour!=12:
        hour += 12
    elif AMPM=='AM' and hour==12:
        hour-=12

    dt = datetime.datetime(year = year,month = month,day = day,hour = hour,minute = minute)
    return dt

def isBetween(dt,startHr,startMin,endHr,endMin):
    if dt.time() > datetime.time(startHr,startMin):
        if dt.time() < datetime.time(endHr,endMin):
            return True
    return False 

untilSkip = skip
morningCount = 0
afternoonCount = 0
eveningCount = 0
with open(dropoff_csv, 'rt') as dropoffs:
    dropoffReader = csv.reader(dropoffs)
    for dropoffRow in dropoffReader:
        if untilSkip > 0:
            untilSkip-=1
            continue
        tripID = dropoffRow[0]
        dropoffTime = dropoffRow[1]
        dropoffAddress = dropoffRow[2]
        dropoffLong = dropoffRow[3]
        dropoffLat = dropoffRow[4]
        with open(pickup_csv,'rt') as pickups:
            pickupReader = csv.reader(pickups)
            for pickupRow in pickupReader:
                if pickupRow[0] == tripID:
                    pickupTime = pickupRow[1]
                    pickupAddress = pickupRow[2]
                    pickupLong = pickupRow[3]
                    pickupLat = pickupRow[4]
                    pickup = convertToDatetime(pickupTime)
                    dropoff = convertToDatetime(dropoffTime)
                    if isBetween(pickup,morningStartHr,morningStartMin,morningEndHr,morningEndMin):
                        if morningCount<=300:
                            dropCSV = open(morning_dropoff_csv,'a', newline='')
                            dropWriter = csv.writer(dropCSV)
                            dropWriter.writerow(dropoffRow)
                            pickCSV = open(morning_pickup_csv,'a', newline='')
                            pickWriter = csv.writer(pickCSV)
                            pickWriter.writerow(pickupRow)
                            morningCount+=1
                    elif isBetween(pickup,afternoonStartHr,afternoonStartMin,afternoonEndHr,afternoonEndMin):
                        if afternoonCount<=300:
                            dropCSV = open(afternoon_dropoff_csv,'a', newline='')
                            dropWriter = csv.writer(dropCSV)
                            dropWriter.writerow(dropoffRow)
                            pickCSV = open(afternoon_pickup_csv,'a', newline='')
                            pickWriter = csv.writer(pickCSV)
                            pickWriter.writerow(pickupRow)
                            afternoonCount+=1
                    elif isBetween(pickup,eveningStartHr,eveningStartMin,eveningEndHr,eveningEndMin):
                        if eveningCount<=300:
                            dropCSV = open(evening_dropoff_csv,'a', newline='')
                            dropWriter = csv.writer(dropCSV)
                            dropWriter.writerow(dropoffRow)
                            pickCSV = open(evening_pickup_csv,'a', newline='')
                            pickWriter = csv.writer(pickCSV)
                            pickWriter.writerow(pickupRow)
                            eveningCount+=1
                    break
        untilSkip = skip
        print("Morning: "+str(morningCount))
        print("Afternoon: "+str(afternoonCount))
        print("Evening: "+str(eveningCount)+'\n')

        if morningCount>=300 and afternoonCount>=300 and eveningCount>=300:
            break


