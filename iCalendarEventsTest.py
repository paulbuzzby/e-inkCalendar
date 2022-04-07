import os
from datetime import datetime
from datetime import timedelta 
import icalendar
import recurring_ical_events
import urllib.request
import pytz
import json

from my_cal_events import myCalEvent



MyCalEvents = []
now = datetime.now()
now8 = now + timedelta(days=8)
start_date = (now.year, now.month, now.day)
end_date =   (now8.year, now8.month, now8.day)

directory = os.path.dirname(__file__)
#ics = open(os.path.join(directory, 'issue_53_parsing_failure.ics'),'rb')

url = "https://outlook.live.com/owa/calendar/b15d0f2b-8803-4a05-beef-eb741989a5a0/1233b3bf-dd08-4cdc-a6d8-6ffe111e6422/cid-D326965B3EECB4FA/calendar.ics"
#url = os.path.join(directory, 'testdata\calendar.ics')

if url.startswith('http') :
    ical_string = urllib.request.urlopen(url).read()
else :
    ical_string = open(url).read()



calendar = icalendar.Calendar.from_ical(ical_string)
events = recurring_ical_events.of(calendar).between(start_date, end_date)

for event in events:    
    start = event["DTSTART"].dt
    duration = event["DTEND"].dt - event["DTSTART"].dt
    title = event["SUMMARY"]
    MyCalEvents.append(myCalEvent(title,start,duration))
    #print("Title {} start {} duration {} ".format(title, start, duration))

#TODO - create function to output calendar to JSON file

for e in sorted(MyCalEvents):
    print("Title {} start {} duration {} ".format(e.evTitle, e.evDate, e.duration))
    #print(e.evDate)

jsonEvents = json.dumps([o.dump() for o in MyCalEvents])

newEvents = []
for x in json.loads(jsonEvents) :
    newEvents.append(myCalEvent.load(x))
#newEvents = [MyCalEvents.load(dumped_ipport)
 #              for dumped_ipport in json.loads(jsonEvents)]

print(jsonEvents)