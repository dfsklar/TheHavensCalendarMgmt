# TheHavensCalendarMgmt

## Which python

Written for python 2.7 but:  For the purpose of doing the google-accounts login for the "union" script, you can run that script on python 3 and it will do the login fine and then crash after the pickle file is emitted (which is all you need to facilitate login back on the robot machine anyway).

## Feature one:  providing a proxy way to access our google calendars

VRBO stupidly does not allow importation of a google-hosted calendar, because "so often it has events like birthdays and to-do reminders".  INSANE!  It will let you display such calendars but it will not let events on those calendars actually block days from availability.  INSANE!!  So I have to mirror the google calendars on my own hosted site.


## Feature two: the "unionizing" feature

We have a separate google calendar for Birch and Spruce that we maintain manually.  The "union" python script is in charge of recognizing reservations on the B and S calendars, and automatically creating entries on the "UNION" ("All Havens") calendar since we cannot allow reserving the both-unit property when any one of the single-unit properties is reserved.

This "union" python script writes to a google calendar so it must be authenticated with google accounts.

It stays "logged-in" by preserving a pickle file with our authentication creds.  If ever that pickle file expires or is lost, you will need to rebuild by running that program on a windows/mac, so it can launch a browser and have you login.  After successful login, it will generate a pickle file that you can distribute to the machine that is robotically running that same script.




## About the anti-single unit calendar

This is an attempt to artificially block rental of the individual single units during weekends and during peak periods of summer/holidays.

During peak seasons: we want to offer NO singles at all. But we open up all peak dates if unrented 2 weeks out.

Non-peak: no singles for fri and sat, but singles ok for weekdays. But open up all dates that are unrented 3 weeks out.

However: if one of the singles is rented, no matter what time of year or of week, the other single must NOT be blocked.



## Prep of a linux box

It is not enough to have python2.7 available.  There are other setups needed:

Firstly, note that on some linux boxes, `pip` won't work and you have to use `pip2.7` as your actual command line.

Some installs of use:
```
apt-get install python-pip
pip2.7 install dateutil
pip2.7 uninstall apiclient
easy_install  --upgrade google-api-python-client
easy_install httplib2
easy_install pyarrow
```



## Automating with cron
```
# THE HAVENS
2,7,12,17,22,27,32,38,42,47,52,57 * * * * nohup /bin/bash /home/dfsklar/TheHavensCalendarMgmt/refresh_all_proxyfiles.sh > /home/dfsklar/TheHavensCalendarMgmt/logs/delta_$$.nohup.out 2>&1
8,38 * * * *                              nohup /bin/bash /home/dfsklar/TheHavensCalendarMgmt/refresh_all_force.sh      > /home/dfsklar/TheHavensCalendarMgmt/logs/forceall_$$.nohup.out 2>&1
```
