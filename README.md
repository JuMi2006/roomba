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

There are 3 attributes wich can be used with the Roomba-Plugin:

<code>roomba_cmd = xxx</code>
Here you can use one of the following commands (clean, dock, power_off, spot, max) and the Roomba will do it.
You can also define a "driving scene": <code>roomba_cmd = backward | 2 | stop | 2 | clean</code>
Integers are sleep times in this moment. The above example drives 2 seconds backward, stops for 2 seconds and begins to clean.
There are the following commands available:
forward (100mm/s)
backward (100mm/s)
spin_left
spin_right
stop

<code>roomba_get = xxx</code>
Use the following item.conf to see how to configure the item for your wanted sensor. 
I think the names are self explaining.

<code>roomba_raw = [123]</code>
To send integers to Roomba following the documentation of Roomba SCI as List!

<pre>[roomba]
    [[command]]
        [[[clean]]]
            name = clean
            type = bool
            roomba_cmd = clean
        [[[dock]]]
            name = dock
            type = bool
            roomba_cmd = dock
        [[[power_off]]]
            name = power_off
            type = bool
            roomba_cmd = power_off
        [[[spot]]]
            name = spot
            type = bool
            roomba_cmd = spot
        [[[max]]]
            name = max
            type = bool
            roomba_cmd = max
            
    [[drive]]
        [[[out]]]
            #drives backward for 2 seconds, then spins left for 2 seconds, then drives forward for 3 seconds, then spins right for 3 seconds, then stops and starts to clean after 2 seconds
            name = test-drive
            type = bool
            roomba_cmd = backward | 2 | spin_left | 2 | forward | 3 | spin_right | 3 | stop | 2 | clean
            
    [[sensor]]
        [[[current]]]
            type = num
            roomba_get = current
        [[[temperature]]]
            type = num
            roomba_get = temperature
        [[[voltage]]]
            type = num
            roomba_get = voltage
        [[[button_clean]]]
            type = bool
            roomba_get = buttons_clean
        [[[capacity]]]
            type = num
            roomba_get = capacity
        [[[charge]]]
            type = num
            roomba_get = charge
        [[[temperature]]]
            type = num
            roomba_get = temperature    
        [[[current]]]
            type = num
            roomba_get = current        
        [[[voltage]]]
            type = num
            roomba_get = voltage    
        [[[charging_state]]]
            type = num
            roomba_get = charging_state
        [[[angle]]]
            type = num
            roomba_get = angle
        [[[distance]]]
            type = num
            roomba_get = distance
        [[[buttons_max]]]
            type = bool
            roomba_get = buttons_max
        [[[buttons_clean]]]
            type = bool
            roomba_get = buttons_clean
        [[[buttons_spot]]]
            type = bool
            roomba_get = buttons_spot
        [[[buttons_power]]]
            type = bool
            roomba_get = buttons_power
        [[[remote_opcode]]]
            type = num
            roomba_get = remote_opcode
        [[[dirt_detect_right]]]
            type = bool
            roomba_get = dirt_detect_right
        [[[dirt_detect_left]]]
            type = bool
            roomba_get = dirt_detect_left
        [[[motor_overcurrent_side_brush]]]
            type = bool
            roomba_get = motor_overcurrent_side_brush
        [[[motor_overcurrent_vacuum]]]
            type = bool
            roomba_get = motor_overcurrent_vacuum
        [[[motor_overcurrent_main_brush]]]
            type = bool
            roomba_get = motor_overcurrent_main_brush
        [[[motor_overcurrent_drive_left]]]
            type = bool
            roomba_get = motor_overcurrent_drive_left
        [[[virtual_wall]]]
            type = bool
            roomba_get = virtual_wall
        [[[cliff_right]]]
            type = bool
            roomba_get = cliff_right
        [[[cliff_front_right]]]
            type = bool
            roomba_get = cliff_front_right
        [[[cliff_front_left]]]
            type = bool
            roomba_get = cliff_front_left
        [[[cliff_left]]]
            type = bool
            roomba_get = cliff_left
        [[[wall]]]
            type = bool
            roomba_get = wall
        [[[bumps_wheeldrops_bump_right]]]
            type = bool
            roomba_get = bumps_wheeldrops_bump_right
        [[[bumps_wheeldrops_bump_left]]]
            type = bool
            roomba_get = bumps_wheeldrops_bump_left
        [[[bumps_wheeldrops_wheeldrop_right]]]
            type = bool
            roomba_get = bumps_wheeldrops_wheeldrop_right
        [[[bumps_wheeldrops_wheeldrop_left]]]
            type = bool
            roomba_get = bumps_wheeldrops_wheeldrop_left
        [[[bumps_wheeldrops_wheeldrop_caster]]]
            type = bool
            roomba_cmd = bumps_wheeldrops_wheeldrop_caster
</pre>

Good doocumentation to Roombas SCI: http://www.robotiklubi.ee/_media/kursused/roomba_sumo/failid/hacking_roomba.pdf
