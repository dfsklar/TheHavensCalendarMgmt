# For help:
#    https://stackoverflow.com/questions/9044084/efficient-date-range-overlap-calculation-in-python

import sys
import datetime
from datetime import datetime, timedelta
from collections import namedtuple

Range = namedtuple('Range', ['start', 'end'])

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
            start_day = parse(field2)
        elif field1 == 'DTSTAMP':
            dtstamp = field2
        elif field1 == "DTEND;VALUE=DATE":
            end_today = parse(field2)
            end_tomorrow = end_today + timedelta(days=1)
            end_tomorrow_day = end_tomorrow.day
            # print "%s:%s" % (field1, end_tomorrow.strftime("%Y%m%d"))
        elif field1 == "SUMMARY":
            is_bothunit_booking = ('BOTH' in field2.strip())
            summary = field2
        elif field1 == "END" and ("VEVENT" in field2):
            if not is_bothunit_booking:
                print "-----------------"
                print summary
                print start_day
                print end_today
# TO TEST:  python update_antisingleunit.py < /var/www/BIRCHHAVEN/goocal_proxy/union.ics


