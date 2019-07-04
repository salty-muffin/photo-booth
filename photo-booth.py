# imports ----------------------------------------------------------------------
import  RPi.GPIO as GPIO
import os
import time
from bounce import *

# gpio pins --------------------------------------------------------------------
SHUTTER   = 0
POWER     = 0
GREEN_LED = 0
RED_LED   = 0

# main script ------------------------------------------------------------------
# setup ------------------------------------------------------------------------
GPIO.setmode(GPIO.BCM)
# outputs
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
# inputs
shutter = Bounce(SHUTTER, GPIO.PUD_UP, 0.1)
power = Bounce(POWER, GPIO.PUD_UP, 2)
# set leds
GPIO.output(RED_LED, GPIO.HIGH)
time.sleep(1)
GPIO.output(RED_LED, GPIO.LOW)
time.sleep(1)
GPIO.output(GREEN_LED, GPIO.HIGH)

# loop -------------------------------------------------------------------------
run = True
while run:
    # update the debounced inputs
    shutter.update()
    power.update()

    if shutter.falling(): # when shutter button is pressed
        # led sequence
        GPIO.output(RED_LED, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(RED_LED, GPIO.LOW)
        time.sleep(1.5)
        GPIO.output(RED_LED, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(RED_LED, GPIO.LOW)
        time.sleep(1.5)
        GPIO.output(RED_LED, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(RED_LED, GPIO.LOW)
        time.sleep(1.5)
        GPIO.output(RED_LED, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(RED_LED, GPIO.LOW)

        # shoot & print
        os.system('raspistill -n -t 200 -w 512 -h 384 -o - | lp')

    elif power.rising(): # when power butten is pressed
        # exit main loop
        run = False

# cleanup & shutdown
GPIO.output(GREEN_LED, GPIO.LOW)
GPIO.cleanup()
os.system('shutdown -h now')
