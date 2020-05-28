import RPi.GPIO as GPIO          
from time import sleep

#Connections from Motor Driver to Pi GPIO
Rin1 = 21
Rin2 = 20
Ren = 12 # Right Enable
Lin1 = 13
Lin2 = 19
Len = 26 #left Enable

initialvaluespeed=30 # This should be between 0 to 100

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Initialization for right motor
GPIO.setup(Rin1,GPIO.OUT)
GPIO.setup(Rin2,GPIO.OUT)
GPIO.setup(Ren,GPIO.OUT)
GPIO.output(Rin1,GPIO.LOW)
GPIO.output(Rin2,GPIO.LOW)
Rp=GPIO.PWM(Ren,1000)
Rp.start(initialvaluespeed)
#Initialization for left motor
GPIO.setup(Lin1,GPIO.OUT)
GPIO.setup(Lin2,GPIO.OUT)
GPIO.setup(Len,GPIO.OUT)
GPIO.output(Lin1,GPIO.LOW)
GPIO.output(Lin2,GPIO.LOW)
Lp=GPIO.PWM(Len,1000)
Lp.start(initialvaluespeed)

class move():
    def __init__(self):
        print("starting")
        
    def Rspeed(self,val):
        Rp.ChangeDutyCycle(initialvaluespeed+val)
 
    def Lspeed(self,val):
        Lp.ChangeDutyCycle(initialvaluespeed+val)

    def forward(self):
        GPIO.output(Rin2,GPIO.LOW)
        GPIO.output(Rin1,GPIO.HIGH)
        GPIO.output(Lin1,GPIO.LOW)
        GPIO.output(Lin2,GPIO.HIGH)

    def escape():
        GPIO.cleanup()
