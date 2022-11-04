"""
This file is not in use anymore.
"""


from event import Event
from address import Address


def create_event(event: Event, address: Address, gui_calendar: object):
    """
    Creates an event on the Google Calendar
    Args:
        event (Event): The event to be created
        address (Address): The address of the event
        gui_calendar (object): The calendar object
    """
    # if not event.validate():
    #     return

    event_date = event.time
    event_address = str(address)

    event_text = f"Event Details:\n{str(event)}\n\n Address:\n{str(event_address)}"
    gui_calendar.calevent_create(event_date, event_text, ["event"])
    gui_calendar.selection_set(event_date)
