# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from __future__ import print_function
import argparse
import sys
import os
import json
import hashlib
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
# The app name shown during OAuth (e.g. "Quickstart") is set in Google Cloud
# Console → APIs & Services → OAuth consent screen → App name.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def event_signature_hash(event):
  """Hash of summary, start, end, and eventType for change detection."""
  summary = event.get('summary', '')
  # Remove any trailing "<<<...>>>" in the summary
  import re
  summary = re.sub(r'\s*<<<.*?>>>$', '', summary)
  summary = summary.strip()
  canonical = json.dumps({
    'summary': summary,
    'start': event.get('start', {}),
    'end': event.get('end', {}),
    'eventType': event.get('eventType', ''),
  }, sort_keys=True)
  print("\n\n\n\n****** CANONICAL:\n")
  print(canonical)
  print("\n\n\n\n\n")
  return hashlib.sha256(canonical.encode('utf-8')).hexdigest()


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
            pickle.dump(creds, token, protocol=0)

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


CALENDARS = {
  "SPRUCE": 'nu1je77d8je49j11rjfbd3tnjg@group.calendar.google.com',
  "BIRCH": 'humh3m6csgsc1en0893s9ibfdc@group.calendar.google.com',
  "UNION": 'ruck03hfkh84jlb6l93fg0sob4@group.calendar.google.com'
}

global CHANGE_COUNT
CHANGE_COUNT = 0




def retrieve_events(service, calname):

  # This will fetch only events in the future or very recent past (within the last 30 days).

  import datetime

  now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

  eventsResult = service.events().list(
    calendarId=CALENDARS[calname],
    timeMin=(datetime.datetime.utcnow() - datetime.timedelta(days=30)).isoformat() + 'Z', maxResults=2000, singleEvents=True,
    orderBy='startTime').execute()
  events = eventsResult.get('items', [])
  print("Retrieved %d events" % len(events))
  # INSERT_YOUR_CODE
  for i, event in enumerate(events[:1]):
      print(f"Event {i + 1}: {event}")

  return events






# Prior to 2026MAR14, I was using this method to bring SH and BH events into the UNION calendar.
# However, bringing in only new events caused the union cal to be unable to get *corrections* made to SH and BH events.
# I keep this here for historical reference.
def import_event_if_new(service, candidate_import, haystack, destination_goocal):
  assert False
  icalUID = candidate_import['iCalUID']
  needle = '<<<' + icalUID + '>>>'

  # The haystack event list is set up so the icalUID is located in the event's summary in this form:
  #   <<<theID>>>.
  # So we first need to find out if this icalUID is already present in the haystack
  if not any(needle in x['summary'] for x in haystack):
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







def reimport_event(service, candidate_import, haystack, destination_goocal, dry_run=False):
  global CHANGE_COUNT
  icalUID = candidate_import['iCalUID']
  needle = '<<<' + icalUID + '>>>'

  # The haystack event list is set up so the icalUID is located in the event's summary in this form:
  #   <<<theID>>>.
  import_body = {
    "summary": candidate_import['summary'] + "     " + needle,
    "start": candidate_import['start'],
    "end": candidate_import['end']
  }

  matching = [x for x in haystack if needle in x.get('summary', '')]
  if matching:
    existing = matching[0]
    candidate_hash = event_signature_hash(candidate_import)
    existing_hash = event_signature_hash(existing)
    if candidate_hash != existing_hash:
      # Signature differs: delete from destination, then re-insert
      print("FOUND IN HAYSTACK BUT SIGNATURE CHANGED, SO:  DELETING THEN RE-INSERTING:")
      print(import_body)
      print("INTO THIS CALENDAR:")
      print(destination_goocal)
      if dry_run:
        print("(dry run - skip delete and insert)")
      else:
        service.events().delete(calendarId=destination_goocal, eventId=existing['id']).execute()
        the_result = service.events().insert(calendarId=destination_goocal, body=import_body).execute()
        print(the_result)
      global CHANGE_COUNT
      CHANGE_COUNT += 1
    # else: same signature, do nothing
  else:
    # Not yet in haystack: insert only
    print("ABOUT TO IMPORT THIS NEW EVENT:")
    print(import_body)
    print("INTO THIS CALENDAR:")
    print(destination_goocal)
    if dry_run:
      print("(dry run - skip insert)")
    else:
      the_result = service.events().insert(calendarId=destination_goocal, body=import_body).execute()
      print(the_result)
    CHANGE_COUNT += 1






def main(service, dry_run=False):
    global CHANGE_COUNT

    if dry_run:
      print("DRY RUN - no inserts or deletes will be performed")
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
      reimport_event(service, candidate_import, events['UNION'], CALENDARS['UNION'], dry_run=dry_run)
    print("Looking for new events in SPRUCE cal...")
    for candidate_import in events['SPRUCE']:
      reimport_event(service, candidate_import, events['UNION'], CALENDARS['UNION'], dry_run=dry_run)

    print("ENDGAME OF update_union_goocal...")
    if CHANGE_COUNT > 0:
        print("%d CHANGED/NEW EVENTS WERE FOUND AND PROCESSED" % CHANGE_COUNT)
        sys.exit(0)
    else:
        print("NO CHANGES WERE FOUND!")
        sys.exit(0)


def parse_args():
  p = argparse.ArgumentParser(description="Update UNION Google calendar from BIRCH and SPRUCE.")
  p.add_argument("--dry-run", "-n", action="store_true",
                 help="Do not perform any inserts or deletes; only show what would be done.")
  return p.parse_args()


if __name__ == "__main__":
  args = parse_args()
  service = init_service()
  main(service, dry_run=args.dry_run)

