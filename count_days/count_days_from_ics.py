import fileinput
import sys
from dateutil.parser import parse
import datetime

total = 0

for line in sys.stdin:
    print line
    if (line[0] == ' '):
        continue
    if (line.startswith("SUMMARY")):
        continue
    (field1, field2) = line.split(':')
    if 'DTSTART' in field1:
      if '2015' in field2:
        dtstart = parse(field2)
        raise Exception(dtstart)
      else:
        dtstart = None
    if 'DTEND' in field1:
      dtend = parse(field2)
      
      
