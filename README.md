# TheHavensCalendarMgmt

This could be of value in doing a copy-events scenario:

http://stackoverflow.com/questions/21467888/copy-events-from-one-google-calendar-to-another-without-duplication


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

