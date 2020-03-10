# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from __future__ import print_function
import sys
import os
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def init_service():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


if False:
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


service = init_service()



CALENDARS = {
  "SPRUCE": 'nu1je77d8je49j11rjfbd3tnjg@group.calendar.google.com',
  "BIRCH": 'humh3m6csgsc1en0893s9ibfdc@group.calendar.google.com',
  "UNION": 'ruck03hfkh84jlb6l93fg0sob4@group.calendar.google.com'
}

CHANGE_COUNT = 0


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
    import_body = {
      "summary": candidate_import['summary'] + "     " + needle,
      "start": candidate_import['start'],
      "end": candidate_import['end']
      }

    print("ABOUT TO IMPORT THIS:")
    print(import_body)
    print("INTO THIS CALENDAR:")
    print(destination_goocal)

    the_result = service.events().insert(calendarId=destination_goocal, body=import_body).execute()
    print(the_result)
    global CHANGE_COUNT
    CHANGE_COUNT += 1


def main(service):
    global CHANGE_COUNT
    
    events = {}

    if True:
      events['BIRCH'] = retrieve_events(service,'BIRCH')
      events['SPRUCE'] = retrieve_events(service,'SPRUCE')
      events['UNION'] = retrieve_events(service, 'UNION')
      pickle.dump(events, open("events.p", "wb"))
    else:
      events = pickle.load(open("events.p", "rb"))

    print("Looking for new events in BIRCH cal...")
    for candidate_import in events['BIRCH']:
      import_event_if_new(service, candidate_import, events['UNION'], CALENDARS['UNION'])
    print("Looking for new events in SPRUCE cal...")
    for candidate_import in events['SPRUCE']:
      import_event_if_new(service, candidate_import, events['UNION'], CALENDARS['UNION'])

    print("ENDGAME OF update_union_goocal...")
    if CHANGE_COUNT > 0:
        print("  Will return 0")
	sys.exit(0)
    else:
        print("  Will return 66")
	sys.exit(66)

main(service)

