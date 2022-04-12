from typing import List
import logging

import icalendar
import recurring_ical_events
import urllib.request
import json


from my_cal_events import myCalEvent


#Take URL or file location and return calendar result
def GetCalendarFile(logger, url : str) :
    logger.info("GetCalendarFile Entry {}".format(url))
    cal = ''

    if not url.lower().endswith('ics') : #link is not an ICS link
        raise Exception("Calendar link must be to an ICS file or URL")

    if url.startswith('http') :
        logger.info("Calendar URL is online")
        cal = urllib.request.urlopen(url).read()
    else :
        cal = open(url).read()

    return cal


def ExtractCalendarEvents(calendarFile, startDate : tuple, endDate : tuple) -> List[myCalEvent] :
    
    MyCalEvents = []    

    calendar = icalendar.Calendar.from_ical(calendarFile)
    events = recurring_ical_events.of(calendar).between(startDate, endDate)

    for event in events:    
        start = event["DTSTART"].dt
        duration = event["DTEND"].dt - event["DTSTART"].dt
        title = event["SUMMARY"]
        MyCalEvents.append(myCalEvent(title,start,duration))

    return sorted(MyCalEvents)



#Convert to JSON object

def ConvertCalendarEventsToJSON(events : List[myCalEvent]) ->str :
    jsonEvents = json.dumps([o.dump() for o in events])

    return jsonEvents

def CreateCalendarEventsFromJSON(json : str) -> List[myCalEvent] :

    newEvents = []
    for x in json :
        newEvents.append(myCalEvent.load(x))

    return newEvents