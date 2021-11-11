from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

SCOPES = 'http://www.googleapis.com/auth/calendar'

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPES)

CAL = build('calendar', 'v3', credentials=CREDS)

CAL_ID = ''
GMT_OFF = '+01:00'

def add_event(event):
    CAL.events().insert(
        calendarId=CAL_ID,
        sendNotifications=True, body=event
    ).execute()