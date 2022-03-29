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

currBatteryLevel = powerService.get_battery()
print('Battery level at start: {:.0f}%'.format(currBatteryLevel))