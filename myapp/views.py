from oauth2client.client import GoogleCredentials
from django.shortcuts import render

import httplib2
import os
from dateutil import parser

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from django.utils import timezone

import datetime
import pytz

# Create your views here.

def myfunc(request, *args, **kwargs):
    
    events = get_calendar()
    
    return render(request, 'templaatti.html', {'events' : events})

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
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
    
    '''
    Get calendar events
    Returns calendar events as a dict from Google calendar
    '''
def get_calendar():
    credentials = get_credentials()
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.now().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
    calendarId='p4r635n487mr7u9cje9n6985e0@group.calendar.google.com', timeMin=now, maxResults=10, singleEvents=True,
    orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    keys = ['summary', 'start', 'end']

    for i in range(len(events)):
        events[i] = dict((key,value) for key, value in events[i].items() if key in keys)
        if 'dateTime' in events[i]['start']:
            print(events[i]['start'], "\n")
            events[i]['start']['parsed'] = parser.parse(events[i]['start']['dateTime'])
            events[i]['end']['parsed'] = parser.parse(events[i]['end']['dateTime'])
            events[i]['endpm'] = events[i]['end']['parsed']
            print(events[i]['start']['parsed'], '\n\n')
        else:
            events[i]['start']['parsed'] = parser.parse(events[i]['start']['date'])
            events[i]['end']['parsed'] = parser.parse(events[i]['end']['date'])
            if (events[i]['end']['parsed'] - events[i]['start']['parsed']) \
                <= datetime.timedelta(days=1):
                events[i]['end'].pop('parsed')
                
	
	
	
    return events
