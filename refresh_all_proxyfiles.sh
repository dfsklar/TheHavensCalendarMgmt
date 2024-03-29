source /home/sklawlxv/virtualenv/var/www/BIRCHHAVEN/pythonapp/2.7/bin/activate 

cd /home/sklawlxv/TheHavensCalendarMgmt/

find logs  -mtime 10 -print -exec /bin/rm {} \;

DF=~/var/www/BIRCHHAVEN/goocal_proxy/

python update_union_goocal.py && \
echo "About to re-pull from SH goocal" && \
sh refresh.sh sh https://calendar.google.com/calendar/ical/nu1je77d8je49j11rjfbd3tnjg%40group.calendar.google.com/private-3c6036e3a5b614ee6a18f0adc62e9247/basic.ics $DF && \
echo "About to re-pull from BH goocal" && \
sh refresh.sh bh https://calendar.google.com/calendar/ical/humh3m6csgsc1en0893s9ibfdc%40group.calendar.google.com/private-fc7d6846b717bcf2c8a9d454de55aa7a/basic.ics $DF && \
echo "About to re-pull from UNION goocal" && \
sh refresh.sh union https://calendar.google.com/calendar/ical/ruck03hfkh84jlb6l93fg0sob4%40group.calendar.google.com/private-35a3c6e9eaa7fbc02dc5e282db3d8e2e/basic.ics $DF && \
echo "About to refresh the anti-singleunit emission" && \
sh update_antisingleunit.sh

STAT=$?
if test $STAT -eq 66
then
    echo "OK status - no refresh of proxy files because no change found in source-of-truth goocals"
elif test $STAT -eq 0
then
    echo "OK status - fresh pulls from GooCals all done"
else
    echo "SOMETHING BAD HAPPENED"
    echo $STAT
fi
