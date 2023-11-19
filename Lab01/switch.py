import RPi.GPIO as gpio
import time
gpio.setwarnings(False)
switch_pin = 13
pin = 5
pin2 = 6
gpio.setmode(gpio.BCM)
gpio.setup(switch_pin, gpio.IN, gpio.PUD_UP)
gpio.setup(pin, gpio.OUT)
gpio.setup(pin2, gpio.OUT)
def button():
    isClicked = False
    if gpio.input(switch_pin) == 0:
        isClicked = True
        
    return isClicked
try:
    while True:
        gpio.output(pin, False)    
        gpio.output(pin2, False)
        if button() == True:
            gpio.output(pin, True)
            gpio.output(pin2, False)
        else:
            gpio.output(pin2, True)
            gpio.output(pin, False)
        

except KeyboardInterrupt:
    gpio.cleanup()
    print("Blink Finished")


