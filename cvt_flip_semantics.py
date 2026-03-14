import sys
import datetime

# ARG 1:  The abbrev for the unit e.g. "404C"

condo_unit = sys.argv[1]

from datetime import datetime

def parse(date_string):
    # Try to handle both date and datetime strings in ICS, removing any trailing newlines/spaces
    date_string = date_string.strip()
    # Handle formats like 20230614 or 20230614T090000Z
    if 'T' in date_string:
        try:
            return datetime.strptime(date_string, "%Y%m%dT%H%M%SZ")
        except ValueError:
            return datetime.strptime(date_string, "%Y%m%dT%H%M%S")
    else:
        return datetime.strptime(date_string, "%Y%m%d")

for line in sys.stdin:
    if line[0] != ' ':
        (field1, field2) = line.split(':', 1)
        if field1 == 'DTSTART;VALUE=DATE':
            start_day = parse(field2).day
        elif field1 == 'DTSTAMP':
            dtstamp = field2
        elif field1 == 'LAST-MODIFIED':
            print("%s:%s" % (field1, dtstamp.rstrip()))
            continue
        elif field1 == "DTEND;VALUE=DATE":
            end_today = parse(field2)
            from datetime import timedelta
            end_tomorrow = end_today + timedelta(days=1)
            end_tomorrow_day = end_tomorrow.day
            print("%s:%s" % (field1, end_tomorrow.strftime("%Y%m%d")))
            continue
        elif field1 == "SUMMARY":
            print("%s:%s %s-%s %s" % (field1, condo_unit, start_day, end_today.day, field2.rstrip()))
            continue

    print(line.rstrip())
