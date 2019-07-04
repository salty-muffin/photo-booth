import RPi.GPIO as GPIO
import time

class Bounce:
    """a debouncer class for the GPIO pins on the raspberry pi.
       inspired by thomasfredericks Bounce2 library for the
       arduino (https://github.com/thomasfredericks/Bounce2)"""
    # constructor with pin, pull-up/pull-down resisistor, which event to be detected and debounce time
    def __init__(self, pin, up_down, debounce):
        self.pin = pin # pin
        self.debounce = debounce # debounce time
        self.pressed = False # has an event been detected?
        self.event = False # which event?
        self.timer = 0 # counter since event

        self.last_state = False
        self.state = False
        self.rising = False
        self.falling = False

        # setup GPIO
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=up_down)

    # read input and calculate debounced input
    def update(self):
        self.state = GPIO.input(self.pin)

        if self.state != self.last_state and not self.pressed: # if something changes
            self.timer = time.time()
            self.event = self.state

            self.pressed = True
        elif self.timer + self.debounce < time.time() and self.pressed: # if debounce time has elapsed after change
            self.rising = self.state and self.event
            self.falling = not self.state and not self.event

            self.pressed = False
        else:
            self.last_state = self.state

    # returns true if risen
    def rising(self):
        if self.rising:
            self.rising = False
            return True

        return False

    # returns true if fallen
    def falling(self):
        if self.falling:
            self.falling = False
            return True

        return False

    # to read pin state
    def state(self):
        return GPIO.input(self.pin)

    # set the debounce time
    def setDebounce(self, debounce):
        self.debounce = debounce
