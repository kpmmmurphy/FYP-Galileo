#!/usr/bin/env python

#Control center for Peripheral Sensing Node
#Author: Kevin Murphy
#Date  : 28 - Febuary - 15

import json
import pyupm_grove as grove
import pyupm_buzzer as upmBuzzer
import pyupm_ttp223 as ttp223

#Grove Pins
PIN_TEMP   = 0
PIN_LIGHT  = 1
PIN_BUZZER = 2
PIN_TOUCH  = 6

#Sensor Objects
temp   = None
light  = None
buzzer = None
touch  = None

#Buzzer Notes
chords = [upmBuzzer.DO, upmBuzzer.RE, upmBuzzer.MI, upmBuzzer.FA, 
          upmBuzzer.SOL, upmBuzzer.LA, upmBuzzer.SI, upmBuzzer.DO, 
          upmBuzzer.SI]

def main():
	createSensors()
	while True:
		print checkTouchPressed(touch)
		print readTemperature(temp)
		print readLightLevel(light)
		soundBuzzer(buzzer)

def createSensors():
	global temp, light, buzzer, touch

	print "Created Sensors ::"
	temp = grove.GroveTemp(PIN_TEMP)
	print temp.name()

	light = grove.GroveLight(PIN_LIGHT)
	print light.name()

	buzzer = upmBuzzer.Buzzer(PIN_BUZZER)
	print buzzer.name()

	touch = ttp223.TTP223(PIN_TOUCH)
	print touch.name()


def soundBuzzer(buzzer):
	global chords
	for chord_ind in range (0,7):
	    # play each note for one second
		buzzer.playSound(chords[chord_ind], 1000000)
		time.sleep(0.1)

def checkTouchPressed(touch):
	isPressed = False
	if touch.isPressed():
		print touch.name(), 'is pressed'
		isPressed = True
	return isPressed

def readTemperature(temp):
	return temp.value()

def readLightLevel(light):
	return light.value()

try:
    main()
except KeyboardInterrupt, SystemExit:
    print "KeyboardInterrupted..."
    del temp
    del light
    del touch
    del buzzer
