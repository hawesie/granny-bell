# this is the original file from mrichardson23

import telnetlib # Needed to connect to FHEM server for sensor triggers
import os        # Needed to execute aplay to play the sounds

HOST = "localhost" # We'll connect to this computer
PORT = 7072        # on FHEM's default telnet port

tn = telnetlib.Telnet() # Create an instance of a telnet object
tn.open(HOST,PORT)      # Connect to the FHEM server on this machine

tn.write("inform on\n") # FHEM's command to spit out the data it gets

entranceSoundFile = None # Start in a state with no sound selected

while True:
	output = tn.read_until("\n")                 # When there's a carriage return from telnet, store the line that came in
	
	print output

	if "channel" in output:                      # For any button press, process it:
		os.system('aplay doorbell.wav &')        # Play the doorbell.wav
		if "A0" in output:                       # If it's the first button (search the telnet line for "A0" to find out)
			print "Button 1 Pressed."
			entranceSoundFile = "1.wav"          # Store the name of the sound file to play.
		if "AI" in output:
			print "Button 2 Pressed."            # And so on...
			entranceSoundFile = "2.wav"
		if "B0" in output:
			print "Button 3 Pressed."
			entranceSoundFile = "3.wav"
		if "BI" in output:
			print "Button 4 Pressed."
			entranceSoundFile = "4.wav"
	if "contact" in output:                       # If there's data from the contact switch
		if "open" in output:                      # If the contact switch has been opened
			print "Door opened."
			if entranceSoundFile is not None:                   # If there's an entrance sound file to play...
				print "I'll play: ", entranceSoundFile
				os.system('aplay ' + entranceSoundFile + ' &')  # ...then play that file
				entranceSoundFile = None                        # "Reset" the doorbell to no sound selected
			else:                                               # If the door opens again, no sound will play unless doorbell is pressed again.
				print "No doorbell selected."
