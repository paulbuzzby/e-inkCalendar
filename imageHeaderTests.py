from PIL import Image, ImageDraw, ImageFont
from datetime import date, datetime, timedelta
import json

from my_cal_events import myCalEvent
import ImageCreator

testEventsFile = open("testdata\CalendarEvents.json")
testEventJson = json.load(testEventsFile)

testEvents = []
for x in testEventJson :
    testEvents.append(myCalEvent.load(x))

event = myCalEvent("Some Appointment I have made", datetime.today() + timedelta(days=1), 90)

header = ImageCreator.CreateDayHeader(event)

header.show()