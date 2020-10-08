#!/usr/bin/env python
import time
import RPi.GPIO as GPIO

import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("foosballsh").sheet1


# choose BCM or BOARD numbering schemes.
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True) # TODO: might come in useful now.

# variables
GPIO_YELLOW_CHANNEL = 17                # GPIO channel for YELLOW team IR receiver. You can use any GPIO port.
GPIO_WHITE_CHANNEL = 18                 # GPIO channel for WHITE team IR receiver. You can use any GPIO port.
                                        
def break_beam_callback(channel):
    if GPIO.input(GPIO_YELLOW_CHANNEL):
        print("Yellow Gool!")
        cell = sheet.cell(2,2).value
        print(cell)
        cell = int(cell) + 1
        print(cell)
        sheet.update_cell(2,2,cell)
        return None
    if GPIO.input(GPIO_WHITE_CHANNEL):
        print("White Gool!")
        sheet.update_cell(2,3,"4")
        return None
        
# setup GPIO channels
GPIO.setup(GPIO_YELLOW_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)        # set GPIO channel with GPIO_YELLOW_CHANNEL as an input channel.
GPIO.setup(GPIO_WHITE_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)        # set GPIO channel with GPIO_YELLOW_CHANNEL as an input channel.
#GPIO.setup(GPIO_WHITE_CHANNEL, GPIO.IN)         #, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(GPIO_YELLOW_CHANNEL, GPIO.FALLING, callback=break_beam_callback)  #RISING, FALLING or BOTH
GPIO.add_event_detect(GPIO_WHITE_CHANNEL, GPIO.FALLING, callback=break_beam_callback)  #RISING, FALLING or BOTH

message = input("press enter to quit\n\n")
GPIO.cleanup()
