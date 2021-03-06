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

SCORE_CELL_YELLOW = 2
SCORE_CELL_WHITE = 3
SCORE_ROW = 2
                                        
def break_beam_callback(channel):
    if GPIO.input(GPIO_YELLOW_CHANNEL):
        print("Yellow Gool!")
        cellY = sheet.cell(SCORE_ROW, SCORE_CELL_YELLOW).value
        cellY = int(cellY) + 1
        sheet.update_cell(SCORE_ROW, SCORE_CELL_YELLOW, cellY)
        return None
    if GPIO.input(GPIO_WHITE_CHANNEL):
        print("White Gool!")
        cellW = sheet.cell(SCORE_ROW, SCORE_CELL_WHITE).value
        cellW = int(cellW) + 1
        sheet.update_cell(SCORE_ROW, SCORE_CELL_WHITE, cellW)
        return None
        
# setup GPIO channels
GPIO.setup(GPIO_YELLOW_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)        # set GPIO channel with GPIO_YELLOW_CHANNEL as an input channel.
GPIO.setup(GPIO_WHITE_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)        # set GPIO channel with GPIO_YELLOW_CHANNEL as an input channel.
#GPIO.setup(GPIO_WHITE_CHANNEL, GPIO.IN)         #, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(GPIO_YELLOW_CHANNEL, GPIO.FALLING, callback=break_beam_callback)  #RISING, FALLING or BOTH
GPIO.add_event_detect(GPIO_WHITE_CHANNEL, GPIO.FALLING, callback=break_beam_callback)  #RISING, FALLING or BOTH

message = input("press enter to quit\n\n")
GPIO.cleanup()
