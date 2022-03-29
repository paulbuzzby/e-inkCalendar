from typing import List
import logging
import os
import icalendar
import recurring_ical_events
import urllib.request
import json
import sys
from datetime import datetime
from datetime import timedelta 
from iCalendarHelper import *
from my_cal_events import myCalEvent
import ImageCreator

logger = logging.getLogger('eInkCalendar')
logger.addHandler(logging.StreamHandler(sys.stdout))  # print logger to stdout
logger.setLevel(logging.INFO)


def DownLoadICSUrlToFile(url) : 

    #url = "https://outlook.live.com/owa/calendar/b15d0f2b-8803-4a05-beef-eb741989a5a0/1233b3bf-dd08-4cdc-a6d8-6ffe111e6422/cid-D326965B3EECB4FA/calendar.ics"

    directory = os.path.dirname(__file__)
    fileTosave = os.path.join(directory, 'testdata\calendar.ics')        
    calendarFile = GetCalendarFile(logger,url)
    calendarFile.write(fileTosave)


def ConvertICSFileToJSON(fileLocation : str) : 

    now = datetime.now()
    now8 = now + timedelta(days=8)
    start_date = (now.year, now.month, now.day)
    end_date =   (now8.year, now8.month, now8.day)
    
    calendarFile = GetCalendarFile(logger,fileLocation)
    MyCalEvents = ExtractCalendarEvents(calendarFile, start_date, end_date)

    #jsonEvents = json.dumps([o.dump() for o in MyCalEvents])

    directory = os.path.dirname(__file__)
    fileTosave = os.path.join(directory, 'testdata\CalendarEvents.json')

    with open(fileTosave, 'w') as f:
        json.dump([o.dump() for o in MyCalEvents], f)
    
def BuildImageFromTestData() : 

    testEventsFile = open("testdata\CalendarEvents.json")
    testEventJson = json.load(testEventsFile)

    testEvents = CreateCalendarEventsFromJSON(testEventJson)
    
    eventImg = ImageCreator.BuildEvents(testEvents)
    eventImg.show()
    eventImg.save('calendar.png')
    
def main() : 


    url = "https://outlook.live.com/owa/calendar/b15d0f2b-8803-4a05-beef-eb741989a5a0/1233b3bf-dd08-4cdc-a6d8-6ffe111e6422/cid-D326965B3EECB4FA/calendar.ics"
    directory = os.path.dirname(__file__)
    icsFile = os.path.join(directory, 'testdata\calendar.ics') 

    #ConvertICSFileToJSON(icsFile)
    BuildImageFromTestData()


if __name__ == "__main__":
    main()