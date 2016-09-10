import sys
import datetime

# ARG 1:  The abbrev for the unit e.g. "404C"

condo_unit = sys.argv[1]

from dateutil.parser import parse

for line in sys.stdin:
    (field1, field2) = line.split(':')
    if field1 == 'DTSTART;VALUE=DATE':
        start_day = parse(field2).day
    elif field1 == "DTEND;VALUE=DATE":
        end_today = parse(field2)
        end_tomorrow = end_today + datetime.timedelta(days=1)
        end_tomorrow_day = end_tomorrow.day
        print "%s:%s" % (field1, end_tomorrow.strftime("%Y%m%d"))
        continue
    elif field1 == "SUMMARY":
        print "%s:%s %s-%s %s" % (field1, condo_unit, start_day, end_tomorrow_day, field2)
        sys.exit(1)
    else:
        print line.rstrip()







