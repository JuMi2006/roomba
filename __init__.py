#!/usr/bin/python

import serial
import time
import sys
import logging
import math
from struct import *
logger = logging.getLogger('Roomba')

cmd_dict=dict(
    power_off = 133,            #change2passive
    spot = 134,                 #change2passive
    clean = 135,                #change2passive
    max = 136,                  #change2passive
    stop = [137,0,0,0,0],
    forward = [137,0,100,128,0],
    backward = [137,255,156,128,0], 
    spin_left = [137,0,100,255,255],
    spin_right = [137,0,100,0,1],
    dock = 143,                 #change2passive
)

#support later
#    motors = 138,               #add 1 databyte
#    leds = 139,                 #add 3 databytes
#    song = 140,                 #add 2n + 2 databytes
#    play = 141,                 #add 1 databyte


class Roomba(object):
    _items = []
    
    def __init__(self,smarthome,tty,baudrate,cycle):
        self._sh = smarthome
        self.tty = tty
        self.baudrate = baudrate
        self.ser = serial.Serial(self.tty, baudrate=self.baudrate, timeout=2)
        self.is_connected = 'False'
        self._cycle = int(cycle)
        if self._cycle > 0:
            self._sh.scheduler.add('Roomba', self.get_sensors, prio=5, cycle=self._cycle, offset=2)      
    
    def run(self):
        pass
        
    def send(self, raw):
        if self.is_connected == 'False':
            try:
                self.connect()
            except:
                logger.error("Roomba: (Re)connect failed in send")
        if self.is_connected == 'True':
            if type(raw) is list:
                #print ("Send {0}".format(raw))
                logger.debug("Roomba: Send:{0}".format(raw))
                self.ser.write(bytearray(raw))
            else:
                #print ("Send [{0}]".format(raw))
                logger.debug("Roomba: Send:{0}".format([raw]))
                self.ser.write(bytearray([raw]))

    def connect(self):
        logger.debug("Roomba: Try to connect")
        try:
            self.ser.open()
            logger.debug("Roomba: Connected")
            self.is_connected = 'True'
            #self.send(128)  #start
            time.sleep(0.2)
            self.send(130)  #command
            time.sleep(0.2)
        except:
            logger.error("Roomba: Function connect failed")
            self.is_connected = 'False'
    
    def disconnect(self):
        self.ser.close()
        self.is_connected = 'False'
        logger.debug("Roomba: Disconnected")
    
    def parse_item(self, item):
        if 'roomba_cmd' in item.conf:
            cmd_string = item.conf['roomba_cmd']
            logger.debug("Roomba: {0} will send cmd \'{1}\'".format(item, cmd_string))
            self._items.append(item)
            return self.update_item
        if 'roomba_get' in item.conf:
            sensor_string = item.conf['roomba_get']
            logger.debug("Roomba: {0} will get \'{1}\'".format(item, sensor_string))
            self._items.append(item)
            return self.update_item      
        if 'roomba_drive' in item.conf:
            drive_string = item.conf['roomba_drive']
            logger.debug("Roomba: {0} will drive \'{1}\'".format(item, drive_string))
            self._items.append(item)
            return self.update_item
        if 'roomba_raw' in item.conf:
            raw_list = item.conf['roomba_raw']
            logger.debug("Roomba: {0} send raw \'{1}\'".format(item, raw_list))
            self._items.append(item)
            return self.update_item	
            
    def update_item(self, item, caller=None, source=None, dest=None):
        if caller != 'roomba':
            if item():
                if 'roomba_cmd' in item.conf:	
                    cmd_string = item.conf['roomba_cmd']
                    logger.debug("Roomba: item = true")
                    raw = cmd_dict[cmd_string]
                    if cmd_string in cmd_dict:
                        self.send(raw)
                if 'roomba_drive' in item.conf:
                    drive_string = item.conf['roomba_drive']
                    logger.debug("Roomba: item = true")
                    self.drive(drive_string)
                else:
                    pass
                self.disconnect()
       
    def drive(self,cmd_string):
        full_raw_cmd = []
        if type(cmd_string) is list:
            for i in cmd_string:
                try:
                    wait = float(i)
                    time.sleep(wait)
                    #print ('SLEEP {0}'.format(wait))
                except:
                    self.send(cmd_dict[i])
                    #print (cmd_dict[i])
        else:
            #print (cmd_dict[cmd_string])
            self.send(cmd_dict[cmd_string])
        self.disconnect()
        
    def raw(self,raw_cmd):
        pass
        
    def get_sensors(self):
        self.send([142,0])
        answer = self.ser.read(26)
        if len(answer) == 26:
            answer = list(answer)
            #print (answer)
            
            #create sensor_dict
            sensor_dict = {}
            sensor_dict = dict()
            
            #sensor_raw:
            _capacity = self.DecodeUnsignedShort(answer[25],answer[24]) #capacity
            sensor_dict['capacity']=_capacity
            
            _charge=self.DecodeUnsignedShort(answer[23],answer[22]) #charge
            sensor_dict['charge']=_charge
            
            _temperature = self.DecodeByte(answer[21]) #temperature
            sensor_dict['temperature']=_temperature
            
            _current=self.DecodeShort(answer[20],answer[19]) #current
            sensor_dict['current']=_current
            
            _voltage = self.DecodeUnsignedShort(answer[18],answer[17]) #voltage
            sensor_dict['voltage']=_voltage
            
            _charging_state = self.DecodeUnsignedByte(answer[16]) #charging state
            sensor_dict['charging_state']=_charging_state
            
            _angle = self.Angle(answer[15], answer[14], 'degrees') #angle
            sensor_dict['angle']=_angle
            
            _distance = self.DecodeShort(answer[13],answer[12]) #distance
            sensor_dict['distance']=_distance
            
            _buttons = list(self.Buttons(answer[11])) #Button
            sensor_dict['buttons_max']=_buttons[0]
            sensor_dict['buttons_clean']=_buttons[1]
            sensor_dict['buttons_spot']=_buttons[2]
            sensor_dict['buttons_power']=_buttons[3]
            
            _remote_opcode = self.DecodeUnsignedByte(answer[10]) #remote_opcode
            sensor_dict['remote_opcode']=_remote_opcode
            
            _dirt_detect_right = self.DecodeUnsignedByte(answer[9]) #dirt detect right
            sensor_dict['dirt_detect_right']=_dirt_detect_right
            
            _dirt_detect_left = self.DecodeUnsignedByte(answer[8]) #dirt detect left
            sensor_dict['dirt_detect_left']=_dirt_detect_left
            
            _motor_overcurrent = self.MotorOvercurrents(answer[7]) #motor overcurrent
            sensor_dict['motor_overcurrent_side_brush']=_motor_overcurrent[0]
            sensor_dict['motor_overcurrent_vacuum']=_motor_overcurrent[1]
            sensor_dict['motor_overcurrent_main_brush']=_motor_overcurrent[2]
            sensor_dict['motor_overcurrent_drive_right']=_motor_overcurrent[3]        
            sensor_dict['motor_overcurrent_drive_left']=_motor_overcurrent[3] 
            
            _virtual_wall = answer[6]
            sensor_dict['virtual_wall']=_virtual_wall
            
            _cliff_right = answer[5]
            sensor_dict['cliff_right']=_cliff_right
            
            _cliff_front_right = answer[4]
            sensor_dict['cliff_front_right']=_cliff_front_right
            
            _cliff_front_left = answer[3]
            sensor_dict['cliff_front_left']=_cliff_front_left
            
            _cliff_left = answer[2]
            sensor_dict['cliff_left']=_cliff_left
            
            _wall = answer[1]
            sensor_dict['wall']=_wall
            
            _bumps_wheeldrops = self.BumpsWheeldrops(answer[0])
            sensor_dict['bumps_wheeldrops_bump_right']=_bumps_wheeldrops[0]
            sensor_dict['bumps_wheeldrops_bump_left']=_bumps_wheeldrops[1]
            sensor_dict['bumps_wheeldrops_wheeldrop_right']=_bumps_wheeldrops[2]
            sensor_dict['bumps_wheeldrops_wheeldrop_left']=_bumps_wheeldrops[3]
            sensor_dict['bumps_wheeldrops_wheeldrop_caster']=_bumps_wheeldrops[4]
            
            for item in self._items:
                if 'roomba_get' in item.conf:
                    sensor = item.conf['roomba_get']
                    if sensor in sensor_dict:
                        value = sensor_dict[sensor]
                        item(value, 'Roomba', 'get_sensors')
                        #print ("SENSOR: {0}  VALUE: {1}".format(sensor,value))
        else:
            logger.error("Roomba: Sensors not readable")
        self.disconnect()
        
    def dec2hex(self,num):
        num = int(num)
        return (str('0x' + '%.2x' % num))

    def DecodeUnsignedShort(self, low, high):
        bytearr = bytearray([high,low])
        value = unpack('>H', bytearr)
        return (value[0])
        
    def DecodeByte(self,byte):
        bytearr = bytearray([byte])
        value = unpack('b', bytearr)
        return (value[0])
        
    def DecodeShort(self, low, high):
        bytearr = bytearray([high,low])
        value = unpack('>h', bytearr)
        return (value[0])
    
    def DecodeUnsignedByte(self, byte):
        bytearr = bytearray([byte])
        value = unpack('B', bytearr)
        return (value[0])
    
    def Angle(self, low, high, unit=None):
        #Angle in radians = (2 * difference) / 258
        #Angle in degrees = (360 * difference) / (258 * Pi).
        if unit not in (None, 'radians', 'degrees'):
            pass
        angle = self.DecodeShort(low, high)
        if unit == 'radians':
            angle = (2 * angle) / 258
            #print ("{0} radians".format(angle))
            return angle
        if unit == 'degrees':
            angle /= math.pi
            #print ("{0} degrees".format(angle))
            return angle
    
    def Buttons(self, byte):
        bytearr = bytearray([byte])
        byte = unpack('B', bytearr)
        byte = byte[0]
        return (byte & 1, byte & 2, byte & 3, byte & 4)
        #returns max,clean,spot,power
    
    def MotorOvercurrents(self, byte):
        bytearr = bytearray([byte])
        byte = unpack('B', bytearr)
        byte = byte[0]
        return (byte & 1, byte & 2, byte & 3, byte & 4, byte & 5)
        #returns side-brush,vacuum,main-brush,drive-right,drive-left
    
    def BumpsWheeldrops(self, byte):
        bytearr = bytearray([byte])
        byte = unpack('B', bytearr)
        byte = byte[0]
        return (byte & 1, byte & 2, byte & 3, byte & 4, byte & 5)
        #returns bump-right,bump-left,wheel-drop-right,wheel-drop-left,wheel-drop-caster
