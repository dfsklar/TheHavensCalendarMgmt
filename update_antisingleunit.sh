export PATHdestination=/var/www/BIRCHHAVEN/goocal_proxy/anti_singleunit.ics
export PATHsource=/var/www/BIRCHHAVEN/goocal_proxy/union.ics
# cat $PATHsource | python update_antisingleunit.py > $PATHdestination 2> logs/antisingleunit.stderr
cat $PATHsource | python ensureempty_antisingleunit.py > $PATHdestination 2> logs/antisingleunit.stderr
