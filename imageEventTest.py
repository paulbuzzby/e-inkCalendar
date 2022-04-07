from PIL import Image, ImageDraw, ImageFont
from datetime import date, datetime, timedelta
import json

from my_cal_events import myCalEvent
import ImageCreator

testEventsFile = open("testdata\CalendarEventsMissingDay.json")
testEventJson = json.load(testEventsFile)

testEvents = []
for x in testEventJson :
    testEvents.append(myCalEvent.load(x))



#eventImg = ImageCreator.CreateEventEntry(testEvents[1])

#eventImg.show()

#e = ImageCreator.CheckForMissingDays(testEvents)

eventImg = ImageCreator.BuildEvents(testEvents)
eventImg.show()
eventImg.save('calendar.png')