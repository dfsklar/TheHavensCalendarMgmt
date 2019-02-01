# For help:
#    https://stackoverflow.com/questions/9044084/efficient-date-range-overlap-calculation-in-python
#
# TO TEST:  python update_antisingleunit.py < /var/www/BIRCHHAVEN/goocal_proxy/union.ics

import sys
import datetime
from datetime import datetime, timedelta, date
from collections import namedtuple

Range = namedtuple('Range', ['startnight', 'lastnight'])

ranges = []

# r1 = Range(start=datetime(2012, 1, 15), end=datetime(2012, 5, 10))
# r2 = Range(start=datetime(2012, 3, 20), end=datetime(2012, 9, 15))

# latest_start = max(r1.start, r2.start)
# earliest_end = min(r1.end, r2.end)
# delta = (earliest_end - latest_start).days + 1
# overlap = max(0, delta)


# ON STDIN: The UNION calendar ics file

from dateutil.parser import parse

for line in sys.stdin:
    if line[0] != ' ':
        (field1, field2) = line.split(':', 1)
        if field1 == 'DTSTART;VALUE=DATE':
            start_day = parse(field2).date()
        elif field1 == 'DTSTAMP':
            dtstamp = field2
        elif field1 == "DTEND;VALUE=DATE":
            checkout_date = parse(field2).date()
            last_booked_date = checkout_date - timedelta(days=1)
        elif field1 == "SUMMARY":
            is_bothunit_booking = ('BOTH' in field2.strip())
            summary = field2
        elif field1 == "END" and ("VEVENT" in field2):
            if not is_bothunit_booking and (last_booked_date > date.today()):
                ranges.append(Range(startnight=start_day, lastnight=last_booked_date))

curdate = datetime(2015,1,1)

print """BEGIN:VCALENDAR
PRODID:-//Google Inc//Google Calendar 70.9054//EN
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:HAVENS-AntiSingleUnit
X-WR-TIMEZONE:America/Los_Angeles
X-WR-CALDESC:Inverse of all single-unit bookings"""



calentry = """BEGIN:VEVENT
DTSTART;VALUE=DATE:%s
DTEND;VALUE=DATE:%s
DTSTAMP:20190201T103802Z
UID:havensantisingleunit_%s@google.com
CREATED:20190201T103202Z
DESCRIPTION:
LAST-MODIFIED:20190201T103202Z
LOCATION:
SEQUENCE:0
STATUS:CONFIRMED
SUMMARY:AntiSingleUnit Blocker
TRANSP:OPAQUE
END:VEVENT"""

def print_calentry(date1, date2):
    print calentry % (date1, date2, date1)
    

# TODO:  SORTING!
idx = 1
for R in ranges:
    inverse = Range(startnight=curdate, lastnight=R.startnight)
    print_calentry(inverse.startnight.strftime("%Y%m%d"), inverse.lastnight.strftime("%Y%m%d"))
    idx += 1
    curdate = R.lastnight + timedelta(days=1)


print_calentry(curdate.strftime("%Y%m%d"), "20660101")

print "END:VCALENDAR"
    
