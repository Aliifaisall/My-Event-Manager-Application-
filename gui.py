# GUI imports
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from graphicalcomponents.labelwidget import LabelWidget
from MyEventManager import gui_create_event
from graphicalcomponents.page import Page
from graphicalcomponents.reminder_page import RemindersPage

# ====================== #


# Backend imports
from event import Event
from address import Address
from people.attendee import Attendee
from backend_frontend_bridge import create_event
from MyEventManager import export_events

#  ====================== #

# Misc.and other functions
from datetime import datetime, date
from calendar import calendar, monthrange

# ====================== #

# Colours
SIDEBAR_COLOR = "#9ddfd3"
SIDEBAR_BUTTON_COLOR = "#f0f0f0"
SIDEBAR_BUTTON_TEXT_COLOR = "#000000"


class CreateEventPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        # Add a button
        self.attendees = []

    def show_task_details(self, form_frame, selected_date):
        title_frame_height = HEIGHT / 10
        frame_heights = (HEIGHT / 2) - title_frame_height
        task_frame = tk.Frame(
            form_frame,
            width=(WIDTH - WIDTH / 5) / 2,
            height=frame_heights,
        )
        task_frame.grid(row=1, column=0)
        LabelWidget(task_frame, "Add Task", "subtitle").place(
            x=0, y=0, width=200, height=25
        )

        # Task name
        LabelWidget(task_frame, "Task Name", "text").place(0, 25, 100, 25)
        task_name_entry = tk.Entry(task_frame)
        task_name_entry.place(x=100, y=25, width=200, height=25)

        # Task Time
        LabelWidget(task_frame, "Task Time", "text").place(0, 50, 100, 25)
        task_date_entry = DateEntry(
            task_frame,
            width=12,
            # background="darkblue",
            foreground="white",
            borderwidth=2,
            year=selected_date.year,
            month=selected_date.month,
            day=selected_date.day,
        )
        task_date_entry.configure(date_pattern="yyyy-mm-dd")
        task_date_entry.place(x=100, y=50, width=200, height=25)

        # Task Description
        LabelWidget(task_frame, "Task Description", "text").place(10, 75, 120, 25)
        task_description_entry = tk.Text(task_frame)
        task_description_entry.place(x=20, y=100, width=270, height=100)

        # return reference to all widgets
        return {
            "task_name_entry": task_name_entry,
            "task_date_entry": task_date_entry,
            "task_description_entry": task_description_entry,
        }

    def show(self, selected_date, calendar_referrence):
        self.calendar_referrence = calendar_referrence
        # Page title
        # LabelWidget(self, "Create Event", "title").place_rel_pos(
        #     0, 0, WIDTH / 4, HEIGHT / 10
        # )
        # Creating layout for form fields
        form_frame = tk.Frame(self)
        # Creating the following grid layout
        """
        ------------------------------
        |        Title               |
        -----------------------------
        |  Task     |  Address       |
        |-----------|----------------|
        | Attendees | Attendees list |
        |-----------|----------------|
        |       Submit Button        |  
        ------------------------------
        """
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)
        form_frame.rowconfigure(0, weight=1)
        form_frame.rowconfigure(1, weight=1)
        form_frame.rowconfigure(2, weight=1)
        form_frame.rowconfigure(3, weight=1)

        form_frame.place(x=0, y=0, relwidth=1, relheight=1)
        title_frame_height = HEIGHT / 10
        frame_heights = (HEIGHT / 2) - title_frame_height

        title_frame = tk.Frame(
            form_frame,
            bg="blue",
            width=(WIDTH - WIDTH / 5),
            height=title_frame_height,
        )
        title_frame.grid(row=0, column=0, columnspan=2)

        # Task frame

        # Address frame
        address_frame = tk.Frame(
            form_frame, width=(WIDTH - WIDTH / 5) / 2, height=frame_heights
        )
        address_frame.grid(row=1, column=1)

        # Attendees frame
        attendees_frame = tk.Frame(
            form_frame, width=(WIDTH - WIDTH / 5) / 2, height=frame_heights
        )
        attendees_frame.grid(row=2, column=0)

        # Attendees list frame
        attendees_list_frame = tk.Frame(
            form_frame, width=(WIDTH - WIDTH / 5) / 2, height=frame_heights
        )
        attendees_list_frame.grid(row=2, column=1)

        # Submit button frame
        submit_button_frame = tk.Frame(
            form_frame,
            # bg="yellow",
            width=(WIDTH - WIDTH / 5),
            height=title_frame_height,
        )
        submit_button_frame.grid(row=3, column=0, columnspan=2)

        # Adding the main title to the title frame
        LabelWidget(title_frame, "Create Event", "title").pack(anchor="center")

        # Making the form for task frame ==========================================================
        task_frame_widgets = self.show_task_details(form_frame, selected_date)

        # Making the form for address frame ===================================================
        LabelWidget(address_frame, "Address", "title").place(0, 0, 150, 25)
        # Name
        LabelWidget(address_frame, "Name", "text").place(0, 25, 100, 25)
        address_name_entry = tk.Entry(address_frame)
        address_name_entry.place(x=100, y=25, width=200, height=25)

        # Street
        LabelWidget(address_frame, "Street", "text").place(0, 50, 100, 25)
        address_street_entry = tk.Entry(address_frame)
        address_street_entry.place(x=100, y=50, width=200, height=25)

        # Suburb
        LabelWidget(address_frame, "Suburb", "text").place(0, 75, 100, 25)
        address_suburb_entry = tk.Entry(address_frame)
        address_suburb_entry.place(x=100, y=75, width=200, height=25)

        # State
        LabelWidget(address_frame, "State", "text").place(0, 100, 100, 25)
        address_state_entry = tk.Entry(address_frame)
        address_state_entry.place(x=100, y=100, width=200, height=25)

        # Postcode
        LabelWidget(address_frame, "Postcode", "text").place(0, 125, 100, 25)
        address_postcode_entry = tk.Entry(address_frame)
        address_postcode_entry.place(x=100, y=125, width=200, height=25)

        # Make a listbox for attendees list frame ==============================================
        LabelWidget(attendees_list_frame, "Attendees", "title").place(0, 0, 150, 25)
        attendees_listbox = tk.Listbox(attendees_list_frame)
        attendees_listbox.bind("<Double-1>", self.delete_attendee)
        attendees_listbox.place(x=0, y=25, relwidth=0.8, relheight=0.8)

        # Making the form for attendees frame ===================================================
        LabelWidget(attendees_frame, " Add Attendees", "title").place(0, 0, 250, 25)
        # Name
        LabelWidget(attendees_frame, "Name", "text").place(0, 25, 100, 25)
        attendees_name_entry = tk.Entry(attendees_frame)
        attendees_name_entry.place(x=100, y=25, width=200, height=25)

        # Email
        LabelWidget(attendees_frame, "Email", "text").place(0, 50, 100, 25)
        attendees_email_entry = tk.Entry(attendees_frame)
        attendees_email_entry.place(x=100, y=50, width=200, height=25)

        # Add attendee button
        add_attendee_button = tk.Button(
            attendees_frame,
            text="Add Attendee",
            command=lambda: self.add_attendee(
                attendees_name_entry, attendees_email_entry, attendees_listbox
            ),
        )
        add_attendee_button.place(x=50, y=100, width=200, height=25)

        # Submit button ========================================================================
        submit_button = tk.Button(
            submit_button_frame,
            text="Submit",
            border=3,
            font=("Arial", 18, "bold"),
            command=lambda: self.submit_event(
                {
                    "summary": task_frame_widgets["task_name_entry"],
                    "description": task_frame_widgets["task_description_entry"],
                    "date": task_frame_widgets["task_date_entry"],
                },
                {
                    "name": address_name_entry,
                    "street": address_street_entry,
                    "suburb": address_suburb_entry,
                    "state": address_state_entry,
                    "postcode": address_postcode_entry,
                },
                self.attendees,
            ),
        )
        submit_button.place(
            x=((WIDTH / 2) - (WIDTH / 2.5)), y=0, relwidth=0.8, relheight=1
        )

        self.lift()

    def add_attendee(self, name_entry, email_entry, attendees_listbox):
        """Add attendee to the listbox and the attendees list

        Args:
            name_entry (str): Name of the attendee
            email_entry (str): Email ID of the attendee
            attendees_listbox (tk.ListBox): ListBox widget to display the attendees
        """
        name = name_entry.get()
        email = email_entry.get()
        attendee = Attendee(name, email)
        try:
            attendee.validate()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        if len(self.attendees) >= 20:
            messagebox.showerror("Error", "Maximum number of attendees reached")
            return
        self.attendees.append(attendee)
        # Clear the entries
        name_entry.delete(0, "end")
        email_entry.delete(0, "end")

        attendees_listbox.insert("end", attendee.name)

    def delete_attendee(self, event):
        """Double click to delete an attendee from the listbox
        Args:
            event (_type_): The event that is triggered
        """
        index = event.widget.curselection()[0]
        self.attendees.pop(index)
        event.widget.delete(index)
        print(self.attendees)

    def submit_event(self, event_details: dict, address_details: dict, attendees: list):
        """Submit the event details to the database
        event_details (dict): Dictionary containing the event details
        address_details (dict): Dictionary containing the address details
        attendees (list): List of attendees
        """
        event_summary = event_details["summary"].get()
        event_description = event_details["description"].get("1.0", "end-1c")
        event_date = event_details["date"].get()
        event_date = datetime.strptime(event_date, "%Y-%m-%d")

        event_location_name = address_details["name"].get()
        event_location_street = address_details["street"].get()
        event_location_suburb = address_details["suburb"].get()
        event_location_state = address_details["state"].get()
        event_location_postcode = address_details["postcode"].get()

        # Creating the address
        address = Address(
            event_location_name,
            event_location_street,
            event_location_suburb,
            event_location_state,
            event_location_postcode,
        )

        # if not address.validate():
        #     messagebox.showerror("Error", "Invalid address details")

        try:
            address.validate()
        except ValueError as e:
            messagebox.showerror("Error in Address: ", str(e))
            return

        event_object = Event(
            event_summary,
            event_description,
            event_date,
            address,
            attendees,
        )

        try:
            event_object.validate()
        except ValueError as e:
            messagebox.showerror("Error in Event: ", str(e))
            return

        # Print everything in the Event object
        print(event_object)
        gui_create_event(event_object, address, self.calendar_referrence)
        messagebox.showinfo("Success", "Event created successfully")

        # Clearing the entries
        self.attendees = []
        event_details["summary"].delete(0, "end")
        event_details["description"].delete("1.0", "end")
        address_details["name"].delete(0, "end")
        address_details["street"].delete(0, "end")
        address_details["suburb"].delete(0, "end")
        address_details["state"].delete(0, "end")
        address_details["postcode"].delete(0, "end")

        # Switch page to the calendar page
        self.switch_page_to("calendar")


class CalendarPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        # 2050 is the max date that can be navigate to
        self.max_allowed_date = datetime(2049, 12, 31)
        self.calendar = Calendar(
            self,
            selectmode="day",
            year=date.today().year,
            month=date.today().month,
            day=date.today().day,
            maxdate=self.max_allowed_date,
        )

    def show(self):
        # self.calendar.place(x=WIDTH / 5, y=0, width=4 * WIDTH / 5, height=HEIGHT)
        self.calendar.place(x=0, y=0, relwidth=1, relheight=1)
        self.lift()


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.gui = args[0]

        # sidebar setup
        self.SIDEBAR_WIDTH = WIDTH / 5

        self.sidebar = tk.Frame(
            self.gui,
            width=self.SIDEBAR_WIDTH,
            bg=SIDEBAR_COLOR,
            height=2 * HEIGHT,
            borderwidth=2,
        )
        self.sidebar.place(x=0, y=0)

        # Pages
        self.calendar_page = CalendarPage(self)
        self.create_event_page = CreateEventPage(self)
        self.reminders_page = RemindersPage(self)

        self.calendar_page.place(
            x=self.SIDEBAR_WIDTH, y=0, relwidth=(1 - (1 / 5)), relheight=1
        )

        self.create_event_page.place(
            x=self.SIDEBAR_WIDTH, y=0, relwidth=(1 - (1 / 5)), relheight=1
        )

        self.reminders_page.place(
            x=self.SIDEBAR_WIDTH, y=0, relwidth=(1 - (1 / 5)), relheight=1
        )

        # Show the calendar page by default
        self.switch_page_to("calendar")
        self.side_nav_buttons()

    def side_nav_buttons(self):
        """_summary_ : Creates the side navigation buttons"""
        sidebar_button_height = HEIGHT / 10
        sidebar_button_width = self.SIDEBAR_WIDTH

        calendar_view_button = tk.Button(
            self.sidebar,
            text="Calendar",
            bg=SIDEBAR_BUTTON_COLOR,
            fg=SIDEBAR_BUTTON_TEXT_COLOR,
            borderwidth=1,
            command=lambda: self.switch_page_to("calendar"),
        )

        create_event_button = tk.Button(
            self.sidebar,
            text="Create Event",
            bg=SIDEBAR_BUTTON_COLOR,
            fg=SIDEBAR_BUTTON_TEXT_COLOR,
            borderwidth=1,
            command=lambda: self.switch_page_to("create_event"),
        )

        reminder_button = tk.Button(
            self.sidebar,
            text="Reminders",
            bg=SIDEBAR_BUTTON_COLOR,
            fg=SIDEBAR_BUTTON_TEXT_COLOR,
            borderwidth=1,
            command=lambda: self.switch_page_to("reminders"),
        )

        export_button = tk.Button(
            self.sidebar,
            text="Export",
            bg=SIDEBAR_BUTTON_COLOR,
            fg=SIDEBAR_BUTTON_TEXT_COLOR,
            borderwidth=1,
            command=export_events,
        )

        # Place the sidebar buttons
        calendar_view_button.place(
            x=0, y=0, width=sidebar_button_width, height=sidebar_button_height
        )
        create_event_button.place(
            x=0,
            y=sidebar_button_height,
            width=sidebar_button_width,
            height=sidebar_button_height,
        )
        reminder_button.place(
            x=0,
            y=2 * sidebar_button_height,
            width=sidebar_button_width,
            height=sidebar_button_height,
        )
        export_button.place(
            x=0,
            y=3 * sidebar_button_height,
            width=sidebar_button_width,
            height=sidebar_button_height,
        )

    def switch_page_to(self, page_name: str):
        """_summary_ : Switches the page to the page_name"""
        if page_name == "calendar":
            self.calendar_page.show()

        elif page_name == "create_event":
            calendar_date = self.calendar_page.calendar.selection_get()
            self.create_event_page.show(calendar_date, self.calendar_page.calendar)
            # self.create_event_page.create_event(calendar_date)

        elif page_name == "reminders":
            self.reminders_page.show(WIDTH, HEIGHT)
        else:
            raise ValueError("Invalid page name")


def gui_setup(width: int, height: int, title: str, main_view: MainView) -> None:
    """_summary_ : Sets up the GUI"""
    root = tk.Tk()
    root.title(title)
    root.geometry(f"{width}x{height}")
    root.resizable(False, False)
    main_view = main_view(root)
    main_view.pack(side="top", fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    WIDTH = 800
    HEIGHT = 600
    gui_setup(WIDTH, HEIGHT, "MyEventManager", MainView)
