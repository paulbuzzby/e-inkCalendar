import sys
import os


import logging
import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback


fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Fonts')
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
testpic = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'calendar.png')

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("Paul's Demo")

    font24 = ImageFont.truetype(os.path.join(fontdir, 'OpenSans-Regular.ttf'), 24)
    font18 = ImageFont.truetype(os.path.join(fontdir, 'OpenSans-Regular.ttf'), 18)


    epd = epd7in5_V2.EPD()
    
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    im = Image.open(testpic) 

    epd.display(epd.getbuffer(im))
    

    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()