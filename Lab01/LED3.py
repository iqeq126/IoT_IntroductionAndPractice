import RPi.GPIO as gpio
import time
gpio.setwarnings(False)
pin = [5, 6, 12]
LED = [1,2,3] 
s = int(input("Let's input(1:3)"))
gpio.setmode(gpio.BCM)
gpio.setup(pin, gpio.OUT)
while True:
    gpio.output(pin, False)
    if s in LED: gpio.output(pin[s-1], True)    
    else: break
    s=int(input("Let's input(1:3)"))
gpio.cleanup()
print("Blink Finished")

