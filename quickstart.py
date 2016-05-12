from __future__ import print_function
import httplib2
import os

import pickle

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


CALENDARS = {
  "SPRUCE": 'nu1je77d8je49j11rjfbd3tnjg@group.calendar.google.com',
  "BIRCH": 'humh3m6csgsc1en0893s9ibfdc@group.calendar.google.com',
  "UNION": 'ruck03hfkh84jlb6l93fg0sob4@group.calendar.google.com'
}


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.params['access_type'] = 'offline'  # SKLARD added this
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials



def retrieve_events(service, calname):
  now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

  eventsResult = service.events().list(
    calendarId=CALENDARS[calname],
    timeMin=now, maxResults=2000, singleEvents=True,
    orderBy='startTime').execute()
  events = eventsResult.get('items', [])
  return events


def import_event_if_new(service, candidate_import, haystack, destination_goocal):
  icalUID = candidate_import['iCalUID']
  needle = '<<<' + icalUID + '>>>'

  # The haystack event list is set up so the icalUID is located in the event's summary in this form:
  #   <<<theID>>>.
  # So we first need to find out if this icalUID is already present in the haystack
  if len(filter(lambda x: needle in x['summary'], haystack)) == 0:
    # If we get here, we know that the candidate_import event is NOT yet present in the haystack
    #service.insert(destination_goocal,
    print("HELLO")




def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    
    events = {}

    if False:
      events['BIRCH'] = retrieve_events(service,'BIRCH')
      events['SPRUCE'] = retrieve_events(service,'SPRUCE')
      events['UNION'] = retrieve_events(service, 'UNION')
      pickle.dump(events, open("events.p", "wb"))
    else:
      events = pickle.load(open("events.p", "rb"))

    for candidate_import in events['BIRCH']:
      import_event_if_new(service, candidate_import, events['UNION'], CALENDARS['UNION'])
    for candidate_import in events['SPRUCE']:
      import_event_if_new(service, candidate_import, events['UNION'], CALENDARS['UNION'])
    

if __name__ == '__main__':
    main()
