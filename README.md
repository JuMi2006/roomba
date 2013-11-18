Roomba
====

plugin.conf
<pre>
[roomba]
     class_name = Roomba
     class_path = plugins.roomba
     tty = /dev/rfcomm1
     baudrate = 57600
	   cycle = 0 #0=deactivate reading sensors
</pre>


item.conf:
<pre>
[roomba]
	[[command]]
		[clean]
			name = clean
			type = bool
			roomba_cmd = clean
		[dock]
			name = dock
			type = bool
			roomba_cmd = dock
		[power_off]
			name = power_off
			type = bool
			roomba_cmd = power_off
		[spot]
			name = spot
			type = bool
			roomba_cmd = spot
		[max]
			name = max
			type = bool
			roomba_cmd = max
				
		[drive]
			type = num
			#add 4 databytes
		[motors]
			type = num
			#add 1 databyte
		[leds]
			type = num
			#add 3 databytes
		[song]
			type = num
			#add 2n + 2 databytes
		[play]
			type = num
			#add 1 databyte
			
	[[drive]]
		[out]
			#drives backward for 2 seconds, then spins left for 2 seconds, then drives forward for 3 seconds, then spins right for 3 seconds, then stops and starts to clean
			name = out_of_the_box
			type = bool
			roomba_drive = backward | 2 | spin_left | 2 | forward | 3 | spin_right | 3 | stop | clean
			
	[[sensor]]
		[current]
			type = num
			roomba_get = current
		
		[temperature]
			type = num
			roomba_get = temperature
		
		[voltage]
			type = num
			roomba_get = voltage
		
		[button_clean]
			type = bool
			roomba_get = buttons_clean
</pre>
