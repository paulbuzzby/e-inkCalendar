#!/usr/bin/env python
# mocks.py: Mock objects for low-level peripheral/hardware-related modules

''' To-Do:
 - add iterable support channels passed to GPIO
 - add GPIO pull-up/pull-down support
 - add event detection support
'''


__author__ = 'Trevor Allen'

# Standard Library
import random
import time
import math

## RPi.GPIO pins (from http://elinux.org/RPi_Low-level_peripherals):
'''
    RPi A+ & B+ GPIO: J8 40-pin header
    --------------------------------
            +3V3 1  2   +5V
    GPIO2   SDA1 3  4   +5V
    GPIO3   SCL1 5  6   GND
    GPIO4   GCLK 7  8   TXD0  GPIO14
             GND 9  10  RXD0  GPIO15
    GPIO17  GEN0 11 12  GEN1  GPIO18
    GPIO27  GEN2 13 14  GND
    GPIO22  GEN3 15 16  GEN4  GPIO23
            +3V3 17 18  GEN5  GPIO24
    GPIO10  MOSI 19 20  GND
    GPIO9   MISO 21 22  GEN6  GPIO25
    GPIO11  SCLK 23 24  CE0_N GPIO8
             GND 25 26  CE1_N GPIO7
    EEPROM ID_SD 27 28  ID_SC EEPROM
    GPIO5        29 30  GND
    GPIO6        31 32        GPIO12
    GPIO13       33 34  GND
    GPIO19       35 36        GPIO16
    GPIO26       37 38        GPIO20
             GND 39 40        GPIO21
    --------------------------------
    '''


class MockSMBus(object):
    ''' Mock of smbus.SMBus() class '''
    mpu_adr = 0x68
    lcd_adr = 0x27
    pwr_mgt_1 = 0x6b
    ## HIGH byte registers for MPU-6050, value+1 for LOW registers
    accel_x = 0x3b
    accel_y = 0x3d
    accel_z = 0x3f
    gyro_x = 0x43
    gyro_y = 0x45
    gyro_z = 0x47
    temp = 0x41

    def __init__(self, bus_no):
        self.bus_no = bus_no

    def __repr__(self):
        return "<Mock: smbus.SMBus>"

    def write_byte(self, addr, cmd):
        if addr not in (self.mpu_adr, self.lcd_adr):
            errmsg = 'Address argument not valid: %s' % hex(addr)
            raise ValueError(errmsg)
        return None

    def write_byte_data(self, addr, cmd, zero=0):
        ''' orig: sensor.Sensor.initialize() '''
        # res = bus.write_byte_data(0x68, 0x6b, 0)  # res = None
        if addr not in (self.mpu_adr, self.lcd_adr):
            errmsg = 'Address argument not valid: %s' % hex(addr)
            raise ValueError(errmsg)
        ## This is specific to MPU
        if cmd not in (self.mpu_adr, self.lcd_adr, self.pwr_mgt_1, self.accel_x, self.accel_y,
                    self.accel_z, self.gyro_x, self.gyro_y, self.gyro_z, self.temp):
            raise ValueError('Command invalid: %s' % hex(cmd))
        return None

    def write_block_data(self, addr, cmd, data):
        # I don't think this is actually used, just available in lcd_device.py
        if addr not in (self.mpu_adr, self.lcd_adr):
            errmsg = 'Address argument not valid: %s' % hex(addr)
            raise ValueError(errmsg)
        return None

    def read_byte_data(self, addr, cmd):
        ''' orig: sensor.Sensor.read_word() '''
        # addr is mpu-addr (0x68); cmd is HIGH register: accel-x (0x3b), accel-y (0x3d),
        # accel-z (0x3f), gyro-x (0x43), gyro-y (0x45), gyro-z (0x47), temp (0x41)
        results = { self.accel_x : 246, self.accel_x+1 : 88,
                    self.accel_y : 4, self.accel_y+1 : 92,
                    self.accel_z : 57, self.accel_z+1 : 104,
                    self.gyro_x : 6, self.gyro_x+1 : 42,
                    self.gyro_y : 0, self.gyro_y+1 : 184,
                    self.gyro_z : 255, self.gyro_z+1 : 216,
                    self.temp : 240, self.temp+1 : 16,
                    self.lcd_adr : 0
                    }
        if addr not in (self.mpu_adr, self.lcd_adr):
            errmsg = 'Address argument not valid: %s' % hex(addr)
            raise ValueError(errmsg)
        ## This is specific to MPU
        ### Checking commands restricts to MPU, disallows LCD display,
        #   unless one were to add all the LCD attributes below to this class
        if cmd not in results.keys():
            raise ValueError('Argument %s not a valid command.' % hex(cmd))
        try:
            return results[cmd]
        except KeyError:
            return None

    def read_byte(self, addr):
        # I don't think this is actually used, just available in lcd_device.py
        if addr not in (self.mpu_adr, self.lcd_adr):
            errmsg = 'Address argument not valid: %s' % hex(addr)
            raise ValueError(errmsg)
        return None

    def read_block_data(self, addr, cmd):
        # I don't think this is actually used, just available in lcd_device.py
        if addr not in (self.mpu_adr, self.lcd_adr):
            errmsg = 'Address argument not valid: %s' % hex(addr)
            raise ValueError(errmsg)
        return None



