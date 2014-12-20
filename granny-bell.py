import telnetlib # Needed to connect to FHEM server for sensor triggers
import os        # Needed to execute aplay to play the sounds
import datetime
import signal
import sys

from pymongo import Connection
from threading import Timer

def button_pressed(output):
	return 'channel' in output and ('B0' in output or 'BI' in output)

def door_opened(output):
	return 'contact' in output and 'open' in output

def door_closed(output):
	return 'contact' in output and 'closed' in output

def log_event(event):
	print event
	event = {"event": event, "date": datetime.datetime.utcnow()}
	door_events.insert(event)


HOST = 'localhost' # We'll connect to this computer
PORT = 7072        # on FHEM's default telnet port

tn = telnetlib.Telnet() # Create an instance of a telnet object
tn.open(HOST,PORT)      # Connect to the FHEM server on this machine

tn.write('inform on\n') # FHEM's command to spit out the data it gets

entranceSoundFile = None # Start in a state with no sound selected

mongo_client = Connection('localhost', 27017)
door_events = mongo_client['granny-bell']['door_events']

# timers to manage 
bell_repeat_timer = None


# how long to wait
bell_repeat_delay_secs = 60

ring_allowed = True

def ring_bell():
	os.system('aplay doorbell.wav &')  
	log_event('bell_ring')

def ring_bell_with_repeat():
	ring_bell()
	global bell_repeat_timer
	bell_repeat_timer = Timer(bell_repeat_delay_secs, ring_bell_with_repeat)
	bell_repeat_timer.start()

def signal_handler(signal, frame): 
	cancel_timers()
	sys.exit(0)

def cancel_timers():
	global bell_repeat_timer

	if bell_repeat_timer is not None:
		bell_repeat_timer.cancel()
		bell_repeat_timer = None

signal.signal(signal.SIGINT, signal_handler)

while True:
	# When there's a carriage return from telnet, store the line that came in	
	output = tn.read_until('\n')                 

	if button_pressed(output):
		log_event('button_pressed')
		if ring_allowed:
			ring_bell_with_repeat()
			ring_allowed = False

	elif door_opened(output):
		log_event('door_opened')

	elif door_closed(output):
		log_event('door_closed')
		ring_allowed = True
		cancel_timers()

		


