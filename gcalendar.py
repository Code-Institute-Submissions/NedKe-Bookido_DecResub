"""
gcalendar module interacts with Google calendar API
It contains methods to create a new event and update an event
Google Calendar API Resources website:
https://developers.google.com/calendar/api/v3/reference
"""

from __future__ import print_function

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = 'http://www.googleapis.com/auth/calendar'

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPES)

CAL = build('calendar', 'v3', credentials=CREDS)

CAL_ID = 'l3pgnrii459d7a696a9pb0fcco@group.calendar.google.com'
GMT_OFF = '+01:00'


def add_event(event):
    """
    Inserts a new event to the Google Calendar
    :param event: Event to be created
    """
    CAL.events().insert(
        calendarId=CAL_ID,
        sendNotifications=True, body=event
    ).execute()


def update_event_description(event_id, description):
    """
    Updates an event description using it's event_id when a new product
    is booked
    :param event_id
    :param description
    """
    event = CAL.events().get(calendarId=CAL_ID, eventId=event_id).execute()
    event['description'] = description
    CAL.events().update(
        calendarId=CAL_ID,
        eventId=event_id,
        body=event
    ).execute()