class Mock_smbusModule(object):
    ''' Mock of smbus module, containing SMBus class '''
    ### Purpose here is to allow instantiation of a fake smbus 'library'
    #   like so: smbus = Mock_smbusModule(); bus = smbus.SMBus(1)
    SMBus = MockSMBus


class MockGPIO(object):
    # Map format is <BCM-#> : <BOARD-#>
    bcm_board_map = { 2 : 3,
      3 : 5,   4 : 7,   14 : 8,  15 : 10, 17 : 11,
     18 : 12, 27 : 13,  22 : 15, 23 : 16, 24 : 18,
     10 : 19,  9 : 21,  25 : 22, 11 : 23,  8 : 24,
      7 : 26,  5 : 29,   6 : 31, 12 : 32, 13 : 33,
     19 : 35, 16 : 36,  26 : 37, 20 : 38, 21 : 40}
    RPI_REVISION = 2
    BCM = 11
    BOARD = 10
    OUT = 0
    IN = 1
    LOW = 0
    HIGH = 1
    PUD_OFF = 20
    PUD_DOWN = 21
    PUD_UP = 22
    HARD_PWM = 43
    FALLING = 32
    BOTH = 33
    I2C = 42
    RISING = 31
    SERIAL = 40
    SPI = 41
    UNKNOWN = -1
    VERSION = '0.5.11'
    RPI_INFO = {'MANUFACTURER': 'Unknown', 'P1_REVISION': 3, 'PROCESSOR': 'Unknown',
                'RAM': 'Unknown', 'REVISION': '0010', 'TYPE': 'Unknown'}

    gpio_setting = { k:1 for k in bcm_board_map.keys() }

    def __init__(self):
        self.mode = -1
        self.setmode_run = False
        self.setup_run = False
        pass

    def __repr__(self):
        return "<Mock: RPi.GPIO>"

    def setmode(self, mode):
        # mode should be GPIO.BCM or GPIO.BOARD
        if mode not in (self.BCM, self.BOARD):
            raise ValueError('An invalid mode was passed to setmode()')
        self.setmode_run = True
        self.mode = mode
        # Returns nothing
        pass

    def getmode(self):
        # Should return BCM, BOARD, or UNKNOWN
        return self.mode

    def _pin_validate(self, channel):
        ''' For test/mock purposes, to centralize validation checks of pin numbers & values '''
        if channel not in self.bcm_board_map.keys():
            raise ValueError('Channel is invalid on a Raspberry Pi: %s' % str(channel))

    def cleanup(self, channels=None):
        # Resets all to INPUT with no pullup/pulldown and no event detection
        if channels is None:
            channels = self.bcm_board_map.keys()
        elif not hasattr(channels, '__iter__'):
            channels = [channels,]
        for pin in channels:
            self.gpio_setting[pin] = 1
        self.mode = -1
        self.setmode_run = False

    def setup(self, channels, direction, pull_up_down=None, initial=None):
        if not hasattr(channels, '__iter__'):
            channels = [channels, ]
        for channel in channels:
            self._pin_validate(channel)

        if direction not in (self.IN, self.OUT):
            raise ValueError('An invalid direction was passed to setup()')
        if (pull_up_down is not None and
            pull_up_down not in (self.PUD_OFF, self.PUD_UP, self.PUD_DOWN) ):
            raise ValueError('pull_up_down not in pre-defined PUD_OFF/UP/DOWN values')
        self.setup_run = True  # really should do this on a per-channel basis
        self.gpio_setting[channel] = direction
        # Returns nothing
        pass

    def output(self, channel, value):
        if not hasattr(channels, '__iter__'):
            channels = [channels, ]
        for channel in channels:
            self._pin_validate(channel)

        if value not in (self.LOW, self.HIGH):
            raise ValueError('An invalid value was passed to output()')
        if not self.setmode_run:
            raise RuntimeError('Please set pin numbering mode using GPIO.setmode(GPIO.BOARD) or GPIO.setmode(GPIO.BCM)')
        if not self.setup_run:
            raise RuntimeError('The GPIO channel has not been set up as an OUTPUT')
        # Returns nothing
        pass

    def input(self, channels):
        if not hasattr(channels, '__iter__'):
            channels = [channels, ]
        for channel in channels:
            self._pin_validate(channel)

        if not self.setmode_run:
            raise RuntimeError('Please set pin numbering mode using GPIO.setmode(GPIO.BOARD) or GPIO.setmode(GPIO.BCM)')
        if not self.setup_run:
            raise RuntimeError('You must setup() the GPIO channel first')
        # Returns either 0 or 1.
        ### This may need to be customized depending on its intended use, perhaps
        #   by using mock to specify the desired return value in tests. For me
        #   leaving it to return 1 works fine.
        return self.HIGH

    def gpio_function(self, channel):
        self._pin_validate(channel)
        if not self.setmode_run:
            raise RuntimeError('Please set pin numbering mode using GPIO.setmode(GPIO.BOARD) or GPIO.setmode(GPIO.BCM)')
        return  self.gpio_setting[channel]


    ## Following functions are placeholders that need filled it.
    def add_event_callback(self, *args):
        pass

    def add_event_detect(self, *args):
        pass

    def setwarnings(self, *args):
        pass

    def wait_for_edge(self, *args):
        pass

    def event_detected(self, *args):
        pass

    def remove_event_detect(self, *args):
        pass


