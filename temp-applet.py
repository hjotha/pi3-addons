#!/usr/bin/python

import os
import time
import signal
import RPi.GPIO as GPIO

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from gi.repository import GObject as gobject

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

# constants
FAN_PIN = 15
MAX_TEMPERATURE = 60
TEMPERATURE_UPDATE_TIMEOUT = 4000
TEMPERATURE_COOLING_TIMEOUT = 60000

APPINDICATOR_ID = 'temp-applet'

COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

#global vars
indicator = 0
last_temp = 0

def get_temperature():
    res = os.popen('vcgencmd measure_temp').readline()
    temp =(res.replace("temp=","").replace("'C\n",""))
    return temp

def fan_on():
	return GPIO.output(FAN_PIN, GPIO.HIGH)
	
def fan_off():
	return GPIO.output(FAN_PIN, GPIO.LOW)

def update_fan():
	
	temp = get_temperature()

	if float(temp) >= MAX_TEMPERATURE:
		fan_on()
		gobject.timeout_add(TEMPERATURE_COOLING_TIMEOUT, update_fan)
	else:
		fan_off()
		gobject.timeout_add(TEMPERATURE_UPDATE_TIMEOUT, update_fan)
	
	return False
	
def update_temperature():

	global indicator, last_temp

	temp = get_temperature()
	tempf = int(float(temp))
	
	if tempf != last_temp:
		last_temp = temp
		if tempf >= MAX_TEMPERATURE:
			image = create_indicator_image( temp, COLOR_RED )
		else:
			image = create_indicator_image( temp, COLOR_GREEN )
			
		indicator.set_icon_full( image, temp )
		
	return True

def create_indicator_image( temp, color ):

	#create image
	img = Image.new('RGB', (18, 18))
	
	#fill background
	img.paste( (60,59,55), [0,0,img.size[0],img.size[1]])

	font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 15)
	draw = ImageDraw.Draw(img)
	
	draw.text((0, 2), temp, color, font=font)

	image = os.path.abspath('temp.png')
	img.save( image )

	return image

def create_indicator(image):
	indicator = appindicator.Indicator.new(APPINDICATOR_ID, image, appindicator.IndicatorCategory.SYSTEM_SERVICES)
	indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
	return indicator

def build_menu():
    menu = gtk.Menu()
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def quit(_):
	fan_off()
	GPIO.cleanup()
	notify.uninit()
	gtk.main_quit()
	return
	
try:
	# low priority
	os.nice(1)    
	
	# allow ctrl+c
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	
	# configure gpio
	GPIO.setwarnings(False)	
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(FAN_PIN, GPIO.OUT)
	fan_off()

	# create ui
	image = create_indicator_image(get_temperature(), COLOR_BLUE)
	indicator = create_indicator(image)
	indicator.set_menu(build_menu())
	
	# notify desktop
	notify.init(APPINDICATOR_ID)

	# temperature check timer
	gobject.timeout_add(TEMPERATURE_UPDATE_TIMEOUT, update_temperature)
	gobject.timeout_add(TEMPERATURE_UPDATE_TIMEOUT, update_fan)
	
	# init gtk
	gtk.main()

except KeyboardInterrupt:
	quit(_)
