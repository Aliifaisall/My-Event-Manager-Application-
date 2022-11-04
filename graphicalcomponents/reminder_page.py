# Code to import from parent directory ===================
import sys
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# ========================================================

# GUI imports ============================================
import tkinter as tk
from graphicalcomponents.page import Page
from graphicalcomponents.labelwidget import LabelWidget
from tkinter import messagebox

# ========================================================

from MyEventManager import get_upcoming_events, get_calendar_api, cancel_event
from datetime import datetime


def all_details_page(event):
    """_summary_: this function is to create a page that will display all the details of the event

    Args:
        event (Event response): This object holds all the details of the event which need to be displayed.
    """
    window = tk.Tk()
    event_title = ""
    event_description = "No description provided"
    event_start_time = ""
    event_address = "No Location provided"
    event_attendees = "No other attendees"
    try:
        event_title = event["summary"]
        event_start_time = event["start"]["date"]
        event_address = event["location"]
        event_attendees = event["attendees"]
        event_description = event["description"]
    except KeyError as e:
        print("KeyError: ", e)

    window.title(f"Event Details: {event_title}")
    window.geometry("500x500")
    window.resizable(False, False)
    window.configure(bg="white")

    # Title
    title_label = LabelWidget(window, text=event_title, type="title")
    title_label.place(x=0, y=10, width=500, height=50)

    # Start Time
    start_time_label = LabelWidget(window, text=event_start_time, font=("Arial", 15))
    start_time_label.place(x=0, y=60, width=500, height=50)

    # Description
    description_label = LabelWidget(window, text=event_description, font=("Arial", 15))
    description_label.place(x=0, y=120, width=500, height=100)

    # Address
    address_label = LabelWidget(window, text=event_address, font=("Arial", 15))
    address_label.place(x=0, y=220, width=500, height=50)

    # Attendees
    attendees_label = LabelWidget(window, text=event_attendees, font=("Arial", 15))
    attendees_label.place(x=0, y=270, width=500, height=50)

    # Cancel event button
    def cancel_button_command(event):
        """_summary_: This function is to cancel the event"""
        if messagebox.askokcancel(
            "Cancel Event", "Are you sure you want to cancel this event?"
        ):
            cancel_event(get_calendar_api(), event["id"])
            window.destroy()
        else:
            return

    cancel_event_button = tk.Button(
        window,
        text="Cancel Event",
        font=("Arial", 15),
        bg="red",
        fg="white",
        command=lambda: cancel_button_command(event),
    )
    cancel_event_button.place(x=250, y=450, width=200, height=40)

    window.mainloop()


class RemindersPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

    def show(self, WIDTH, HEIGHT):
        self.SIDEBAR_WIDTH = WIDTH / 5

        MAX_EVENT_TO_SHOW = 7
        START_TIME = datetime.now().isoformat() + "Z"
        upcoming_events = get_upcoming_events(
            get_calendar_api(), START_TIME, MAX_EVENT_TO_SHOW
        )
        print(upcoming_events)

        # Setting up the UI for the reminders page
        TITLE_HEIGHT = HEIGHT / 10
        title_frame = tk.Frame(self)
        title_frame.configure(bg="red")
        title_frame.place(x=0, y=0, width=(WIDTH - WIDTH / 5), height=TITLE_HEIGHT)

        title = LabelWidget(title_frame, "Reminders", "title")
        title.pack()

        # Reminders frame
        reminders_frame = tk.Frame(self)
        # reminders_frame.configure(bg="blue")
        reminders_frame.place(
            x=0,
            y=TITLE_HEIGHT,
            width=(WIDTH - WIDTH / 5),
            height=(HEIGHT - TITLE_HEIGHT),
        )

        def reminder_card(reminder_frame, event):
            card = tk.Frame(reminder_frame)
            card.configure(bg="darkgrey")
            event_title = event["summary"]
            event_start_time = "No time provided"
            try:
                event_start_time = event["start"]["date"]
            except KeyError as e:
                print("KeyError: ", e)

            title_label = LabelWidget(card, event_title, "subtitle", bg="darkgrey")
            date_label = LabelWidget(card, event_start_time, "text", bg="darkgrey")

            title_label.place(x=0, y=0, width=200, height=20)
            date_label.place(x=0, y=20, width=200, height=20)

            more_details_button = tk.Button(
                card, text="More Details", command=lambda: all_details_page(event)
            )
            more_details_button.place(x=350, y=10, width=200, height=30)

            return card

        # Reminders card
        for i, event in enumerate(upcoming_events):
            _card = reminder_card(reminders_frame, event)
            _card.place(x=5, y=5 + (i * 55), relwidth=0.9, height=50)

        # Lift the frame
        self.lift()
