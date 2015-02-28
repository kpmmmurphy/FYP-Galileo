#!/usr/bin/env python

#Control center for Peripheral Sensing Node
#Author: Kevin Murphy
#Date  : 28 - Febuary - 15

import json
import time
import datetime
import socket
import struct
from uuid import getnode as get_mac
import threading 
import pyupm_grove as grove
import pyupm_buzzer as upmBuzzer
import pyupm_ttp223 as ttp223

#Grove Pins
PIN_TEMP   = 0
PIN_LIGHT  = 1
PIN_LED    = 2
PIN_BUZZER = 3
PIN_TOUCH  = 4

#Sensor Names
SENSOR_TEMP  = "temperature"
SENSOR_LIGHT = "light"
SENSOR_TOUCH = "touch"

#Sensor Objects
temp   = None
light  = None
buzzer = None
touch  = None
led    = None

#SOCKET
MULTICAST_GRP  = '224.1.1.1'
MULTICAST_PORT = 5007
DEFAULT_PORT   = 5006
DEFAULT_SERVER_PORT = 5005

#Session Keys
SESSION_IP        = "ip_address"
SESSION_TIMESTAMP = "timestamp"
SESSION_DEVICE_ID = "device_id" 
SESSION_TYPE      = "type"

#Buzzer Notes
chords = [upmBuzzer.DO, upmBuzzer.RE, upmBuzzer.MI, upmBuzzer.FA, 
          upmBuzzer.SOL, upmBuzzer.LA, upmBuzzer.SI, upmBuzzer.DO, 
          upmBuzzer.SI]

def main():
	global MULTICAST_GRP, MULTICAST_PORT
	session = createSession()
	sensorReadings = {}
	createSensors()
	multicastSocket = createMulticatSocket(session[SESSION_IP], MULTICAST_GRP, MULTICAST_PORT)
	while True:
		sensorReadings[SENSOR_TOUCH] = checkTouchPressed(touch)
		sensorReadings[SENSOR_TEMP]  = readTemperature(temp)
		sensorReadings[SENSOR_LIGHT] = readLightLevel(light)
		print json.dumps(sensorReadings)

#SOCKET STUFF
def createSession():
	global SESSION_IP, SESSION_TIMESTAMP, SESSION_DEVICE_ID, SESSION_TYPE
	timestamp   = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	ipAddress   = getIPAddress()
	mac_address = get_mac()
	sess = { SESSION_IP: ipAddress, SESSION_DEVICE_ID : mac_address, SESSION_TIMESTAMP : timestamp, SESSION_TYPE : "peripheral" } 
	json.dumps(sess)
	return sess

def getIPAddress():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	#TODO This should be changed when connecting to PI!!!!!!!!!!!!!!!!!!!!!!
	s.connect(("gmail.com",80))
	return s.getsockname()[0]

def createSocket(bindToIP, connectToIP):
	newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	newSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	newSocket.setblocking(True)

	if bindToIP is not None:
		#For receiving 
		newSocket.bind((bindToIP, CONSTS.DEFAULT_SERVER_PORT))
		newSocket.listen(5)
	elif connectToIP is not None:
		#For sending
		#newSocket.bind((self.__ipAddress, CONSTS.DEFAULT_PORT))
		newSocket.connect((connectToIP, CONSTS.DEFAULT_PORT))

	return newSocket

def createMulticatSocket(inetIP, multicastGroup, multicastPort):
	multicastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	multicastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#Socket must be connected to the wlan0 interface's IP address
	#Bind to our default Multicast Port.
	multicastSocket.bind((multicastGroup, multicastPort))
	#multicastSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicastGroup)+socket.inet_aton(inetIP))
	mreq = struct.pack("4sl", socket.inet_aton(multicastGroup), socket.INADDR_ANY)
	multicastSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
	multicastSocket.setblocking(True)	
	return multicastSocket


#SENSORS----------------------
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
