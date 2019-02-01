# TheHavensCalendarMgmt

# Why do we need this?

VRBO stupidly does not allow importation of a google-hosted calendar, because "so often it has events like birthdays and to-do reminders".  INSANE!  It will let you display such calendars but it will not let events on those calendars actually block days from availability.  INSANE!!  So I have to mirror the google calendars on my own hosted site.

# Prep of a linux box

It is not enough to have python2.7 available.  There are other setups needed:

Firstly, note that on some linux boxes, `pip` won't work and you have to use `pip2.7` as your actual command line.

Some installs of use:
```
apt-get install python-pip
pip2.7 install dateutil
pip2.7 uninstall apiclient
easy_install  --upgrade google-api-python-client
easy_install httplib2
```

# Automating with cron
```
# THE HAVENS
2,7,12,17,22,27,32,38,42,47,52,57 * * * * nohup /bin/bash /home/dfsklar/TheHavensCalendarMgmt/refresh_all_proxyfiles.sh > /home/dfsklar/TheHavensCalendarMgmt/logs/delta_$$.nohup.out 2>&1
8,38 * * * *                              nohup /bin/bash /home/dfsklar/TheHavensCalendarMgmt/refresh_all_force.sh      > /home/dfsklar/TheHavensCalendarMgmt/logs/forceall_$$.nohup.out 2>&1
```
