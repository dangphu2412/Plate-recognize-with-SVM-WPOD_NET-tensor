import RPi.GPIO as IO  #Khai báo thư viện RPi.GPIO tên IO
from time import sleep #Khai báo lệnh sleep từ thư viện ime

servo=18               #Khai báo chân Servo = GPIO18

IO.setwarnings(False)  #Tắt thông báo
IO.setmode (IO.BCM)    #Khai báo dạng chân BCM
IO.setup(servo,IO.OUT) #Khai báo chân Servo OUTPUT
p = IO.PWM(servo,50)   #Khai báo xung 50Hz
p.start(2)             #Bắt đầu xung tại chu kì = 2

def openServo():
        try:      
                sleep(.1)
                DutyCycle = 90/18+2        
                p.ChangeDutyCycle(DutyCycle)
                sleep(.5)
        except KeyboardInterrupt:           
                IO.cleanup()                
                print('DONE')

def closeServo():
        try:      
                sleep(1)       
                p.ChangeDutyCycle(2)
                sleep(.5)
        except KeyboardInterrupt:           
                IO.cleanup()                
                print('DONE')
