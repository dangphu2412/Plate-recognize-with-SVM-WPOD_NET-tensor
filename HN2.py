import RPi.GPIO as GPIO
from time import sleep
import Servo
import read_plate as detect
import LCD
import firestore

GPIO.setmode(GPIO.BCM)

GPIO.setup(25, GPIO.IN) #in
GPIO.setup(22, GPIO.IN) #servo
track = 0
status = False
while True:
   sensorIn = GPIO.input(25)
   sensorTracking = GPIO.input(22)

   if sensorIn == 0 and track == 0:
       print("Fuck")
       plate = detect.get_plate()
       if plate != "":
            status = firestore.getInfoByPlate(plate)
            if status != False:
                moneyBack = status["money"] - 5000
                firestore.updateDB(plate, moneyBack, status["status"])
                sleep(0.1)
                Servo.openServo()
                LCD.LCD(plate)
                track = track + 1
            else: LCD.LCD("Bien so ko hop le")
       else: LCD.LCD("Bien so ko hop le")
   if sensorTracking == 0 and track == 1:
       track = 0
   if sensorIn == 1 and sensorTracking == 1 and track == 0:
       Servo.closeServo()
       print("This is 0")
       sleep(0.1)
