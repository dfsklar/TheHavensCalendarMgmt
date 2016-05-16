cd /root/TheHavensCalendarMgmt/

DF=/var/www/BIRCHHAVEN/goocal_proxy/

python update_union_goocal.py && \
sh refresh.sh sh https://calendar.google.com/calendar/ical/nu1je77d8je49j11rjfbd3tnjg%40group.calendar.google.com/private-a013b65e5ed16f0ca12971a9a6a2269c/basic.ics $DF && \
sh refresh.sh bh https://calendar.google.com/calendar/ical/humh3m6csgsc1en0893s9ibfdc%40group.calendar.google.com/private-fc7d6846b717bcf2c8a9d454de55aa7a/basic.ics $DF && \
sh refresh.sh union https://calendar.google.com/calendar/ical/ruck03hfkh84jlb6l93fg0sob4%40group.calendar.google.com/private-35a3c6e9eaa7fbc02dc5e282db3d8e2e/basic.ics $DF

if test $? -eq 66
then
    echo "OK status - no refresh of proxy files because no change found in source-of-truth goocals"
else
    echo "SOMETHING BAD HAPPENED"
fi
