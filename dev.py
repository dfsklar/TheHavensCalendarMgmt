# For help:
#    https://stackoverflow.com/questions/9044084/efficient-date-range-overlap-calculation-in-python
#
# TO TEST:  python update_antisingleunit.py < /var/www/BIRCHHAVEN/goocal_proxy/union.ics

import sys
from collections import namedtuple
import arrow

Range = namedtuple('Range', ['startnight', 'lastnight'])
# r1 = Range(start=datetime(2012, 1, 15), end=datetime(2012, 5, 10))
# r2 = Range(start=datetime(2012, 3, 20), end=datetime(2012, 9, 15))



today = arrow.now().replace(hour=0, minute=0, second=0, microsecond=0)
finaldate = today.shift(years=2)


alldates = list(arrow.Arrow.range('day', today, finaldate))

THECAL = {}

def day_of_year(arrowdate):
    return int(x.format('DDD'))

def is_weekend(arrowdate):
    # FRI and SAT are the weekends
    return int(x.format('d')) in [5, 6]

def printdebug(x):
    print '------'
    print x
    print x.format('ddd')
    print day_of_year(x)
    print is_weekend(x)


def is_in_peak_period(arrowdate):
    doy = day_of_year(arrowdate)
    return (doy < 2) or (doy>=165 and doy<=257) or (doy>=350)


# STEP 1: Block all dates as the default
for x in alldates:
    THECAL[x] = 'blocked'

# STEP 2: Unblock all non-peak weekdays
for x in alldates:
    if not is_weekend(x):
        if not is_in_peak_period(x):
            THECAL[x] = 'avail'


# ON STDIN: The UNION calendar ics file
# STEP 3: Unblock any days that are already booked to a single unit
for line in sys.stdin:
    if line[0] != ' ':
        (field1, field2) = line.split(':', 1)
        if field1 == 'DTSTART;VALUE=DATE':
            start_day = arrow.get(field2)
        elif field1 == 'DTSTAMP':
            dtstamp = field2
        elif field1 == "DTEND;VALUE=DATE":
            checkout_date = arrow.get(field2)
            last_booked_date = checkout_date.shift(days=-1)
        elif field1 == "SUMMARY":
            is_bothunit_booking = ('BOTH' in field2.strip())
            summary = field2
        elif field1 == "END" and ("VEVENT" in field2):
            if not is_bothunit_booking and (last_booked_date > today):
                print "Processing " + line
                while start_day <= last_booked_date:
                    THECAL[start_day] = 'avail'
                    start_day = start_day.shift(days=1)

# STEP 4: Unblock any days that are "imminent"
for x in arrow.Arrow.range('day', today, today.shift(weeks=2)):
    THECAL[x] = 'avail'
for x in arrow.Arrow.range('day', today.shift(weeks=2), today.shift(weeks=3)):
    if not is_in_peak_period(x):
        THECAL[x] = 'avail'

# DEBUG                           
for x in alldates:
    print x
    print THECAL[x]


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
    
