import RPi.GPIO as gpio
import time
trig_pin = 13
echo_pin = 19
led_pin = [4,5,6]

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(led_pin, gpio.OUT)
gpio.setup(trig_pin, gpio.OUT)
gpio.setup(echo_pin, gpio.IN)

gpio.output(trig_pin, False)
time.sleep(1)
print("start")
try:
    while True:
        gpio.output(trig_pin, False)
        time.sleep(1)
        gpio.output(trig_pin, True)
        time.sleep(1)
        gpio.output(trig_pin, False)
        while gpio.input(echo_pin) == 0:
            pulse_start = time.time()
        while gpio.input(echo_pin) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 34000 / 2
        distance = round(distance, 2)
        
        gpio.output(led_pin, False)
        if distance > 40:
            gpio.output(led_pin[0], True)
            print("Green High")
        elif distance > 20:
            gpio.output(led_pin[1], True)
            print("Yellow High")
        else:
            gpio.output(led_pin[2], True)
            print("Red High")
        print("Distance : ", distance, "cm")
except KeyboardInterrupt:
    gpio.cleanup()
