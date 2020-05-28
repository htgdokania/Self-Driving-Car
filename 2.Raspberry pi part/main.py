from time import sleep
import CarMove
import ActionClientRead
from ultrasonic import UltraSonic 
US=UltraSonic()
m1=CarMove.move()

dat=[0,0,0,0,0]
while 1:
    c=0
    D=ActionClientRead.Tcp_Read()
    for b in D:
        dat[c]=b
        c+=1
    left=dat[0]  # number of left lines detected
    right=dat[1] # number of right lines detected
    red=dat[2]   # Indicate whether red Color Marker present (1) or Not (0)

    dis=US.Distance() #Get current Distance from US sensor
    print("distance=",dis)
    print("left=",left)
    print("right=",right)
    
    speedR,speedL,setback=0,0,0

    if red or dis<15 : # Stop the car if condition is true 
        speedR=-1*CarMove.initialvaluespeed
        speedL=-1*CarMove.initialvaluespeed
    elif(left>right): # if left is more ==> move left by stopping the left wheel.
        speedR=10
        speedL=-1*CarMove.initialvaluespeed
    elif(right>left): # if right is more==> move right by stopping the right wheel.
        speedL=10
        speedR=-1*CarMove.initialvaluespeed

    m1.Rspeed(speedR)
    m1.Lspeed(speedL)
    m1.forward()
