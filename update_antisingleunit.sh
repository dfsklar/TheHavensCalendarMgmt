export PATHdestination=/var/www/html/goocal_proxy/anti_singleunit.ics
export PATHsource=/var/www/html/goocal_proxy/union.ics

# cat $PATHsource | python update_antisingleunit.py > $PATHdestination 2> logs/antisingleunit.stderr

cat $PATHsource | python3 ensureempty_antisingleunit.py > $PATHdestination 2> logs/antisingleunit.stderr
