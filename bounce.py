import RPi.GPIO as GPIO
import time

class Bounce:
    """a debouncer class for the GPIO pins on the raspberry pi.
       heavily inspired by thomasfredericks Bounce2 library for
       the arduino (https://github.com/thomasfredericks/Bounce2)"""
    # constructor with pin, pull-up/pull-down resisistor, which event to be detected and debounce time
    def __init__(self, pin, up_down, rising_falling, debounce):
        self.pin = pin # pin
        self.debounce = debounce # debounce time
        self.pressed = False # has an event been detected?
        self.event = False # which event?
        self.timer = 0 # counter since event

        # setup GPIO
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=up_down)
        GPIO.add_event_detect(channel, rising_falling)

    # to read the debounced input
    def read(self):
        if GPIO.event_detect(self.pin) and not self.pressed: # if an event has been detected
            self.timer = time.time()
            self.event = GPIO.input(self.pin)
            self.pressed = True

        if self.timer + self.debounce < time.time() and self.pressed: # if an event has happened and the debounce time has elapsed
            self.pressed = False
            if GPIO.input(self.pin) == self.event:
                return True

        return False

    # to read pin state
    def status(self):
        return GPIO.input(self.pin)
