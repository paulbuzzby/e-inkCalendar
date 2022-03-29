from datetime import datetime, timedelta
import string
from numpy import isin
import pytz

utc=pytz.UTC

class myCalEvent():
 
    def __init__(self, evTitle : str, evDate :datetime, duration :timedelta):
        self.evTitle = evTitle        
        if isinstance(evDate, str) :
            self.evDate = datetime.fromisoformat(evDate)
        elif isinstance(evDate, datetime) : #Check to see if the event in the calendar has a time. If it doesn't then it is an all day event
            self.evDate = evDate 
        else :            
            self.evDate = utc.localize(datetime(evDate.year, evDate.month, evDate.day)) # Force an all day event to have a time so that comparisons can be done to order the events
            #https://devtip.in/15307623/cant-compare-naive-and-aware-datetimenow-less=-challengedatetime_end
        self.duration = duration

    def __lt__(self, other): # built it less than comparison so events can be ordered
        return self.evDate < other.evDate

    def dump(self):
        return {"CalEvent": {'title': self.evTitle,
                                    'date': self.evDate.isoformat(),                                    
                                    'duration': self.duration.total_seconds()}}
    # usage - jsonEvents = json.dumps([o.dump() for o in MyCalEvents])
    #https://stackoverflow.com/questions/27585192/how-to-convert-a-list-of-object-to-json-format-in-python
    @staticmethod
    def load(dumped_obj):
        return myCalEvent(dumped_obj['CalEvent']['title'],
                            dumped_obj['CalEvent']['date'],
                            timedelta(seconds=dumped_obj['CalEvent']['duration']))
    # usage - newEvents = []
    # for x in json.loads(jsonEvents) :
    #     newEvents.append(myCalEvent.load(x))