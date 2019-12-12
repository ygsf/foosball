#!/usr/bin/env python
import time
import RPi.GPIO as GPIO

# choose BCM or BOARD numbering schemes.
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True) # TODO: might come in useful now.

# variables
GPIO_TRANSISTOR_FREQUENCY = 38000       # in herz, 38khz is specifically suited for the IR receiver. floats are also ok (100.5, 4.5, etc.).
GPIO_TRANSISTOR_DATA_CHANNEL = 18     	# transistor data channel for switching IR emitters on and off. Must be channel 18 (due to PWM)!
GPIO_YELLOW_CHANNEL = 7              	# GPIO channel for YELLOW team IR receiver. You can use any GPIO port.
GPIO_WHITE_CHANNEL = 14               	# GPIO channel for WHITE team IR receiver. You can use any GPIO port.
PWM_DUTY_CYCLE = 60                   	# duty cycle value can be 0.0 to 100.0%, floats are OK.
                                      	# basically 60% on and 40% off (same as in foos/plugins/io_raspberry.py).
                                      	# TODO: might need to increase duty cycle to generate a stronger signal.

# setup GPIO channels
GPIO.setup(GPIO_TRANSISTOR_DATA_CHANNEL, GPIO.OUT)     	# set GPIO channel with GPIO_TRANSISTOR_FREQUENCY as an output channel.
GPIO.setup(GPIO_YELLOW_CHANNEL, GPIO.IN)		# set GPIO channel with GPIO_YELLOW_CHANNEL as an input channel. TODO: Might need to add: pull_up_down=GPIO.PUD_UP
GPIO.setup(GPIO_WHITE_CHANNEL, GPIO.IN) 		#, pull_up_down=GPIO.PUD_UP)

def main():

    try:

        pwmsetup = GPIO.PWM(GPIO_TRANSISTOR_DATA_CHANNEL, GPIO_TRANSISTOR_FREQUENCY)
        pwmsetup.start(PWM_DUTY_CYCLE)

        time.sleep(1)
        
        while True:
           time.sleep(0.1)
           #print(GPIO.input(GPIO_YELLOW_CHANNEL))

           if (GPIO.input(GPIO_YELLOW_CHANNEL) == 0):
                print("Goal Yellow!")
                time.sleep(1)

           if (GPIO.input(GPIO_WHITE_CHANNEL) == 0):
                print("Goal White!")
                time.sleep(1)
           
    except Exception as exc:
        print(exc)

    finally:
        pwmsetup.stop() # stop PWM output
        GPIO.cleanup()  # this ensures a clean exit

main()
