# Make sure you are logged into your Monash student account.
# Go to: https://developers.google.com/calendar/quickstart/python
# Click on "Enable the Google Calendar API"
# Configure your OAuth client - select "Desktop app", then proceed
# Click on "Download Client Configuration" to obtain a credential.json file
# Do not share your credential.json file with anybody else, and do not commit it to your A2 git repository.
# When app is run for the first time, you will need to sign in using your Monash student account.
# Allow the "View your calendars" permission request.
# can send calendar event invitation to a student using the student.monash.edu email.
# The app doesn't support sending events to non student or private emails such as outlook, gmail etc
# students must have their own api key
# no test cases for authentication, but authentication may required for running the app very first time.
# http://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.html

# Code adapted from https://developers.google.com/calendar/quickstart/python
from datetime import datetime, timedelta
import json
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from address import Address

from event import Event
from people.attendee import Attendee

import pytz

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
]

CANCELLED_EVENTS = []
ALL_EVENTS = []


def get_calendar_api():
    """
    Get an object which allows you to consume the Google Calendar API.
    You do not need to worry about what this function exactly does, nor create test cases for it.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("calendar", "v3", credentials=creds)


def get_upcoming_events(api, starting_time, number_of_events):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next n events on the user's calendar.
    """
    if number_of_events <= 0:
        raise ValueError("Number of events must be at least 1.")

    events_result = (
        api.events()
        .list(
            calendarId="primary",
            timeMin=starting_time,
            maxResults=number_of_events,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    return events_result.get("items", [])


def post_event(api, event: Event):
    """
    Posts an event to the calendar
    """
    # validate event object
    # if not event.validate():
    #     raise ValueError("Event object is not valid")

    try:
        event.validate()
    except ValueError as e:
        print("The event object is invalid")
        raise e

    # print(event.body())
    api_response = (
        api.events().insert(calendarId="primary", body=event.body()).execute()
    )
    ALL_EVENTS.append(api_response)
    return api_response


def get_event_by_id(api, event_id):
    """
    Gets an event from the calendar by its id
    """
    event = api.events().get(calendarId="primary", eventId=event_id).execute()
    return event


def delete_event(api, event_id):
    """
    Deletes an event from the calendar with a known id

    """
    # raise an error if the event is deleted without an ID
    if event_id is None:
        raise ValueError("Event cant be deleted because it hasnt been created yet!")

    try:
        event_to_delete = get_event_by_id(api, event_id)
        # Get the date for the event
        event_date = event_to_delete["start"]["date"]
    except Exception as e:
        print("Event not found")
        raise e

    today = datetime.now()
    if event_date >= today:
        raise ValueError("Cannot delete future events")

    api_response = api.events().delete(calendarId="primary", eventId=event_id).execute()
    for ev in ALL_EVENTS:
        if ev["id"] == event_id:
            ALL_EVENTS.remove(ev)
            break
    return api_response


def cancel_event(api, event_id):

    if event_id is None:
        raise ValueError("Event ID cannot be None")

    if event_id == "":
        raise ValueError("Event ID cannot be empty")

    # Check if event is already cancelled
    for event in CANCELLED_EVENTS:
        if event["id"] == event_id:
            raise ValueError("Event is already cancelled")
    try:
        event = api.events().get(calendarId="primary", eventId=event_id).execute()
        event["status"] = "cancelled"
        updated_event = (
            api.events()
            .update(calendarId="primary", eventId=event_id, body=event)
            .execute()
        )
        CANCELLED_EVENTS.append(updated_event)
        return updated_event
    except Exception as e:
        print("Event not found")
        raise e


def main():
    api = get_calendar_api()
    time_now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time

    events = get_upcoming_events(api, time_now, 10)

    if not events:
        print("No upcoming events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])


def gui_create_event(event: Event, address: Address, gui_calendar: object):
    """
    Creates an event on the Google Calendar
    Args:
        event (Event): The event to be created
        address (Address): The address of the event
        gui_calendar (object): The calendar object
    """
    event_date = event.time
    event_address = str(address)
    event_text = f"Event Details:\n{str(event)}\n\n Address:\n{str(event_address)}"

    today = datetime.now()
    five_years = 5 * 365
    five_year_delta = timedelta(days=five_years)
    five_years_from_now = (today + five_year_delta).replace(tzinfo=pytz.UTC)
    five_years_in_past = (today - five_year_delta).replace(tzinfo=pytz.UTC)

    if not (event_date < five_years_in_past or event_date > five_years_from_now):
        gui_calendar.calevent_create(event_date, event_text, ["event"])
        gui_calendar.tag_config("event", background="green")
        gui_calendar.selection_set(event_date)

    # Use the api to create the event
    api = get_calendar_api()
    post_event(api, event)


def export_events():
    events = [*ALL_EVENTS, *CANCELLED_EVENTS]
    with open("events.json", "w") as f:
        json.dump(events, f)


def search_events(api, tag, value):
    """This function gets all your events and searches through them to find the ones that match the tag and value

    Args:
        tag (str): The tag to search for
        value (str): The value which is should match

    Returns:
        list: ALl events that match the tag and value
    """
    if tag is None:
        raise ValueError("Tag cannot be None")

    if tag == "":
        raise ValueError("Tag cannot be empty")

    if value is None:
        raise ValueError("Value cannot be None")

    if value == "":
        raise ValueError("Value cannot be empty")

    api = get_calendar_api()
    all_events = api.events().list(calendarId="primary").execute()["items"]
    valid_events = []

    try:
        all_events[0][tag]
    except KeyError:
        raise KeyError("Tag not found")

    for event in all_events:
        if event[tag] == value:
            valid_events.append(event)
    return valid_events


if __name__ == "__main__":
    # Prevents the main() function from being called by the test suite runner
    main()
    event1_address = Address(
        "Mr. John Smith",
        "123 Fake street",
        "CLayton",
        "VIC",
        "3168",
    )

    event1 = Event(
        "Event 1",
        "This is a test event",
        datetime(2022, 10, 10, 10, 0, 0),
        event1_address,
        [Attendee("John Smith", "abc@email.com")],
    )

    post_event(get_calendar_api(), event1)
    event1_id = event1.id
    print(get_event_by_id(get_calendar_api(), event1_id))
    delete_event(get_calendar_api(), event1_id)
    print(get_event_by_id(get_calendar_api(), event1_id))

    # cancel_event(get_calendar_api(), "123")
    # post_event(get_calendar_api(), event2)
    # print(
    #     get_upcoming_events(
    #         get_calendar_api(), datetime.datetime.utcnow().isoformat() + "Z", 10
    #     )
    # )
    # delete_event(get_calendar_api(), event1.id)
    # delete_event(get_calendar_api(), event2.id)

    # print(
    #     get_upcoming_events(
    #         get_calendar_api(), datetime.datetime.utcnow().isoformat() + "Z", 10
    #     )
    # )
