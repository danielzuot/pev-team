import csv
import requests
import json
import datetime

def calculateTimeDifference(pickupTime,dropoffTime):
    pickupList = pickupTime.split()

    pickupDateList = pickupList[0].split('/')
    pickupMonth = int(pickupDateList[0])
    pickupDay = int(pickupDateList[1])
    pickupYear = int(pickupDateList[2])

    pickupTimeList = pickupList[1].split(":")
    pickupHour = int(pickupTimeList[0])
    pickupMinute = int(pickupTimeList[1])
    pickupAMPM = pickupList[2]
    if pickupAMPM=='PM' and pickupHour!=12:
        pickupHour += 12
    elif pickupAMPM=='AM' and pickupHour==12:
        pickupHour-=12

    pickup = datetime.datetime(year = pickupYear,month = pickupMonth,day = pickupDay,hour = pickupHour,minute = pickupMinute)

    dropoffList = dropoffTime.split()

    dropoffDateList = dropoffList[0].split('/')
    dropoffMonth = int(dropoffDateList[0])
    dropoffDay = int(dropoffDateList[1])
    dropoffYear = int(dropoffDateList[2])

    dropoffTimeList = dropoffList[1].split(":")
    dropoffHour = int(dropoffTimeList[0])
    dropoffMinute = int(dropoffTimeList[1])
    dropoffAMPM = dropoffList[2]
    if dropoffAMPM=='PM' and dropoffHour!=12:
        dropoffHour += 12
    elif dropoffAMPM=='AM' and dropoffHour==12:
        dropoffHour-=12

    dropoff = datetime.datetime(year = dropoffYear,month = dropoffMonth,day = dropoffDay,hour = dropoffHour,minute = dropoffMinute)

    difference = dropoff - pickup
    return difference.total_seconds()

dropoff_csv = '../Taxi/TaxiData_pt1/filtered_taxi_9_12/filtered_dropoffs_9_12.csv'
pickup_csv = '../Taxi/TaxiData_pt1/filtered_taxi_9_12/filtered_pickups_9_12.csv'
driveMode = "driving"
bikeMode = "bicycling"
DTZ_API_KEY = "AIzaSyDLnF0RwcwqWQtnZwyjwe0V0qJjmJmnH1c"
JXM_API_KEY = "AIzaSyAbJsA8HEWB8X50nD_rH_vcwt84D4588Ww"

totalMapsDriveTime = 0
totalMapsBikeTime = 0
totalTaxiTime = 0
tripCount = 0
with open(dropoff_csv, 'rt') as dropoffs:
    dropoffReader = csv.reader(dropoffs)
    for dropoffRow in dropoffReader:
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


                    rDrive = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins="+pickupAddress+"&destinations="+dropoffAddress+"&mode="+driveMode+"&key="+DTZ_API_KEY)
                    rBike = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins="+pickupAddress+"&destinations="+dropoffAddress+"&mode="+bikeMode+"&key="+DTZ_API_KEY)
                    resultBike = json.loads(rBike.text)
                    resultDrive = json.loads(rDrive.text)
                    if resultDrive['rows'][0]['elements'][0]['status'] == 'NOT_FOUND':
                        print("couldn't find distance")
                        print("\n")
                        break
                    mapsDriveDuration = resultDrive['rows'][0]['elements'][0]['duration']['value']
                    mapsBikeDuration = resultBike['rows'][0]['elements'][0]['duration']['value']
                    driveDuration = calculateTimeDifference(pickupTime,dropoffTime)
                    '''if mapsDuration > 3*driveDuration:
                        print("something's wrong")
                        print("Picked up at: "+pickupAddress)
                        print("Dropped off at: "+dropoffAddress)
                        print("Maps duration: "+str(mapsDuration))
                        print("Taxi duration: "+str(driveDuration))
                        print("\n")
                        break'''
                    totalMapsDriveTime += mapsDriveDuration
                    totalMapsBikeTime += mapsBikeDuration
                    totalTaxiTime += driveDuration
                    tripCount=tripCount+1
                    print("Ideal Drive: "+str(mapsDriveDuration))
                    print("Ideal Bike: "+str(mapsBikeDuration))
                    print("Taxi: "+str(driveDuration))
                    print("Ideal Drive Total: "+str(totalMapsDriveTime))
                    print("Ideal Bike Total: "+str(totalMapsBikeTime))
                    print("Taxi Total: "+str(totalTaxiTime))
                    print("Trip count: "+str(tripCount))
                    print("\n")
                    break
