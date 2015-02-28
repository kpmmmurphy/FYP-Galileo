#!/usr/bin/env python

#Control center for Peripheral Sensing Node
#Author: Kevin Murphy
#Date  : 28 - Febuary - 15

import json
import pyupm_grove as grove
import pyupm_buzzer as upmBuzzer
import pyupm_ttp223 as ttp223

#Grove Pins
PIN_LIGHT  = 4
PIN_TEMP   = 3
PIN_BUZZER = 2
PIN_TOUCH  = 6

#Buzzer Notes
chords = [upmBuzzer.DO, upmBuzzer.RE, upmBuzzer.MI, upmBuzzer.FA, 
          upmBuzzer.SOL, upmBuzzer.LA, upmBuzzer.SI, upmBuzzer.DO, 
          upmBuzzer.SI];

def main():
	createSensors()
	while True:
		print checkTouchPressed(touch)
		print readTemperature(temp)
		print readLightLevel(light)
		soundBuzzer(buzzer)

def createSensors():
	print "Created Sensors ::"
	temp = grove.GroveTemp(PIN_TEMP)
	print temp.name()

	light = grove.GroveLight(PIN_LIGHT)
	print light.name()

	buzzer = upmBuzzer.Buzzer(PIN_BUZZER)
	print buzzer.name()

	touch = ttp223.TTP223(touch)
	print touch.name()


def soundBuzzer(buzzer):
	for chord_ind in range (0,7):
	    # play each note for one second
	    print buzzer.playSound(chords[chord_ind], 1000000)
	    time.sleep(0.1)

def checkTouchPressed(touch):
	isPressed = False
	if touch.isPressed():
		print touch.name(), 'is pressed'
		isPressed = True
	return isPressed

def readTemperature(temp):
	return celsius = temp.value()

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
