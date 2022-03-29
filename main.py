from datetime import datetime
from datetime import timedelta 
import json
import logging
import sys

from ImageCreator import *
from iCalendarHelper import *

#Battery Display
#Error information if occurs


def main() :
        
    # Create and configure logger
    logging.basicConfig(filename="logfile.log", format='%(asctime)s %(levelname)s - %(message)s', filemode='a')
    logger = logging.getLogger('fridgeCal')
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

        calendarFile = GetCalendarFile(logger, icsLocation)
        calEvents = ExtractCalendarEvents(calendarFile, start_date, end_date)

        eventsImage = BuildEvents(calEvents)

        #eventsImage.show()       




    except Exception as e:
        logger.error(e)

    logger.info("Completed daily calendar update")
    

if __name__ == "__main__":
    main()