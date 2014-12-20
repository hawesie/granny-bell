import telnetlib # Needed to connect to FHEM server for sensor triggers
import os        # Needed to execute aplay to play the sounds
import datetime
from pymongo import Connection

HOST = 'localhost' # We'll connect to this computer
PORT = 7072        # on FHEM's default telnet port

tn = telnetlib.Telnet() # Create an instance of a telnet object
tn.open(HOST,PORT)      # Connect to the FHEM server on this machine

tn.write('inform on\n') # FHEM's command to spit out the data it gets

entranceSoundFile = None # Start in a state with no sound selected

mongo_client = Connection('localhost', 27017)
door_events = mongo_client['granny-bell']['door_events']


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

def ring_bell():
	print 'ding dong'

ring_allowed = True

while True:
	# When there's a carriage return from telnet, store the line that came in	
	output = tn.read_until('\n')                 


	if button_pressed(output):
		log_event('button_pressed')
		if ring_allowed:
			ring_bell()
			ring_allowed = False

	elif door_opened(output):
		log_event('door_opened')

	elif door_closed(output):
		log_event('door_closed')
		ring_allowed = True



