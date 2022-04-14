#https://code-maven.com/create-images-with-python-pil-pillow

import os
from PIL import Image, ImageDraw, ImageFont
from datetime import date, datetime, timedelta
from typing import List

import numpy as np

from my_cal_events import myCalEvent
from helpers import *

width = 480
height = 800

headerHeight = 30
eventHeight = 50

backColour = (255, 255, 255)
textColour = (0, 0, 0)

fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Fonts')

fntBold = ImageFont.truetype(os.path.join(fontdir, 'OpenSans-Bold.ttf'), 20)
fntlarge = ImageFont.truetype(os.path.join(fontdir, 'OpenSans-Regular.ttf'), 20)
fntTime = ImageFont.truetype(os.path.join(fontdir, 'OpenSans-Regular.ttf'), 15)
fntEventSummary = ImageFont.truetype(os.path.join(fontdir, 'OpenSans-Regular.ttf'), 22)
fntError = ImageFont.truetype(os.path.join(fontdir, 'OpenSans-Regular.ttf'), 12)

#Create the day header and return the image
def CreateDayHeader(x: myCalEvent) -> Image:
    today = date.today()
    dayString = x.evDate.strftime("%a %d %b")

    img = Image.new('RGB', (width, headerHeight), color = backColour)

    if x.evDate.date() == today :
        d = ImageDraw.Draw(img)
        d.text((10,1), "Today", font=fntBold, fill=textColour)
        d.text((80,1), dayString, font=fntlarge, fill=textColour)
    elif x.evDate.date() == (today + timedelta(days=1)) :
        d = ImageDraw.Draw(img)
        d.text((10,1), "Tomorrow", font=fntBold, fill=textColour)
        d.text((120,1), dayString, font=fntlarge, fill=textColour)
    else :
        d = ImageDraw.Draw(img)
        d.text((10,1), dayString, font=fntlarge, fill=textColour)

    d.line([(0,0),(width,0)], fill=textColour, width=2) #create a split between the days
    return img

def CreateEventEntry(x: myCalEvent) -> Image:
    
    formatStr = "{H}h {M}m" #1h 30m
    eventTime = x.evDate.strftime("%H:%M") #12:00
    eventDuration = strfdelta(x.duration, formatStr)

    img = Image.new('RGB', (width, eventHeight), color = backColour)

    d = ImageDraw.Draw(img)
    if x.evTitle != "No Events" :
        d.text((10,5), eventTime, font=fntTime, fill=textColour)
        d.text((10,25), eventDuration, font=fntTime, fill=textColour)

    d.text((80,7), x.evTitle, font=fntEventSummary, fill=textColour)

    return img

def CreateTimestamp(currentHeight) -> Image:


    img = Image.new('RGB', (width, height-currentHeight), color = backColour)
    d = ImageDraw.Draw(img)
    d.text((25,0), datetime.now().isoformat(), font=fntError, fill=textColour)

    return img

def BuildEvents(events : List[myCalEvent]) -> Image :

    currentDate = date.today()
    dayHeaderCreated = False
    eventImages = []
    heightCount = 0

    events = CheckForMissingDays(events)

    for e in sorted(events):
        
        if currentDate != e.evDate.date() :
            currentDate = e.evDate.date()
            dayHeaderCreated = False

        if currentDate == e.evDate.date() and dayHeaderCreated is False :
            eventImages.append(CreateDayHeader(e)) 
            dayHeaderCreated = True
            heightCount += headerHeight
        
        eventImages.append(CreateEventEntry(e))
        heightCount += eventHeight
        
        if heightCount > 740 :
            break


    while heightCount > 800 :
        i = eventImages.pop() # BUG if the last time through the loop is also a new day and height count is less than 750 it has a chance to make an image over 800
        heightCount -= i.height

    eventImages.append(CreateTimestamp(heightCount))
    imgs_comb = append_images(eventImages,"virtical")

    return imgs_comb

def CheckForMissingDays(events : List[myCalEvent]) -> List[myCalEvent] :

    first = True
    lastDay = date.today()
    nextDay = date.today()
    newEvents = []

    for e in sorted(events):

        if first :
            lastDay = e.evDate.date()
            nextDay = lastDay + timedelta(days=1)
            first = False
        
        if not first :
            if e.evDate.date() != lastDay and e.evDate.date() != nextDay :
                newEvents.append(myCalEvent("No Events",nextDay,timedelta(hours=0)))                
        
        lastDay = e.evDate.date()
        nextDay = lastDay + timedelta(days=1)
        
        newEvents.append(e)


    return sorted(newEvents)

def AddBattery(img : image, batteryLevel) -> image:
    
    d = ImageDraw.Draw(img)
    d.text((400,2), 'Battery {:.0f}%'.format(batteryLevel), font=fntError, fill=textColour)

    return img