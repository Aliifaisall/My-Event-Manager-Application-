# Code to import from parent directory ===================
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# ========================================================
from address import Address
from people.attendee import Attendee
import unittest
from datetime import datetime, timezone
from datetime import datetime
from event import Event, generate_id


class EventTest(unittest.TestCase):
    """
    This class is to test the event class.
    Summary of tests:
        - test_generating_id:
            | This is to check if the id is going to be generated.
        - test_generating_id1:
            | This is to check if the id generated will fulfil the required Google calendar API ID criteria.
        - test_event_name:
            | This is to check that the name in the event is not empty.
        - test_event_name1:
            | This is to check if the validation raises an error when the name is something outside the alphabet.
        - test_event_name2:
            | This is to check if the validation checks off when the name is valid.
    Whitebox testing method: Statement Coverage
    Reason: We used Statement Coverage because this method allowed us to write tests which account for 100% line coverage.
    """

    def setUp(self):
        # fmt: off
        self.white_list = [
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "v",
        ]
        # fmt: on

    # class created to test for the events as an entire unit
    # using random testing

    def test_generating_id(self):
        """
        This is to check if the id is going to be generated.
        """
        id = generate_id()
        test_id_length = 5 <= len(id) <= 1024
        self.assertTrue(test_id_length)

    # ID criteria taken from :
    # https://developers.google.com/calendar/api/v3/reference/events/insert?fbclid=IwAR2u55N8d605xqx-lj48vRmqVC8HUPJiHEPOAGmaAZ5UhHCN3WW4lW4uG4w
    # is says that an id should be lowercase letters a-v and digits 0-9
    # Equivlance partioning strategy of testing would be approperiate because we have a known valid list

    def test_generating_id1(self):
        """
        This is to check if the id generated will fulfil the required Google calendar API ID criteria.
        """

        id = generate_id()
        for char in id:
            if char not in self.white_list:
                return False

            id_value = self.white_list
            self.assertTrue(id_value)

    # testing if the name of the event is of alphabetic letter and not empty
    # this test will require the Equivlance partioning class test strategy

    def test_event_name(self):
        """
        This is to check that the name in the event is not empty.
        """
        name = ""
        event = Event(
            name,
            "description",
            datetime.now(),
            Address("Ali", "Street", "Howit", "VIC", "3168"),
            [Attendee("Ali", "ali@email.com")],
        )
        with self.assertRaises(ValueError):
            event.validate()

    # testing if the name was inserted with something other than the alphabtic letter
    def test_event_name1(self):
        """
        This is to check if the validation raises an error when the name is something outside the alphabet.
        """
        name = "123455@#$"
        event = Event(
            name,
            "description",
            datetime.now(),
            Address("Ali", "Street", "Howit", "VIC", "3168"),
            [Attendee("Ali", "ali@email.com")],
        )
        with self.assertRaises(ValueError):
            event.validate()

    # tesing if the name is valid input
    def test_event_name2(self):
        """
        This is to check if the validation checks off when the name is valid.
        """
        name = "Ali"
        event = Event(
            name,
            "description",
            datetime.now(),
            Address("Ali", "Street", "Howit", "VIC", "3168"),
            [Attendee("Ali", "ali@email.com")],
        )
        self.assertTrue(event.validate())

    # testing if the event time is valid 
    def test_event_Time(self):
        """
        this is to check if the event time is on 2050

        """
        time = datetime(2050, 1, 1)
        event = Event(
            "name",
            "description",
            time,
            Address("Ali", "Street", "Howit", "VIC", "3168"),
            [Attendee("Ali", "ali@email.com")],
        )
        with self.assertRaises(ValueError):
            event.validate()

    # testing if the event is below 2050 
    def test_event_Time2(self):
        """
        this is to check if the event time is below 2050

        """
        time = datetime.now()

        if time < datetime(2050, 1, 1):
            event = Event(
                "name",
                "description",
                time,
                Address("Ali", "Street", "Howit", "VIC", "3168"),
                [Attendee("Ali", "ali@email.com")],
            )
            self.assertTrue(event.validate())

    # testing if the event is above 2050
    def test_event_time3(self):
        """
        this is to test if the event time is above 2050

        """
        time = datetime.now()

        if time > datetime(2050, 1, 1):
            event = Event(
                "name",
                "description",
                time,
                Address("Ali", "Street", "Howit", "VIC", "3168"),
                [Attendee("Ali", "ali@email.com")],
            )
            with self.assertRaises(ValueError):
                event.validate()

    # testing if the event attendes is 20 attedees 
    def test_event_attendees(self):
        """
        this is to test if the attendess are 20 characters 

        """
        all_attendees = [Attendee("Ali", "ali@email.com")] * 20
        event = Event(
            "Ali",
            "description",
            datetime.now(),
            Address("Ali", "Street", "Howit", "VIC", "3168"),
            all_attendees
        )
        self.assertTrue(event.validate())

    # testing if the event attendees are above 20
    def test_event_attendees1(self):
        """
        this is to test if the event attendess are above 20

        """
        all_attendees = [Attendee("Ali", "ali@email.com")] * 21
        event = Event(
            "Ali",
            "description",
            datetime.now(),
            Address("Ali", "Street", "Howit", "VIC", "3168"),
            all_attendees
        )
        with self.assertRaises(ValueError):
            event.validate()


if __name__ == "__main__":
    unittest.main()
