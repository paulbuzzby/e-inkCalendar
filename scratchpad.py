import os
from datetime import datetime, timedelta
from helpers import *
from power import PowerHelper


today = datetime.now()

x = timedelta(seconds=86400.0)
onehour = timedelta(seconds=4600)
formatStr = '{H}h {M}m'

print(today.strftime("%H:%M"))
print(strfdelta(x, formatStr))
print(strfdelta(onehour, formatStr))

directory = os.path.dirname(__file__)
#ics = open(os.path.join(directory, 'issue_53_parsing_failure.ics'),'rb')

print(directory)
#print(ics)

powerService = PowerHelper()

#currBatteryLevel = powerService.get_battery()
#print('Battery level at start: {:.0f}%'.format(currBatteryLevel))
#print(today.now().astimezone().replace(microsecond=0).isoformat())
#batteryDate = datetime.fromisoformat("2022-03-30T16:02:09+01:00")

print(powerService.get_RTC_time())
print(today.minute)
print(0 <= today.minute <= 5)
print(today.minute in range(55,59))

#2022-03-30T16:02:03+01:00
#2022-03-30T16:02:09+01:00