class MockSPI(object):
    ''' Mock of spi module '''
    ### Designed for use with MFRC522 rfid module by mxgxw, available on GitHub:
    #   https://github.com/mxgxw/MFRC522-python

    spi_reg_names = {
        # Attr name : [register, (spi.xver results)]
        'CRCResultRegM' : [0x21, (0, 255)],
        'CRCResultRegL' : [0x22, (0, 255)],
        'ErrorReg' : [0x06, (0,0)],
        'ControlReg' : [0x0C, (0,16)],
        'TxControlReg' : [0x14, (0,128)],
        'Status2Reg' : [0x08, (0,0)],
        'DivIrqReg' : [0x05, (0,0)],
        'FIFOLevelReg' : [0x0A, (0,0)],
        'CommIrqReg' : [0x04, (0,20)],
        'BitFramingReg' : [0x0D, (0,0)]
    }


    # Attr : [register]
    spi_write_names = {
        'BitFramingReg' : 0x0D,
        'CommandReg' : 0x01,
        'PCD_RESETPHASE' : 0x0F,
        'PCD_CALCCRC' : 0x03,
        'PCD_IDLE' : 0x00,
        'PCD_TRANSCEIVE' : 0x0C,
        'PCD_AUTHENT' : 0x0E,
        'CommIEnReg' : 0x02,
        'ModeReg' : 0x11,
        'TModeReg' : 0x2A,
        'TxAutoReg' : 0x15,
        'TPrescalerReg' : 0x2B,
        'TReloadRegL' : 0x2D,
        'TReloadRegH' : 0x2C
    }



    '''  Need to figure out how to fake these functions from mfrc522.py:

    def CalculateCRC(self, pIndata):
        i = 0
        while i<len(pIndata):
          self.Write_MFRC522(self.FIFODataReg, pIndata[i])
          i = i + 1

    def MFRC522_ToCard(self,command,sendData):
        while(i<len(sendData)):
            self.Write_MFRC522(self.FIFODataReg, sendData[i])
            i = i+1
            self.Write_MFRC522(self.FIFODataReg, sendData[i])
    '''
    def __init__(self):
        raise UserWarning('This mock spi class is not entirely operational yet.')
        self.spi_xfer_vals = {
            0x21 : (0, 255),
            0x22 : (0, 255),
            0x06 : (0,0),
            0x0C : (0,16),
            0x14 : (0,128),
            0x08 : (0,0),
            0x05 : (0,0),
            0x0A : (0,0),
            0x04 : (0,20),
            0x0D : (0,0)
        }
        # Writable Register : Val(s)
        self.spi_write_vals = {
            0x0D : [0x00, 0x07],  # BitFramingReg
            0x01 : [0x0F, 0x03, 0x00, 0x0C, 0x0E],  # CommandReg
            0x02 : [0x00, 0x12, 0x77, 0x80],  # CommIEnReg
            0x11 : [0x3D],  # ModeReg
            0x2A : [0x8D],  # TModeReg
            0x15 : [0x40],  # TxAutoReg
            0x2B : [0x3E],  # TPrescalerReg
            0x2D : [30],  # TReloadRegL
            0x2C : [0],  # TReloadRegH
            0x80 : [0],  # Fallback/Default
            # These following 'masks' may need to be included as "val"s
            #   for all writable registers: 0x03, 0x80, 0x04, 0x08
        }
    def openSPI(self, device='/dev/spidev0.0', speed=1000000):
        # spi.transfer(((addr<<1)&0x7E,val))
        pass

    def closeSPI(self):
        pass

    def transfer(self, stuffs):
        # self.spi.transfer(((addr<<1)&0x7E,val))
        addr, val = stuffs
        ## A very poor attempt to mimic MFRC522's read/write functions:
        if ( (addr not in self.spi_xfer_vals.keys())
            and (addr not in self.spi_write_vals.keys()) ):
            raise KeyError('Addr invalid: %s' % str(addr))
        legit_value = any( [val in vals for vals in self.spi_write_vals.values()] )
        if not legit_value:
            raise ValueError('Value invalid: %s' % hex(val))
        try:
            res = self.spi_xfer_vals[addr]
        except KeyError:
            res = self.spi_write_vals[addr]
        return res

