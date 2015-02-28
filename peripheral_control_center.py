#!/usr/bin/env python

#Control center for Peripheral Sensing Node
#Author: Kevin Murphy
#Date  : 28 - Febuary - 15

import json
import time
import pyupm_grove as grove
import pyupm_buzzer as upmBuzzer
import pyupm_ttp223 as ttp223

#Grove Pins
PIN_TEMP   = 0
PIN_LIGHT  = 1
PIN_LED    = 2
PIN_BUZZER = 3
PIN_TOUCH  = 4

#Sensor Objects
temp   = None
light  = None
buzzer = None
touch  = None
led    = None

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
		flashLed(led)

def createSensors():
	global temp, light, buzzer, touch, led

	print "Created Sensors ::"
	temp = grove.GroveTemp(PIN_TEMP)
	print temp.name()

	light = grove.GroveLight(PIN_LIGHT)
	print light.name()

	buzzer = upmBuzzer.Buzzer(PIN_BUZZER)
	print buzzer.name()

	touch = ttp223.TTP223(PIN_TOUCH)
	print touch.name()

	led = grove.GroveLed(PIN_LED)
	print led.name()

def soundBuzzer(buzzer):
	global chords
	buzzer.playSound(chords[0], 1000000)

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

def flashLed(led):
	led.on()
	time.sleep(1)
	led.off()
	time.sleep(1)

try:
    main()
except KeyboardInterrupt, SystemExit:
    print "KeyboardInterrupted..."
    del temp
    del light
    del touch
    del buzzer
    del led
