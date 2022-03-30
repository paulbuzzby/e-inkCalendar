from datetime import datetime
from datetime import timedelta 
import json
import logging
import sys

from ImageCreator import *
from iCalendarHelper import *
import epd7in5_V2
from power import PowerHelper

#Battery Display
#Error information if occurs


def main() :
        
    # Create and configure logger
    logging.basicConfig(filename="logfile.log", format='%(asctime)s %(levelname)s - %(message)s', filemode='a')
    logger = logging.getLogger('eInkCalendar')
    logger.addHandler(logging.StreamHandler(sys.stdout))  # print logger to stdout
    logger.setLevel(logging.INFO)
    logger.info("Starting daily calendar update")

    configFile = open('config.json')
    config = json.load(configFile)

    logger.info("JSON config loaded {}".format(config))

    icsLocation = config["icsURL"]
    dayToCapture = config["dayToCapture"]
    shutdownOnUpdate = config["shutdownOnUpdate"]
    
    #dayToCapture
    now = datetime.now()
    now8 = now + timedelta(days=dayToCapture)
    start_date = (now.year, now.month, now.day)
    end_date =   (now8.year, now8.month, now8.day)

    try :
        logger.info("Starting daily calendar update")
        
        powerService = PowerHelper()
        currBatteryLevel = powerService.get_battery()
        logger.info('Battery level at start: {:.3f}'.format(currBatteryLevel))

        
        calendarFile = GetCalendarFile(logger, icsLocation)
        calEvents = ExtractCalendarEvents(calendarFile, start_date, end_date)

        eventsImage = BuildEvents(calEvents)
        eventsImage = AddBattery(eventsImage,currBatteryLevel)

        epd = epd7in5_V2.EPD()
        
        logging.info("init and Clear")
        epd.init()
        epd.Clear()        

        epd.display(epd.getbuffer(eventsImage))        

        logging.info("Goto Sleep...")
        epd.sleep()

        powerService.sync_time() #

        if shutdownOnUpdate :
            #as an extra safty feature check to see if it is the first 5 minutes of the hour as this is when the system will be shedulded to update
            logger.info("Configured to shutdown after update")
            if now.minute in range (0,5):
                logger.info("Shutting down safely.")
                import os
                os.system("sudo shutdown -h now")
        
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd7in5_V2.epdconfig.module_exit()
        exit()

    except Exception as e:
        logger.error(e)

    logger.info("Completed daily calendar update")
    

if __name__ == "__main__":
    main()